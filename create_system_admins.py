from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
import sys
import os

# 导入应用配置
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from info_user.main import app, db, User

# 定义各系统管理员信息
SYSTEM_ADMINS = [
    {
        'username': 'dashboard_admin',
        'password': 'Dashboard@123',
        'is_admin': False,
        'dashboard_access': True,
        'compass_access': False,
        'cube_access': False,
        'description': '全域驾驶舱管理员'
    },
    {
        'username': 'compass_admin',
        'password': 'Compass@123',
        'is_admin': False,
        'dashboard_access': False,
        'compass_access': True,
        'cube_access': False,
        'description': '供需罗盘管理员'
    },
    {
        'username': 'cube_admin',
        'password': 'Cube@123',
        'is_admin': False,
        'dashboard_access': False,
        'compass_access': False,
        'cube_access': True,
        'description': '智投魔方管理员'
    }
]

def create_system_admins():
    with app.app_context():
        for admin_info in SYSTEM_ADMINS:
            username = admin_info['username']
            password = admin_info['password']
            
            # 检查用户是否已存在
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                print(f"管理员 '{username}' 已存在，更新其密码和权限")
                existing_user.set_password(password)
                existing_user.is_admin = admin_info['is_admin']
                existing_user.dashboard_access = admin_info['dashboard_access']
                existing_user.compass_access = admin_info['compass_access']
                existing_user.cube_access = admin_info['cube_access']
                db.session.commit()
            else:
                # 创建新的管理员
                admin = User(
                    username=username,
                    is_admin=admin_info['is_admin'],
                    dashboard_access=admin_info['dashboard_access'],
                    compass_access=admin_info['compass_access'],
                    cube_access=admin_info['cube_access']
                )
                admin.set_password(password)
                db.session.add(admin)
                db.session.commit()
                print(f"{admin_info['description']} '{username}' 创建成功")
            
            print(f"管理员用户名: {username}")
            print(f"管理员密码: {password}")
            print(f"权限: {admin_info['description']}")
            print("----------------------------")

if __name__ == '__main__':
    create_system_admins() 