from info_user.main import app, db, User

def fix_admin_permissions():
    with app.app_context():
        try:
            # 获取所有管理员账户
            admins = User.query.all()
            print(f'找到 {len(admins)} 个管理员账户')
            
            # 修复权限
            for admin in admins:
                print(f'处理账户: {admin.username}')
                
                # 根据用户名设置正确的权限
                if admin.username == 'superadmin':
                    admin.is_admin = True
                    admin.dashboard_access = True
                    admin.compass_access = True
                    admin.cube_access = True
                    print(f'  设置 {admin.username} 为超级管理员，拥有所有权限')
                elif admin.username == 'dashboard_admin':
                    admin.is_admin = False
                    admin.dashboard_access = True
                    admin.compass_access = False
                    admin.cube_access = False
                    print(f'  设置 {admin.username} 只有全域驾驶舱权限')
                elif admin.username == 'compass_admin':
                    admin.is_admin = False
                    admin.dashboard_access = False
                    admin.compass_access = True
                    admin.cube_access = False
                    print(f'  设置 {admin.username} 只有供需罗盘权限')
                elif admin.username == 'cube_admin':
                    admin.is_admin = False
                    admin.dashboard_access = False
                    admin.compass_access = False
                    admin.cube_access = True
                    print(f'  设置 {admin.username} 只有智投魔方权限')
                elif admin.username == 'admin':
                    admin.is_admin = True
                    admin.dashboard_access = True
                    admin.compass_access = True
                    admin.cube_access = True
                    print(f'  设置 {admin.username} 为超级管理员，拥有所有权限')
                else:
                    print(f'  保持 {admin.username} 的现有权限不变')
            
            # 提交更改
            db.session.commit()
            print('管理员权限修复完成')
            
            # 验证更改
            print('\n验证权限设置:')
            for admin in User.query.all():
                print(f'ID: {admin.id}, 用户名: {admin.username}, 超级管理员: {admin.is_admin}')
                print(f'全域驾驶舱权限: {admin.dashboard_access}, 供需罗盘权限: {admin.compass_access}, 智投魔方权限: {admin.cube_access}')
                print('-' * 50)
                
        except Exception as e:
            db.session.rollback()
            print(f'发生错误: {str(e)}')

if __name__ == '__main__':
    fix_admin_permissions() 