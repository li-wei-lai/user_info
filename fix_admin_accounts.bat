@echo off
echo ===== 检查数据库和用户 =====
python check_users.py
echo.

echo ===== 测试和修复登录验证 =====
python fix_login.py
echo.

echo ===== 创建简单管理员账号 =====
python create_simple_admin.py
echo.

echo ===== 所有操作完成 =====
echo 请尝试使用以下账号登录:
echo 1. 用户名: admin, 密码: 123456
echo.
echo 按任意键退出...
pause > nul 