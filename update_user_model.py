import sys
import os
import traceback
from sqlalchemy import Column, Boolean

def update_user_model():
    print("===== 更新User模型，添加protected字段 =====")
    
    try:
        # 获取应用配置
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        try:
            from info_user.main import app, db, User
            print("成功导入应用模块")
        except Exception as e:
            print(f"导入应用模块失败: {str(e)}")
            traceback.print_exc()
            return False
        
        # 检查User模型是否已有protected字段
        if hasattr(User, 'protected'):
            print("User模型已有protected字段，无需更新")
            return True
        
        # 添加protected字段到User模型
        with app.app_context():
            # 添加字段到模型
            User.protected = Column(Boolean, default=False)
            
            # 更新数据库表结构
            try:
                # 检查数据库中是否已有protected字段
                inspector = db.inspect(db.engine)
                columns = [c['name'] for c in inspector.get_columns('user')]
                
                if 'protected' not in columns:
                    # 添加字段到数据库表
                    db.engine.execute('ALTER TABLE user ADD COLUMN protected BOOLEAN DEFAULT FALSE')
                    print("已添加protected字段到user表")
                else:
                    print("user表已有protected字段，无需添加")
            except Exception as e:
                print(f"更新数据库表结构失败: {str(e)}")
                traceback.print_exc()
                return False
        
        # 修改User模型定义文件
        main_file_path = os.path.join('info_user', 'main.py')
        if os.path.exists(main_file_path):
            with open(main_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 备份原始文件
            with open(main_file_path + '.bak', 'w', encoding='utf-8') as f:
                f.write(content)
            
            # 查找User模型定义
            import re
            user_model_pattern = r'class User\(UserMixin, db\.Model\):(.*?)def'
            user_model_match = re.search(user_model_pattern, content, re.DOTALL)
            
            if user_model_match:
                user_model_code = user_model_match.group(1)
                
                # 检查是否已经有protected字段
                if 'protected' not in user_model_code:
                    # 找到最后一个字段定义
                    last_field_pattern = r'(\s+\w+_access = db\.Column.*?\))'
                    last_field_match = re.search(last_field_pattern, user_model_code, re.DOTALL)
                    
                    if last_field_match:
                        last_field = last_field_match.group(1)
                        # 在最后一个字段后添加protected字段
                        new_field = f"{last_field}\n    protected = db.Column(db.Boolean, default=False)  # 保护字段，防止账号被删除"
                        modified_model_code = user_model_code.replace(last_field, new_field)
                        
                        # 替换原始代码
                        content = content.replace(user_model_code, modified_model_code)
                        
                        # 写入修改后的内容
                        with open(main_file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        
                        print("已修改User模型定义，添加了protected字段")
                    else:
                        print("无法找到合适的位置添加protected字段")
                        return False
                else:
                    print("User模型定义中已有protected字段，无需修改")
            else:
                print("无法找到User模型定义")
                return False
        
        print("===== User模型更新完成 =====")
        return True
    
    except Exception as e:
        print(f"更新User模型时出错: {str(e)}")
        traceback.print_exc()
        return False

if __name__ == '__main__':
    update_user_model() 