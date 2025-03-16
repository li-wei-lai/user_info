from info_user.main import app, db, UserInfo, send_approval_email, send_rejection_email
from info_user.config import SYSTEM_DOMAINS, SYSTEM_NAMES

def test_email():
    with app.app_context():
        try:
            # 打印系统配置
            print("系统域名配置:")
            for service_type, domain in SYSTEM_DOMAINS.items():
                print(f"  {SYSTEM_NAMES[service_type]}: {domain}")
            print()
            
            # 获取所有用户
            users = UserInfo.query.all()
            if not users:
                print("数据库中没有用户记录")
                return
            
            # 按服务类型分组用户
            users_by_service = {}
            for user in users:
                service_type = user.service_type or '未指定'
                if service_type not in users_by_service:
                    users_by_service[service_type] = []
                users_by_service[service_type].append(user)
            
            # 打印用户分组
            print("用户按服务类型分组:")
            for service_type, service_users in users_by_service.items():
                system_name = SYSTEM_NAMES.get(service_type, '未知系统')
                print(f"  {system_name}: {len(service_users)} 个用户")
            print()
            
            # 选择测试用户
            test_email = input("请输入测试邮箱地址: ")
            
            # 为每种服务类型选择一个用户进行测试
            for service_type, service_users in users_by_service.items():
                if service_type in SYSTEM_DOMAINS:  # 只测试已配置域名的服务类型
                    test_user = service_users[0]
                    
                    # 修改测试用户的邮箱
                    original_email = test_user.email
                    test_user.email = test_email
                    
                    # 测试发送审批通知邮件
                    print(f"测试发送 {SYSTEM_NAMES.get(service_type, '未知系统')} 审批通知邮件...")
                    send_approval_email(test_user)
                    
                    # 测试发送拒绝通知邮件
                    print(f"测试发送 {SYSTEM_NAMES.get(service_type, '未知系统')} 拒绝通知邮件...")
                    send_rejection_email(test_user)
                    
                    # 恢复原始邮箱
                    test_user.email = original_email
            
            print("\n测试完成，请检查邮箱")
            
        except Exception as e:
            print(f"测试失败: {str(e)}")

if __name__ == '__main__':
    test_email() 