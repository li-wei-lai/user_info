import sys
import os
from pprint import pprint

# 导入应用配置
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from info_user.main import app, db, User

def check_database_connection():
    try:
        with app.app_context():
            # 测试数据库连接
            db.engine.connect()
            print("数据库连接成功！")
            return True
    except Exception as e:
        print(f"数据库连接失败: {str(e)}")
        return False

def list_all_users():
    if not check_database_connection():
        return
    
    with app.app_context():
        try:
            # 获取所有用户
            users = User.query.all()
            
            if not users:
                print("数据库中没有用户记录")
                return
            
            print(f"共找到 {len(users)} 个用户:")
            for user in users:
                print(f"\n用户ID: {user.id}")
                print(f"用户名: {user.username}")
                print(f"是否超级管理员: {user.is_admin}")
                print(f"全域驾驶舱权限: {user.dashboard_access}")
                print(f"供需罗盘权限: {user.compass_access}")
                print(f"智投魔方权限: {user.cube_access}")
                print("-" * 30)
        except Exception as e:
            print(f"查询用户失败: {str(e)}")

if __name__ == '__main__':
    list_all_users() 