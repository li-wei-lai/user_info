from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
import sys
import os

# 导入应用配置
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from info_user.main import app, db, User

# 定义管理员信息
ADMIN_USERNAME = 'superadmin'
ADMIN_PASSWORD = 'Admin@123'  # 强密码，包含大小写字母和数字

def create_superadmin():
    with app.app_context():
        # 检查用户是否已存在
        existing_user = User.query.filter_by(username=ADMIN_USERNAME).first()
        if existing_user:
            print(f"管理员 '{ADMIN_USERNAME}' 已存在，更新其密码和权限")
            existing_user.set_password(ADMIN_PASSWORD)
            existing_user.is_admin = True
            existing_user.dashboard_access = True
            existing_user.compass_access = True
            existing_user.cube_access = True
            db.session.commit()
        else:
            # 创建新的超级管理员
            admin = User(
                username=ADMIN_USERNAME,
                is_admin=True,
                dashboard_access=True,
                compass_access=True,
                cube_access=True
            )
            admin.set_password(ADMIN_PASSWORD)
            db.session.add(admin)
            db.session.commit()
            print(f"超级管理员 '{ADMIN_USERNAME}' 创建成功")
        
        print(f"管理员用户名: {ADMIN_USERNAME}")
        print(f"管理员密码: {ADMIN_PASSWORD}")
        print("该管理员拥有所有系统的访问权限")

if __name__ == '__main__':
    create_superadmin() 