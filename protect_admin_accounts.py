import sys
import os
import traceback
import pymysql
from werkzeug.security import generate_password_hash

def protect_admin_accounts():
    print("===== 创建并保护管理员账号 =====")
    
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
        conn = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_pass,
            database=db_name,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        cursor = conn.cursor()
        
        # 检查user表是否存在
        cursor.execute("SHOW TABLES LIKE 'user'")
        if not cursor.fetchone():
            print("user表不存在，创建表...")
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS `user` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `username` VARCHAR(80) UNIQUE NOT NULL,
                `password_hash` VARCHAR(255) NOT NULL,
                `is_admin` BOOLEAN DEFAULT TRUE,
                `is_super_admin` BOOLEAN DEFAULT FALSE,
                `dashboard_access` BOOLEAN DEFAULT FALSE,
                `compass_access` BOOLEAN DEFAULT FALSE,
                `cube_access` BOOLEAN DEFAULT FALSE,
                `protected` BOOLEAN DEFAULT FALSE
            )
            """)
            conn.commit()
        else:
            # 检查是否有protected字段，如果没有则添加
            cursor.execute("SHOW COLUMNS FROM `user` LIKE 'protected'")
            if not cursor.fetchone():
                print("添加protected字段到user表...")
                cursor.execute("ALTER TABLE `user` ADD COLUMN `protected` BOOLEAN DEFAULT FALSE")
                conn.commit()
        
        # 创建或更新管理员账号
        admin_accounts = [
            {
                'username': 'superadmin',
                'password': '123456',
                'is_super_admin': True,
                'dashboard_access': True,
                'compass_access': True,
                'cube_access': True
            },
            {
                'username': 'dashboard_admin',
                'password': '123456',
                'is_super_admin': False,
                'dashboard_access': True,
                'compass_access': False,
                'cube_access': False
            },
            {
                'username': 'compass_admin',
                'password': '123456',
                'is_super_admin': False,
                'dashboard_access': False,
                'compass_access': True,
                'cube_access': False
            },
            {
                'username': 'cube_admin',
                'password': '123456',
                'is_super_admin': False,
                'dashboard_access': False,
                'compass_access': False,
                'cube_access': True
            }
        ]
        
        for account in admin_accounts:
            # 检查账号是否存在
            cursor.execute("SELECT * FROM `user` WHERE `username` = %s", (account['username'],))
            existing_user = cursor.fetchone()
            
            if existing_user:
                # 更新现有账号
                cursor.execute("""
                UPDATE `user` SET 
                    `password_hash` = %s,
                    `is_admin` = TRUE,
                    `is_super_admin` = %s,
                    `dashboard_access` = %s,
                    `compass_access` = %s,
                    `cube_access` = %s,
                    `protected` = TRUE
                WHERE `username` = %s
                """, (
                    generate_password_hash(account['password']),
                    account['is_super_admin'],
                    account['dashboard_access'],
                    account['compass_access'],
                    account['cube_access'],
                    account['username']
                ))
                print(f"更新管理员账号: {account['username']}")
            else:
                # 创建新账号
                cursor.execute("""
                INSERT INTO `user` (
                    `username`, 
                    `password_hash`, 
                    `is_admin`, 
                    `is_super_admin`, 
                    `dashboard_access`, 
                    `compass_access`, 
                    `cube_access`,
                    `protected`
                ) VALUES (%s, %s, TRUE, %s, %s, %s, %s, TRUE)
                """, (
                    account['username'],
                    generate_password_hash(account['password']),
                    account['is_super_admin'],
                    account['dashboard_access'],
                    account['compass_access'],
                    account['cube_access']
                ))
                print(f"创建管理员账号: {account['username']}")
        
        conn.commit()
        
        # 创建触发器，防止删除受保护的账号
        cursor.execute("SHOW TRIGGERS LIKE 'prevent_admin_deletion'")
        if not cursor.fetchone():
            print("创建触发器，防止删除受保护的管理员账号...")
            cursor.execute("""
            CREATE TRIGGER prevent_admin_deletion
            BEFORE DELETE ON `user`
            FOR EACH ROW
            BEGIN
                IF OLD.protected = TRUE THEN
                    SIGNAL SQLSTATE '45000' 
                    SET MESSAGE_TEXT = 'Cannot delete protected admin account';
                END IF;
            END;
            """)
            conn.commit()
        
        # 修改main.py，添加删除用户前的检查
        main_file_path = os.path.join('info_user', 'main.py')
        if os.path.exists(main_file_path):
            with open(main_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否已经有删除用户的路由
            if 'def delete_user' in content:
                print("修改删除用户的路由，添加保护检查...")
                
                # 备份原始文件
                with open(main_file_path + '.bak', 'w', encoding='utf-8') as f:
                    f.write(content)
                
                # 查找删除用户的函数
                import re
                delete_user_pattern = r'def\s+delete_user\s*\([^)]*\):(.*?)(?:@app\.route|\Z)'
                delete_user_match = re.search(delete_user_pattern, content, re.DOTALL)
                
                if delete_user_match:
                    delete_user_code = delete_user_match.group(1)
                    
                    # 检查是否已经有保护检查
                    if 'protected' not in delete_user_code:
                        # 在查询用户后添加保护检查
                        modified_code = delete_user_code.replace(
                            "user = User.query.get_or_404(user_id)",
                            "user = User.query.get_or_404(user_id)\n    if user.protected:\n        flash('不能删除受保护的管理员账号')\n        return redirect(url_for('admin'))"
                        )
                        
                        # 替换原始代码
                        content = content.replace(delete_user_code, modified_code)
                        
                        # 写入修改后的内容
                        with open(main_file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        
                        print("已修改删除用户的路由，添加了保护检查")
        
        # 验证管理员账号
        print("\n===== 验证管理员账号 =====")
        cursor.execute("SELECT * FROM `user` WHERE `protected` = TRUE")
        protected_users = cursor.fetchall()
        
        print(f"受保护的管理员账号数量: {len(protected_users)}")
        for user in protected_users:
            print(f"用户名: {user['username']}")
            print(f"  超级管理员: {'是' if user['is_super_admin'] else '否'}")
            print(f"  全域驾驶舱权限: {'是' if user['dashboard_access'] else '否'}")
            print(f"  供需罗盘权限: {'是' if user['compass_access'] else '否'}")
            print(f"  智投魔方权限: {'是' if user['cube_access'] else '否'}")
            print(f"  受保护状态: {'是' if user['protected'] else '否'}")
            print("")
        
        # 关闭连接
        cursor.close()
        conn.close()
        
        print("===== 管理员账号创建并保护完成 =====")
        print("\n请使用以下账号登录:")
        print("1. 超级管理员: superadmin / 123456")
        print("2. 全域驾驶舱管理员: dashboard_admin / 123456")
        print("3. 供需罗盘管理员: compass_admin / 123456")
        print("4. 智投魔方管理员: cube_admin / 123456")
        
        return True
    
    except Exception as e:
        print(f"保护管理员账号时出错: {str(e)}")
        traceback.print_exc()
        return False

if __name__ == '__main__':
    protect_admin_accounts() 