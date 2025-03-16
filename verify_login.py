import sys
import os
import traceback
import pymysql
from werkzeug.security import check_password_hash, generate_password_hash

def verify_login():
    print("===== 验证登录问题 =====")
    
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
        
        # 获取数据库连接信息
        db_uri = app.config['SQLALCHEMY_DATABASE_URI']
        print(f"数据库URI: {db_uri}")
        
        # 解析数据库连接信息
        import re
        match = re.match(r'mysql\+pymysql://([^:]+):([^@]+)@([^/]+)/(.+)', db_uri)
        if match:
            db_user, db_pass, db_host, db_name = match.groups()
            print(f"解析数据库连接信息成功: {db_user}@{db_host}/{db_name}")
        else:
            print(f"无法解析数据库连接信息: {db_uri}")
            return False
        
        # 连接数据库
        try:
            conn = pymysql.connect(
                host=db_host,
                user=db_user,
                password=db_pass,
                database=db_name,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            print("数据库连接成功")
        except Exception as e:
            print(f"数据库连接失败: {str(e)}")
            traceback.print_exc()
            return False
        
        cursor = conn.cursor()
        
        # 检查user表是否存在
        cursor.execute("SHOW TABLES LIKE 'user'")
        if not cursor.fetchone():
            print("错误: user表不存在，请先运行创建账号的脚本")
            return False
        
        # 检查管理员账号
        admin_accounts = ['superadmin', 'dashboard_admin', 'compass_admin', 'cube_admin']
        test_password = '123456'
        
        print("\n===== 测试管理员账号 =====")
        for username in admin_accounts:
            cursor.execute("SELECT * FROM `user` WHERE `username` = %s", (username,))
            user = cursor.fetchone()
            
            if not user:
                print(f"错误: 账号 {username} 不存在于数据库中")
                continue
            
            print(f"\n账号: {username}")
            print(f"  ID: {user['id']}")
            print(f"  密码哈希: {user['password_hash']}")
            print(f"  是否管理员: {'是' if user.get('is_admin') else '否'}")
            print(f"  是否超级管理员: {'是' if user.get('is_super_admin') else '否'}")
            print(f"  全域驾驶舱权限: {'是' if user.get('dashboard_access') else '否'}")
            print(f"  供需罗盘权限: {'是' if user.get('compass_access') else '否'}")
            print(f"  智投魔方权限: {'是' if user.get('cube_access') else '否'}")
            print(f"  受保护状态: {'是' if user.get('protected') else '否'}")
            
            # 验证密码
            if check_password_hash(user['password_hash'], test_password):
                print(f"  密码验证: 成功 (密码 '{test_password}' 正确)")
            else:
                print(f"  密码验证: 失败 (密码 '{test_password}' 不正确)")
                
                # 重置密码
                print(f"  正在重置密码...")
                new_password_hash = generate_password_hash(test_password)
                cursor.execute("""
                UPDATE `user` SET 
                    `password_hash` = %s
                WHERE `username` = %s
                """, (
                    new_password_hash,
                    username
                ))
                conn.commit()
                print(f"  密码已重置为: {test_password}")
        
        # 检查登录路由
        main_file_path = os.path.join('info_user', 'main.py')
        if os.path.exists(main_file_path):
            with open(main_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print("\n===== 检查登录路由 =====")
            if 'def login' in content:
                print("登录路由存在")
                
                # 检查密码验证逻辑
                if 'check_password_hash' in content and 'password_hash' in content:
                    print("密码验证逻辑存在")
                else:
                    print("警告: 密码验证逻辑可能有问题")
                
                # 检查会话管理
                if 'login_user' in content and 'session' in content:
                    print("会话管理逻辑存在")
                else:
                    print("警告: 会话管理逻辑可能有问题")
            else:
                print("错误: 登录路由不存在")
        
        # 检查登录模板
        login_template_path = os.path.join('info_user', 'templates', 'login.html')
        if os.path.exists(login_template_path):
            with open(login_template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print("\n===== 检查登录模板 =====")
            if 'form' in content and 'method="POST"' in content:
                print("登录表单存在且使用POST方法")
            else:
                print("警告: 登录表单可能有问题")
            
            if 'name="username"' in content and 'name="password"' in content:
                print("用户名和密码输入框存在")
            else:
                print("警告: 用户名或密码输入框可能有问题")
        else:
            print("错误: 登录模板不存在")
        
        # 创建一个新的测试账号
        print("\n===== 创建测试账号 =====")
        test_username = "test_login_user"
        test_password = "test123"
        
        # 检查测试账号是否已存在
        cursor.execute("SELECT * FROM `user` WHERE `username` = %s", (test_username,))
        if cursor.fetchone():
            # 删除已存在的测试账号
            cursor.execute("DELETE FROM `user` WHERE `username` = %s", (test_username,))
            print(f"已删除已存在的测试账号: {test_username}")
        
        # 创建新的测试账号
        password_hash = generate_password_hash(test_password)
        
        cursor.execute("""
        INSERT INTO `user` (
            `username`, 
            `password_hash`, 
            `is_admin`, 
            `is_super_admin`, 
            `dashboard_access`, 
            `compass_access`, 
            `cube_access`
        ) VALUES (%s, %s, TRUE, TRUE, TRUE, TRUE, TRUE)
        """, (
            test_username,
            password_hash
        ))
        conn.commit()
        print(f"已创建测试账号: {test_username} / {test_password}")
        
        # 验证测试账号
        cursor.execute("SELECT * FROM `user` WHERE `username` = %s", (test_username,))
        test_user = cursor.fetchone()
        if test_user and check_password_hash(test_user['password_hash'], test_password):
            print(f"测试账号验证成功")
        else:
            print(f"警告: 测试账号验证失败")
        
        # 关闭连接
        cursor.close()
        conn.close()
        
        print("\n===== 登录问题验证完成 =====")
        print("\n可能的解决方案:")
        print("1. 所有管理员账号的密码已重置为: 123456")
        print("2. 尝试使用新创建的测试账号登录: test_login_user / test123")
        print("3. 确保应用已重启，并且正在使用正确的数据库")
        print("4. 检查浏览器缓存和Cookie，尝试清除后再登录")
        print("5. 检查应用日志，查看是否有错误信息")
        print("6. 确保登录表单正确提交到/login路由")
        
        return True
    
    except Exception as e:
        print(f"验证登录问题时出错: {str(e)}")
        traceback.print_exc()
        return False

if __name__ == '__main__':
    verify_login() 