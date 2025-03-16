from info_user.main import app, db, UserInfo, User

def check_users():
    with app.app_context():
        # 检查用户记录
        users = UserInfo.query.all()
        print('用户总数:', len(users))
        print('\n用户记录:')
        for user in users:
            print(f'ID: {user.id}, 姓名: {user.name}, 服务类型: {user.service_type}, 状态: {user.status}')

def check_admins():
    with app.app_context():
        # 检查管理员账户
        admins = User.query.all()
        print('\n管理员账户总数:', len(admins))
        print('\n管理员账户:')
        for admin in admins:
            print(f'ID: {admin.id}, 用户名: {admin.username}, 超级管理员: {admin.is_admin}, '
                  f'全域驾驶舱权限: {admin.dashboard_access}, 供需罗盘权限: {admin.compass_access}, 智投魔方权限: {admin.cube_access}')

if __name__ == '__main__':
    try:
        check_users()
        check_admins()
        print("\n检查完成")
    except Exception as e:
        print(f"发生错误: {str(e)}") 