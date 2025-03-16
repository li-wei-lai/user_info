import sys
import os
import traceback
from datetime import datetime
from flask_mail import Message
from info_user.main import app, mail, UserInfo

def test_email_template():
    """测试邮件模板和发送功能"""
    print("\n===== 测试邮件模板和发送功能 =====")
    
    # 显示当前配置
    print(f"邮件服务器: {app.config['MAIL_SERVER']}")
    print(f"邮件端口: {app.config['MAIL_PORT']}")
    print(f"使用SSL: {app.config['MAIL_USE_SSL']}")
    print(f"使用TLS: {app.config['MAIL_USE_TLS']}")
    print(f"用户名: {app.config['MAIL_USERNAME']}")
    print(f"默认发件人: {app.config['MAIL_DEFAULT_SENDER']}")
    
    # 测试收件人
    test_recipient = input("请输入测试收件人邮箱: ")
    if not test_recipient:
        print("❌ 未提供测试收件人，跳过邮件测试")
        return
    
    # 创建测试用户数据
    test_user = UserInfo(
        name="测试用户",
        email=test_recipient,
        phone="13800138000",
        password="已加密的密码",
        original_password="test123456",
        message="这是一条测试消息",
        user_type="external",
        service_type="dashboard",
        brand_external="测试品牌",
        created_at=datetime.now()
    )
    
    # 选择邮件类型
    print("\n请选择要测试的邮件类型:")
    print("1. 审核通过邮件")
    print("2. 审核拒绝邮件")
    
    choice = input("\n请输入选项 [1-2]: ")
    
    with app.app_context():
        try:
            if choice == '1':
                # 测试审核通过邮件
                msg = Message(
                    subject='[测试] 您的信息已通过审核',
                    recipients=[test_recipient]
                )
                msg.html = app.jinja_env.get_template('email/approval_notification.html').render(
                    user=test_user,
                    now=datetime.now()
                )
                print("正在发送审核通过邮件...")
            elif choice == '2':
                # 测试审核拒绝邮件
                msg = Message(
                    subject='[测试] 您的申请未通过审核',
                    recipients=[test_recipient]
                )
                msg.html = app.jinja_env.get_template('email/rejection_notification.html').render(
                    user=test_user,
                    now=datetime.now()
                )
                print("正在发送审核拒绝邮件...")
            else:
                print("❌ 无效选项，退出程序")
                return
            
            # 发送邮件
            mail.send(msg)
            print("✅ 测试邮件发送成功!")
            print(f"请检查邮箱 {test_recipient} 查看邮件内容")
            
        except Exception as e:
            print(f"❌ 邮件发送失败: {str(e)}")
            traceback.print_exc()
            
            # 提供可能的解决方案
            print("\n可能的原因:")
            if "authentication" in str(e).lower() or "login" in str(e).lower():
                print("1. 邮箱用户名或密码错误")
                print("2. 邮箱安全设置不允许第三方应用登录")
                print("\n解决方案:")
                print("1. 检查邮箱用户名和密码")
                print("2. 在邮箱设置中启用SMTP服务和第三方应用访问")
                print("3. 使用应用专用密码而不是账户密码")
                print("4. 运行 python fix_email.py 修复邮件配置")
            elif "ssl" in str(e).lower() or "tls" in str(e).lower():
                print("1. SSL/TLS配置错误")
                print("\n解决方案:")
                print("1. 检查MAIL_USE_SSL和MAIL_USE_TLS设置")
                print("2. 确认邮件服务器端口是否正确")
                print("3. 运行 python fix_email.py 修复邮件配置")
            elif "timeout" in str(e).lower() or "connect" in str(e).lower():
                print("1. 网络连接问题")
                print("2. 邮件服务器无法访问")
                print("\n解决方案:")
                print("1. 检查网络连接")
                print("2. 确认服务器可以访问外部网络")
                print("3. 确认邮件服务器地址是否正确")
                print("4. 运行 python fix_email.py 修复邮件配置")

if __name__ == "__main__":
    test_email_template() 