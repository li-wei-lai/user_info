from info_user.main import app, db, UserInfo, User
from flask import request, url_for
from flask_login import login_user

def test_admin_permissions():
    with app.app_context():
        try:
            # 获取所有管理员账户
            admins = User.query.all()
            print(f'找到 {len(admins)} 个管理员账户')
            
            # 获取所有用户信息
            users = UserInfo.query.all()
            print(f'找到 {len(users)} 个用户申请')
            
            # 统计每种服务类型的用户数量
            service_counts = {}
            for user in users:
                service_type = user.service_type or '未指定'
                if service_type in service_counts:
                    service_counts[service_type] += 1
                else:
                    service_counts[service_type] = 1
            
            print('\n用户申请服务类型统计:')
            for service_type, count in service_counts.items():
                print(f'{service_type}: {count} 个用户')
            
            # 测试每个管理员的权限
            print('\n测试管理员权限:')
            for admin in admins:
                print(f'\n管理员: {admin.username}')
                print(f'超级管理员: {admin.is_admin}')
                print(f'全域驾驶舱权限: {admin.dashboard_access}')
                print(f'供需罗盘权限: {admin.compass_access}')
                print(f'智投魔方权限: {admin.cube_access}')
                
                # 模拟该管理员登录
                login_user(admin)
                
                # 测试不同服务类型的过滤
                print('\n可访问的用户申请:')
                
                # 如果是超级管理员，可以看到所有用户
                if admin.is_admin:
                    print('超级管理员可以看到所有用户申请')
                    continue
                
                # 测试每种服务类型
                for service_type in ['dashboard', 'compass', 'cube']:
                    # 检查管理员是否有该服务类型的权限
                    has_access = False
                    if service_type == 'dashboard' and admin.dashboard_access:
                        has_access = True
                    elif service_type == 'compass' and admin.compass_access:
                        has_access = True
                    elif service_type == 'cube' and admin.cube_access:
                        has_access = True
                    
                    # 统计该服务类型的用户数量
                    count = sum(1 for user in users if user.service_type == service_type)
                    
                    if has_access:
                        print(f'- {service_type}: 可以看到 {count} 个用户申请')
                    else:
                        print(f'- {service_type}: 无权限查看')
            
            print('\n权限测试完成')
                
        except Exception as e:
            print(f'发生错误: {str(e)}')

if __name__ == '__main__':
    test_admin_permissions() 