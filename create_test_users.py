from info_user.main import app, db, UserInfo
from werkzeug.security import generate_password_hash
from datetime import datetime

def create_test_users():
    with app.app_context():
        try:
            # 创建不同服务类型的测试用户
            test_users = [
                {
                    'name': '测试用户1',
                    'email': 'test1@example.com',
                    'phone': '13800000001',
                    'password': '123456',
                    'message': '这是一个全域驾驶舱测试用户',
                    'user_type': 'internal',
                    'service_type': 'dashboard',
                    'department': '测试部门',
                    'position': '测试职位',
                    'brands': '["品牌1", "品牌2"]'
                },
                {
                    'name': '测试用户2',
                    'email': 'test2@example.com',
                    'phone': '13800000002',
                    'password': '123456',
                    'message': '这是一个供需罗盘测试用户',
                    'user_type': 'internal',
                    'service_type': 'compass',
                    'department': '测试部门',
                    'position': '测试职位',
                    'brands': '["品牌1", "品牌2"]'
                },
                {
                    'name': '测试用户3',
                    'email': 'test3@example.com',
                    'phone': '13800000003',
                    'password': '123456',
                    'message': '这是一个智投魔方测试用户',
                    'user_type': 'internal',
                    'service_type': 'cube',
                    'department': '测试部门',
                    'position': '测试职位',
                    'brands': '["品牌1", "品牌2"]'
                }
            ]
            
            # 添加测试用户
            for user_data in test_users:
                # 检查是否已存在相同邮箱的用户
                existing_user = UserInfo.query.filter_by(email=user_data['email']).first()
                if existing_user:
                    print(f"用户 {user_data['name']} ({user_data['email']}) 已存在，跳过")
                    continue
                
                # 创建新用户
                new_user = UserInfo(
                    name=user_data['name'],
                    email=user_data['email'],
                    phone=user_data['phone'],
                    password=generate_password_hash(user_data['password']),
                    original_password=user_data['password'],
                    message=user_data['message'],
                    user_type=user_data['user_type'],
                    service_type=user_data['service_type'],
                    department=user_data.get('department'),
                    position=user_data.get('position'),
                    brands=user_data.get('brands'),
                    brand_external=user_data.get('brand_external'),
                    created_at=datetime.utcnow(),
                    status='pending'
                )
                
                db.session.add(new_user)
                print(f"添加用户 {user_data['name']} ({user_data['email']}) - 服务类型: {user_data['service_type']}")
            
            # 提交更改
            db.session.commit()
            print('测试用户创建完成')
            
        except Exception as e:
            db.session.rollback()
            print(f'发生错误: {str(e)}')

if __name__ == '__main__':
    create_test_users() 