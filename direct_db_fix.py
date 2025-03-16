import sys
import os
from werkzeug.security import generate_password_hash
import pymysql

def direct_db_fix():
    """直接修改数据库中的管理员账号"""
    try:
        # 数据库连接信息
        db_config = {
            'host': 'rm-uf6d863v517727p6mdo.mysql.rds.aliyuncs.com',
            'user': 'heyin_data_jony',
            'password': 'Jony_123',
            'database': 'test_db',
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor
        }
        
        # 连接数据库
        conn = pymysql.connect(**db_config)
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
                `is_admin` BOOLEAN DEFAULT FALSE,
                `dashboard_access` BOOLEAN DEFAULT FALSE,
                `compass_access` BOOLEAN DEFAULT FALSE,
                `cube_access` BOOLEAN DEFAULT FALSE
            )
            """)
            conn.commit()
        
        # 检查是否存在admin用户
        cursor.execute("SELECT * FROM user WHERE username = 'admin'")
        admin = cursor.fetchone()
        
        # 生成密码哈希
        password_hash = generate_password_hash('123456')
        
        if admin:
            # 更新admin用户
            cursor.execute("""
            UPDATE user 
            SET password_hash = %s, is_admin = 1, 
                dashboard_access = 1, compass_access = 1, cube_access = 1
            WHERE username = 'admin'
            """, (password_hash,))
            print("更新admin用户成功")
        else:
            # 创建admin用户
            cursor.execute("""
            INSERT INTO user (username, password_hash, is_admin, dashboard_access, compass_access, cube_access)
            VALUES ('admin', %s, 1, 1, 1, 1)
            """, (password_hash,))
            print("创建admin用户成功")
        
        # 提交更改
        conn.commit()
        
        # 验证用户是否创建成功
        cursor.execute("SELECT * FROM user WHERE username = 'admin'")
        admin = cursor.fetchone()
        if admin:
            print("admin用户存在于数据库中")
            print(f"ID: {admin['id']}")
            print(f"用户名: {admin['username']}")
            print(f"密码哈希: {admin['password_hash']}")
            print(f"是否超级管理员: {admin['is_admin']}")
        else:
            print("admin用户创建失败")
        
        # 关闭连接
        cursor.close()
        conn.close()
        
        print("\n请使用以下账号登录:")
        print("用户名: admin")
        print("密码: 123456")
        
    except Exception as e:
        print(f"直接修改数据库失败: {str(e)}")

if __name__ == '__main__':
    direct_db_fix() 