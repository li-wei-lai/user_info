import sys
import os
from werkzeug.security import generate_password_hash, check_password_hash

# 导入应用配置
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from info_user.main import app, db, User

def test_login(username, password):
    """测试登录功能"""
    with app.app_context():
        # 查找用户
        user = User.query.filter_by(username=username).first()
        
        if not user:
            print(f"用户 '{username}' 不存在")
            return False
        
        # 测试密码验证
        if user.check_password(password):
            print(f"用户 '{username}' 密码验证成功")
            return True
        else:
            print(f"用户 '{username}' 密码验证失败")
            # 打印密码哈希以便调试
            print(f"存储的密码哈希: {user.password_hash}")
            return False

def reset_admin_password(username, new_password):
    """重置管理员密码"""
    with app.app_context():
        # 查找用户
        user = User.query.filter_by(username=username).first()
        
        if not user:
            print(f"用户 '{username}' 不存在")
            return False
        
        # 重置密码
        user.set_password(new_password)
        db.session.commit()
        print(f"用户 '{username}' 密码已重置为 '{new_password}'")
        return True

def create_admin_if_not_exists():
    """如果不存在管理员账号，则创建一个"""
    with app.app_context():
        # 检查是否有任何用户
        user_count = User.query.count()
        
        if user_count == 0:
            # 创建超级管理员
            admin = User(
                username="admin",
                is_admin=True,
                dashboard_access=True,
                compass_access=True,
                cube_access=True
            )
            admin.set_password("admin123")
            db.session.add(admin)
            db.session.commit()
            print("创建了默认管理员账号: admin / admin123")

if __name__ == '__main__':
    # 确保至少有一个管理员账号
    create_admin_if_not_exists()
    
    # 测试超级管理员登录
    test_login("superadmin", "Admin@123")
    
    # 如果登录失败，重置密码
    reset_admin_password("superadmin", "Admin@123")
    
    # 再次测试登录
    test_login("superadmin", "Admin@123")
    
    # 如果仍然失败，尝试使用默认管理员
    test_login("admin", "admin123") 