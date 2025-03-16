import sys
import os
import traceback
import re

def add_delete_user_route():
    print("===== 添加删除用户路由 =====")
    
    try:
        # 获取应用配置
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        try:
            from info_user.main import app
            print("成功导入应用模块")
        except Exception as e:
            print(f"导入应用模块失败: {str(e)}")
            traceback.print_exc()
            return False
        
        # 修改main.py，添加删除用户路由
        main_file_path = os.path.join('info_user', 'main.py')
        if not os.path.exists(main_file_path):
            print(f"错误: 主应用文件不存在: {main_file_path}")
            return False
        
        # 读取main.py内容
        with open(main_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 备份原始文件
        with open(main_file_path + '.bak', 'w', encoding='utf-8') as f:
            f.write(content)
        
        # 检查是否已经有删除用户的路由
        if 'def delete_user' in content:
            print("删除用户路由已存在，检查是否需要添加保护机制...")
            
            # 查找删除用户的函数
            delete_user_pattern = r'def\s+delete_user\s*\([^)]*\):(.*?)(?:@app\.route|\Z)'
            delete_user_match = re.search(delete_user_pattern, content, re.DOTALL)
            
            if delete_user_match:
                delete_user_code = delete_user_match.group(1)
                
                # 检查是否已经有保护检查
                if 'protected' not in delete_user_code:
                    # 在查询用户后添加保护检查
                    modified_code = delete_user_code.replace(
                        "user = User.query.get_or_404(user_id)",
                        "user = User.query.get_or_404(user_id)\n    if user.protected:\n        flash('不能删除受保护的管理员账号', 'danger')\n        return redirect(url_for('admin'))"
                    )
                    
                    # 替换原始代码
                    content = content.replace(delete_user_code, modified_code)
                    
                    # 写入修改后的内容
                    with open(main_file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print("已修改删除用户的路由，添加了保护检查")
                else:
                    print("删除用户路由已有保护机制，无需修改")
            else:
                print("无法找到完整的删除用户函数，无法修改")
        else:
            print("删除用户路由不存在，添加新的路由...")
            
            # 检查是否已导入必要的模块
            imports_to_add = []
            
            if 'from flask import' in content:
                # 更新现有的Flask导入
                flask_import_pattern = r'from flask import (.*?)\n'
                flask_import_match = re.search(flask_import_pattern, content)
                
                if flask_import_match:
                    flask_imports = flask_import_match.group(1)
                    needed_imports = ['flash', 'redirect', 'url_for']
                    missing_imports = [imp for imp in needed_imports if imp not in flask_imports]
                    
                    if missing_imports:
                        new_flask_imports = flask_imports.rstrip()
                        if new_flask_imports.endswith(','):
                            new_flask_imports += ' ' + ', '.join(missing_imports)
                        else:
                            new_flask_imports += ', ' + ', '.join(missing_imports)
                        
                        content = re.sub(flask_import_pattern, f'from flask import {new_flask_imports}\n', content)
                        print(f"已更新Flask导入: {', '.join(missing_imports)}")
            
            # 添加删除用户路由
            delete_user_route = '''
@app.route('/delete_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def delete_user(user_id):
    # 获取用户信息
    user = User.query.get_or_404(user_id)
    
    # 检查是否是受保护的管理员账号
    if hasattr(user, 'protected') and user.protected:
        flash('不能删除受保护的管理员账号', 'danger')
        return redirect(url_for('admin'))
    
    # 检查权限：超级管理员可以删除所有用户，其他管理员只能删除有权限的系统的用户
    if not current_user.is_admin:
        if not current_user.has_system_access(user.service_type):
            flash('没有权限删除此用户', 'danger')
            return redirect(url_for('admin'))
    
    # 删除用户
    db.session.delete(user)
    db.session.commit()
    
    flash('用户已成功删除', 'success')
    return redirect(url_for('admin'))
'''
            
            # 找到合适的位置添加删除用户路由
            update_user_status_pattern = r'@app\.route\([\'"]\/update_user_status[\'"](.*?)def\s+update_user_status\s*\(.*?\):(.*?)return\s+jsonify\(\{[\'"]success[\'"]\s*:\s*True\}\)'
            update_user_status_match = re.search(update_user_status_pattern, content, re.DOTALL)
            
            if update_user_status_match:
                # 在update_user_status路由后添加
                update_user_status_end = update_user_status_match.end()
                content = content[:update_user_status_end] + '\n' + delete_user_route + content[update_user_status_end:]
                print("已添加删除用户路由")
            else:
                # 在文件末尾添加
                content += '\n' + delete_user_route
                print("已添加删除用户路由（在文件末尾）")
            
            # 写入修改后的内容
            with open(main_file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        # 修改admin.html，添加删除按钮
        admin_template_path = os.path.join('info_user', 'templates', 'admin.html')
        if os.path.exists(admin_template_path):
            with open(admin_template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            
            # 备份原始模板
            with open(admin_template_path + '.bak', 'w', encoding='utf-8') as f:
                f.write(template_content)
            
            # 检查是否已经有删除按钮
            if 'delete-btn' not in template_content and 'data-status="rejected"' in template_content:
                # 找到拒绝按钮的位置
                reject_button_pattern = r'<button type="button" class="btn btn-sm btn-danger status-btn" data-user-id="\{\{ user\.id \}\}" data-status="rejected">(.*?)</button>'
                reject_button_match = re.search(reject_button_pattern, template_content, re.DOTALL)
                
                if reject_button_match:
                    reject_button = reject_button_match.group(0)
                    # 在拒绝按钮后添加删除按钮
                    delete_button = '''
                                    <button type="button" class="btn btn-sm btn-danger delete-btn" data-user-id="{{ user.id }}">
                                        <i class="bi bi-trash"></i> 删除
                                    </button>'''
                    template_content = template_content.replace(reject_button, reject_button + delete_button)
                    
                    # 添加删除按钮的JavaScript处理
                    script_end_pattern = r'</script>\s*</body>'
                    script_end_match = re.search(script_end_pattern, template_content)
                    
                    if script_end_match:
                        delete_button_script = '''
            // 删除用户处理
            const deleteButtons = document.querySelectorAll('.delete-btn');
            deleteButtons.forEach(button => {
                button.addEventListener('click', function() {
                    const userId = this.dataset.userId;
                    
                    if (confirm('确定要删除此用户吗？此操作不可撤销！')) {
                        window.location.href = `/delete_user/${userId}`;
                    }
                });
            });
            '''
                        script_end = script_end_match.group(0)
                        template_content = template_content.replace(script_end, delete_button_script + script_end)
                    
                    # 写入修改后的内容
                    with open(admin_template_path, 'w', encoding='utf-8') as f:
                        f.write(template_content)
                    
                    print("已添加删除按钮到管理界面")
                else:
                    print("无法找到拒绝按钮的位置，无法添加删除按钮")
            else:
                print("管理界面已有删除按钮或找不到合适的位置添加")
        
        print("===== 删除用户路由添加完成 =====")
        return True
    
    except Exception as e:
        print(f"添加删除用户路由时出错: {str(e)}")
        traceback.print_exc()
        return False

if __name__ == '__main__':
    add_delete_user_route() 