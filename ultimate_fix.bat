@echo off
echo ===== 开始全面修复管理员账号和登录问题 =====
echo.

echo ===== 步骤1: 深度诊断 =====
python deep_diagnosis.py
echo.

echo ===== 步骤2: 修复登录表单 =====
python fix_login_form.py
echo.

echo ===== 步骤3: 检查登录页面 =====
python check_login_page.py
echo.

echo ===== 步骤4: 检查登录路由 =====
python check_login_route.py
echo.

echo ===== 步骤5: 更新User模型 =====
python update_user_model.py
echo.

echo ===== 步骤6: 添加删除用户路由 =====
python add_delete_user_route.py
echo.

echo ===== 步骤7: 创建并保护管理员账号 =====
python protect_admin_accounts.py
echo.

echo ===== 步骤8: 创建简单管理员账号 =====
python create_simple_admin.py
echo.

echo ===== 步骤9: 直接修改数据库 =====
python direct_db_fix.py
echo.

echo ===== 所有修复操作完成 =====
echo.
echo 请重启应用并尝试使用以下账号登录:
echo 1. 超级管理员: superadmin / 123456
echo 2. 全域驾驶舱管理员: dashboard_admin / 123456
echo 3. 供需罗盘管理员: compass_admin / 123456
echo 4. 智投魔方管理员: cube_admin / 123456
echo 5. 简单管理员: admin / 123456
echo.
echo 以上管理员账号已被保护，无法被删除。
echo.
echo 如果仍然无法登录，请检查:
echo 1. 数据库连接是否正常
echo 2. 应用是否正确重启
echo 3. 登录页面是否正确提交表单
echo 4. 浏览器缓存和Cookie是否已清除
echo.
echo 按任意键退出...
pause > nul 