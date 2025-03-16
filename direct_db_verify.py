import sys
import os
import traceback
import pymysql
from werkzeug.security import check_password_hash, generate_password_hash

def direct_db_verify():
    print("===== 直接验证数据库中的用户账号 =====")
    
    try:
        # 数据库连接信息 - 使用应用中的实际配置
        db_host = 'rm-uf6d863v517727p6mdo.mysql.rds.aliyuncs.com'
        db_user = 'heyin_data_jony'
        db_pass = 'Jony_123'
        db_name = 'test_db'
        
        print(f"尝试连接数据库: {db_user}@{db_host}/{db_name}")
        
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
            
            # 尝试不指定数据库名称连接
            try:
                conn = pymysql.connect(
                    host=db_host,
                    user=db_user,
                    password=db_pass,
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor
                )
                print("成功连接到MySQL服务器，但未指定数据库")
                
                # 检查数据库是否存在
                cursor = conn.cursor()
                cursor.execute("SHOW DATABASES")
                databases = [db['Database'] for db in cursor.fetchall()]
                print(f"可用的数据库: {', '.join(databases)}")
                
                if db_name in databases:
                    print(f"数据库 {db_name} 存在，尝试使用它")
                    cursor.execute(f"USE {db_name}")
                else:
                    print(f"错误: 数据库 {db_name} 不存在")
                    return False
            except Exception as e2:
                print(f"连接MySQL服务器失败: {str(e2)}")
                traceback.print_exc()
                return False
        
        cursor = conn.cursor()
        
        # 检查user表是否存在
        cursor.execute("SHOW TABLES LIKE 'user'")
        if not cursor.fetchone():
            print("错误: user表不存在")
            
            # 列出所有表
            cursor.execute("SHOW TABLES")
            tables = [list(table.values())[0] for table in cursor.fetchall()]
            print(f"数据库中的表: {', '.join(tables)}")
            
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
            
            # 打印所有字段
            for key, value in user.items():
                if key not in ['id', 'username', 'password_hash']:
                    print(f"  {key}: {value}")
            
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
        
        # 列出所有用户
        cursor.execute("SELECT username FROM `user`")
        all_users = [user['username'] for user in cursor.fetchall()]
        print(f"\n数据库中的所有用户: {', '.join(all_users)}")
        
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
        
        # 获取表结构
        cursor.execute("DESCRIBE `user`")
        columns = [column['Field'] for column in cursor.fetchall()]
        print(f"user表的列: {', '.join(columns)}")
        
        # 创建新的测试账号
        password_hash = generate_password_hash(test_password)
        
        # 根据表结构动态构建SQL
        fields = []
        values = []
        placeholders = []
        
        # 基本字段
        base_fields = {
            'username': test_username,
            'password_hash': password_hash
        }
        
        # 权限字段
        permission_fields = {
            'is_admin': True,
            'is_super_admin': True,
            'dashboard_access': True,
            'compass_access': True,
            'cube_access': True,
            'protected': True
        }
        
        # 合并所有字段
        all_fields = {**base_fields, **permission_fields}
        
        # 只使用表中存在的字段
        for field, value in all_fields.items():
            if field in columns:
                fields.append(f"`{field}`")
                values.append(value)
                placeholders.append("%s")
        
        # 构建SQL
        sql = f"INSERT INTO `user` ({', '.join(fields)}) VALUES ({', '.join(placeholders)})"
        
        # 执行SQL
        cursor.execute(sql, values)
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
        
        print("\n===== 验证完成 =====")
        print("\n可能的解决方案:")
        print("1. 所有管理员账号的密码已重置为: 123456")
        print("2. 尝试使用新创建的测试账号登录: test_login_user / test123")
        print("3. 确保应用已重启，并且正在使用正确的数据库")
        print("4. 检查浏览器缓存和Cookie，尝试清除后再登录")
        print("5. 检查应用日志，查看是否有错误信息")
        
        return True
    
    except Exception as e:
        print(f"验证过程中出错: {str(e)}")
        traceback.print_exc()
        return False

if __name__ == '__main__':
    direct_db_verify() 