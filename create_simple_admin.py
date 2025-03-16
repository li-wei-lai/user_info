import sys
import os
from werkzeug.security import generate_password_hash

# 导入应用配置
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from info_user.main import app, db, User

def create_simple_admin():
    """创建一个简单的管理员账号"""
    with app.app_context():
        # 定义简单的管理员信息
        username = "admin"
        password = "123456"
        
        # 检查用户是否已存在
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            print(f"管理员 '{username}' 已存在，更新其密码和权限")
            existing_user.password_hash = generate_password_hash(password)  # 直接设置密码哈希
            existing_user.is_admin = True
            existing_user.dashboard_access = True
            existing_user.compass_access = True
            existing_user.cube_access = True
            db.session.commit()
        else:
            # 创建新的管理员
            admin = User(
                username=username,
                password_hash=generate_password_hash(password),  # 直接设置密码哈希
                is_admin=True,
                dashboard_access=True,
                compass_access=True,
                cube_access=True
            )
            db.session.add(admin)
            db.session.commit()
            print(f"管理员 '{username}' 创建成功")
        
        print(f"管理员用户名: {username}")
        print(f"管理员密码: {password}")
        print("该管理员拥有所有系统的访问权限")
        
        # 验证密码哈希是否正确设置
        admin = User.query.filter_by(username=username).first()
        print(f"密码哈希: {admin.password_hash}")
        
        # 测试密码验证
        from werkzeug.security import check_password_hash
        if check_password_hash(admin.password_hash, password):
            print("密码验证成功")
        else:
            print("密码验证失败")

if __name__ == '__main__':
    create_simple_admin() 