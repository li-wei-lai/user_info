from info_user.main import app, db, User

with app.app_context():
    try:
        # 检查管理员账户
        admins = User.query.all()
        print('管理员账户总数:', len(admins))
        
        for admin in admins:
            print(f'ID: {admin.id}, 用户名: {admin.username}, 超级管理员: {admin.is_admin}')
            print(f'全域驾驶舱权限: {admin.dashboard_access}, 供需罗盘权限: {admin.compass_access}, 智投魔方权限: {admin.cube_access}')
            print('-' * 50)
    except Exception as e:
        print(f"发生错误: {str(e)}") 