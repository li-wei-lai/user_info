@echo off
echo ===== 开始修复管理员权限问题 =====
echo.

echo 步骤1: 修复管理员权限...
python fix_admin_permissions.py
echo.

echo 步骤2: 验证修复结果...
python verify_fix.py
echo.

echo ===== 修复完成 =====
echo.
echo 现在每个系统的管理员只能看到自己系统的用户申请。
echo 请重启应用程序以使更改生效。
echo.
pause 