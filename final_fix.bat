@echo off
echo ===== 开始修复管理员账号问题 =====
echo.

echo ===== 步骤1: 检查数据库和用户 =====
python check_users.py
echo.

echo ===== 步骤2: 测试和修复登录验证 =====
python fix_login.py
echo.

echo ===== 步骤3: 创建简单管理员账号 =====
python create_simple_admin.py
echo.

echo ===== 步骤4: 直接修改数据库 =====
python direct_db_fix.py
echo.

echo ===== 所有修复操作完成 =====
echo.
echo 请尝试使用以下账号登录:
echo 1. 用户名: admin, 密码: 123456
echo.
echo 如果仍然无法登录，请检查:
echo 1. 数据库连接是否正常
echo 2. 应用是否正确重启
echo 3. 登录页面是否正确提交表单
echo.
echo 按任意键退出...
pause > nul 