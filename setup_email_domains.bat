@echo off
echo ===== 系统域名配置与邮件测试 =====
echo.

echo 步骤1: 更新系统域名配置...
python update_domains.py
echo.

echo 步骤2: 测试邮件发送...
python test_email.py
echo.

echo ===== 配置完成 =====
echo.
echo 现在系统将根据用户申请的系统类型，在邮件中提供不同的登录链接。
echo.
pause 