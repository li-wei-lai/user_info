import sys
import os
import traceback
import pymysql
from werkzeug.security import generate_password_hash

def create_admin_accounts():
    print("===== 创建管理员账号 =====")
    
    try:
        # 数据库连接信息 - 使用应用中的实际配置
        db_host = 'rm-uf6d863v517727p6mdo.mysql.rds.aliyuncs.com'
        db_user = 'heyin_data_jony'
        db_pass = 'Jony_123'
        db_name = 'test_db'
        
        print(f"尝试连接数据库: {db_user}@{db_host}/{db_name}")
        
        # 连接数据库
        conn = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_pass,
            database=db_name,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        print("数据库连接成功")
        
        cursor = conn.cursor()
        
        # 检查user表是否存在
        cursor.execute("SHOW TABLES LIKE 'user'")
        if not cursor.fetchone():
            print("错误: user表不存在，需要先创建表")
            
            # 创建user表
            cursor.execute("""
            CREATE TABLE `user` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `username` VARCHAR(64) UNIQUE NOT NULL,
                `password_hash` VARCHAR(256) NOT NULL,
                `is_admin` BOOLEAN DEFAULT FALSE,
                `is_super_admin` BOOLEAN DEFAULT FALSE,
                `dashboard_access` BOOLEAN DEFAULT FALSE,
                `compass_access` BOOLEAN DEFAULT FALSE,
                `cube_access` BOOLEAN DEFAULT FALSE,
                `protected` BOOLEAN DEFAULT FALSE,
                `description` TEXT
            )
            """)
            conn.commit()
            print("已创建user表")
        
        # 定义管理员账号
        admin_accounts = [
            {
                'username': 'superadmin',
                'password': '123456',
                'is_admin': True,
                'is_super_admin': True,
                'dashboard_access': True,
                'compass_access': True,
                'cube_access': True,
                'protected': True,
                'description': '超级管理员 - 拥有所有权限'
            },
            {
                'username': 'dashboard_admin',
                'password': '123456',
                'is_admin': True,
                'is_super_admin': False,
                'dashboard_access': True,
                'compass_access': False,
                'cube_access': False,
                'protected': True,
                'description': '全域驾驶舱管理员'
            },
            {
                'username': 'compass_admin',
                'password': '123456',
                'is_admin': True,
                'is_super_admin': False,
                'dashboard_access': False,
                'compass_access': True,
                'cube_access': False,
                'protected': True,
                'description': '供需罗盘管理员'
            },
            {
                'username': 'cube_admin',
                'password': '123456',
                'is_admin': True,
                'is_super_admin': False,
                'dashboard_access': False,
                'compass_access': False,
                'cube_access': True,
                'protected': True,
                'description': '智投魔方管理员'
            }
        ]
        
        # 获取表结构
        cursor.execute("DESCRIBE `user`")
        columns = [column['Field'] for column in cursor.fetchall()]
        print(f"user表的列: {', '.join(columns)}")
        
        # 创建管理员账号
        for account in admin_accounts:
            # 检查账号是否已存在
            cursor.execute("SELECT * FROM `user` WHERE `username` = %s", (account['username'],))
            if cursor.fetchone():
                print(f"账号 {account['username']} 已存在，更新密码和权限")
                
                # 更新账号
                password_hash = generate_password_hash(account['password'])
                
                # 构建更新SQL
                update_fields = []
                update_values = []
                
                for field, value in account.items():
                    if field != 'username' and field != 'password' and field in columns:
                        if field == 'password_hash':
                            update_fields.append(f"`{field}` = %s")
                            update_values.append(password_hash)
                        else:
                            update_fields.append(f"`{field}` = %s")
                            update_values.append(value)
                
                # 添加密码哈希
                if 'password_hash' not in account and 'password_hash' in columns:
                    update_fields.append("`password_hash` = %s")
                    update_values.append(password_hash)
                
                # 添加用户名作为WHERE条件
                update_values.append(account['username'])
                
                # 执行更新
                sql = f"UPDATE `user` SET {', '.join(update_fields)} WHERE `username` = %s"
                cursor.execute(sql, update_values)
            else:
                print(f"创建新账号: {account['username']}")
                
                # 创建新账号
                password_hash = generate_password_hash(account['password'])
                
                # 构建插入SQL
                fields = []
                values = []
                placeholders = []
                
                for field, value in account.items():
                    if field != 'password' and field in columns:
                        fields.append(f"`{field}`")
                        values.append(value)
                        placeholders.append("%s")
                
                # 添加密码哈希
                if 'password_hash' not in account and 'password_hash' in columns:
                    fields.append("`password_hash`")
                    values.append(password_hash)
                    placeholders.append("%s")
                
                # 执行插入
                sql = f"INSERT INTO `user` ({', '.join(fields)}) VALUES ({', '.join(placeholders)})"
                cursor.execute(sql, values)
            
            conn.commit()
            print(f"账号 {account['username']} 处理完成")
        
        # 验证账号
        print("\n===== 验证管理员账号 =====")
        for account in admin_accounts:
            cursor.execute("SELECT * FROM `user` WHERE `username` = %s", (account['username'],))
            user = cursor.fetchone()
            
            if user:
                print(f"\n账号: {user['username']}")
                print(f"  ID: {user['id']}")
                print(f"  是否管理员: {'是' if user.get('is_admin') else '否'}")
                print(f"  是否超级管理员: {'是' if user.get('is_super_admin') else '否'}")
                print(f"  全域驾驶舱权限: {'是' if user.get('dashboard_access') else '否'}")
                print(f"  供需罗盘权限: {'是' if user.get('compass_access') else '否'}")
                print(f"  智投魔方权限: {'是' if user.get('cube_access') else '否'}")
                print(f"  受保护状态: {'是' if user.get('protected') else '否'}")
            else:
                print(f"错误: 账号 {account['username']} 创建失败")
        
        # 关闭连接
        cursor.close()
        conn.close()
        
        print("\n===== 管理员账号创建完成 =====")
        print("\n管理员账号信息:")
        print("1. 超级管理员 (superadmin): 密码 123456 - 拥有全部权限")
        print("2. 全域驾驶舱管理员 (dashboard_admin): 密码 123456 - 仅全域驾驶舱权限")
        print("3. 供需罗盘管理员 (compass_admin): 密码 123456 - 仅供需罗盘权限")
        print("4. 智投魔方管理员 (cube_admin): 密码 123456 - 仅智投魔方权限")
        print("\n请确保应用已重启，然后尝试使用上述账号登录")
        
        return True
    
    except Exception as e:
        print(f"创建管理员账号时出错: {str(e)}")
        traceback.print_exc()
        return False

if __name__ == '__main__':
    create_admin_accounts() 