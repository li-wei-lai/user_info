from info_user.main import app, db, UserInfo

def check_user_services():
    with app.app_context():
        try:
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
            
            # 列出每个服务类型的用户
            print('\n各服务类型的用户:')
            for service_type in sorted(service_counts.keys()):
                print(f'\n{service_type} 服务类型的用户:')
                service_users = [user for user in users if user.service_type == service_type]
                for user in service_users:
                    print(f'ID: {user.id}, 姓名: {user.name}, 状态: {user.status}')
                
        except Exception as e:
            print(f'发生错误: {str(e)}')

if __name__ == '__main__':
    check_user_services() 