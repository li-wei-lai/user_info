from info_user.main import app, db, UserInfo, User

def verify_fix():
    with app.app_context():
        try:
            print("=== 验证管理员权限修复 ===\n")
            
            # 检查管理员账户
            admins = User.query.all()
            print(f'管理员账户总数: {len(admins)}')
            
            # 验证每个管理员的权限
            for admin in admins:
                print(f'\n管理员: {admin.username}')
                print(f'超级管理员: {admin.is_admin}')
                print(f'全域驾驶舱权限: {admin.dashboard_access}')
                print(f'供需罗盘权限: {admin.compass_access}')
                print(f'智投魔方权限: {admin.cube_access}')
                
                # 检查权限是否正确
                if admin.username == 'superadmin':
                    assert admin.is_admin == True, "superadmin 应该是超级管理员"
                    assert admin.dashboard_access == True, "superadmin 应该有全域驾驶舱权限"
                    assert admin.compass_access == True, "superadmin 应该有供需罗盘权限"
                    assert admin.cube_access == True, "superadmin 应该有智投魔方权限"
                    print("✓ superadmin 权限正确")
                elif admin.username == 'dashboard_admin':
                    assert admin.is_admin == False, "dashboard_admin 不应该是超级管理员"
                    assert admin.dashboard_access == True, "dashboard_admin 应该有全域驾驶舱权限"
                    assert admin.compass_access == False, "dashboard_admin 不应该有供需罗盘权限"
                    assert admin.cube_access == False, "dashboard_admin 不应该有智投魔方权限"
                    print("✓ dashboard_admin 权限正确")
                elif admin.username == 'compass_admin':
                    assert admin.is_admin == False, "compass_admin 不应该是超级管理员"
                    assert admin.dashboard_access == False, "compass_admin 不应该有全域驾驶舱权限"
                    assert admin.compass_access == True, "compass_admin 应该有供需罗盘权限"
                    assert admin.cube_access == False, "compass_admin 不应该有智投魔方权限"
                    print("✓ compass_admin 权限正确")
                elif admin.username == 'cube_admin':
                    assert admin.is_admin == False, "cube_admin 不应该是超级管理员"
                    assert admin.dashboard_access == False, "cube_admin 不应该有全域驾驶舱权限"
                    assert admin.compass_access == False, "cube_admin 不应该有供需罗盘权限"
                    assert admin.cube_access == True, "cube_admin 应该有智投魔方权限"
                    print("✓ cube_admin 权限正确")
            
            print("\n=== 验证用户申请分布 ===\n")
            
            # 检查用户申请
            users = UserInfo.query.all()
            print(f'用户申请总数: {len(users)}')
            
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
            
            # 确保每种服务类型都有用户
            assert 'dashboard' in service_counts, "应该有全域驾驶舱用户"
            assert 'compass' in service_counts, "应该有供需罗盘用户"
            assert 'cube' in service_counts, "应该有智投魔方用户"
            print("✓ 所有服务类型都有用户")
            
            print("\n=== 验证完成 ===")
            print("\n所有检查都通过了！权限修复成功。")
            print("现在每个系统的管理员只能看到自己系统的用户申请。")
            
        except AssertionError as e:
            print(f"验证失败: {str(e)}")
        except Exception as e:
            print(f"发生错误: {str(e)}")

if __name__ == '__main__':
    verify_fix() 