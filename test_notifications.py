import sys
import os
import json
import requests
import traceback
from datetime import datetime
from flask_mail import Message
from info_user.main import app, mail, DINGTALK_WEBHOOK

def test_dingtalk_notification():
    """测试钉钉通知功能"""
    print("\n===== 测试钉钉通知 =====")
    
    # 显示当前配置
    print(f"当前钉钉Webhook: {DINGTALK_WEBHOOK}")
    
    # 构建测试消息
    title = "测试通知"
    content = f"""
### 测试钉钉通知
- **时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **来源**: 测试脚本
- **目的**: 验证钉钉通知功能是否正常工作
    """
    
    headers = {
        "Content-Type": "application/json"
    }
    message = {
        "msgtype": "markdown",
        "markdown": {
            "title": title,
            "text": content
        }
    }
    
    try:
        # 发送请求
        print("正在发送钉钉通知...")
        response = requests.post(DINGTALK_WEBHOOK, headers=headers, data=json.dumps(message), timeout=10)
        
        # 检查响应
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        response_data = response.json()
        if response.status_code == 200 and response_data.get('errcode') == 0:
            print("✅ 钉钉通知发送成功!")
        else:
            print(f"❌ 钉钉通知发送失败: {response_data.get('errmsg', '未知错误')}")
            
            # 提供可能的解决方案
            if "token" in response_data.get('errmsg', ''):
                print("\n可能的原因:")
                print("1. access_token已过期或无效")
                print("2. 机器人已被禁用或删除")
                print("\n解决方案:")
                print("1. 登录钉钉管理后台，重新创建或更新机器人")
                print("2. 更新代码中的DINGTALK_WEBHOOK值")
            elif "ip" in response_data.get('errmsg', ''):
                print("\n可能的原因: 服务器IP不在钉钉机器人的白名单中")
                print("\n解决方案: 在钉钉机器人安全设置中添加服务器IP到白名单")
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求异常: {str(e)}")
        print("\n可能的原因:")
        print("1. 网络连接问题")
        print("2. 钉钉服务器无法访问")
        print("\n解决方案:")
        print("1. 检查网络连接")
        print("2. 确认服务器可以访问外部网络")
    except Exception as e:
        print(f"❌ 未知异常: {str(e)}")
        traceback.print_exc()

def test_email_sending():
    """测试邮件发送功能"""
    print("\n===== 测试邮件发送 =====")
    
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
    
    with app.app_context():
        try:
            # 构建测试邮件
            msg = Message(
                subject='测试邮件 - 信息审核系统',
                recipients=[test_recipient]
            )
            msg.html = f"""
            <h1>测试邮件</h1>
            <p>这是一封测试邮件，用于验证邮件发送功能是否正常工作。</p>
            <p>发送时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            """
            
            # 发送邮件
            print(f"正在发送测试邮件到 {test_recipient}...")
            mail.send(msg)
            print("✅ 测试邮件发送成功!")
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
            elif "ssl" in str(e).lower() or "tls" in str(e).lower():
                print("1. SSL/TLS配置错误")
                print("\n解决方案:")
                print("1. 检查MAIL_USE_SSL和MAIL_USE_TLS设置")
                print("2. 确认邮件服务器端口是否正确")
            elif "timeout" in str(e).lower() or "connect" in str(e).lower():
                print("1. 网络连接问题")
                print("2. 邮件服务器无法访问")
                print("\n解决方案:")
                print("1. 检查网络连接")
                print("2. 确认服务器可以访问外部网络")
                print("3. 确认邮件服务器地址是否正确")

def update_dingtalk_webhook():
    """更新钉钉Webhook配置"""
    print("\n===== 更新钉钉Webhook =====")
    
    new_webhook = input("请输入新的钉钉Webhook URL: ")
    if not new_webhook:
        print("❌ 未提供新的Webhook，跳过更新")
        return
    
    try:
        # 读取main.py文件
        with open('info_user/main.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替换Webhook
        import re
        pattern = r'DINGTALK_WEBHOOK = "([^"]+)"'
        if re.search(pattern, content):
            new_content = re.sub(pattern, f'DINGTALK_WEBHOOK = "{new_webhook}"', content)
            
            # 写回文件
            with open('info_user/main.py', 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print("✅ 钉钉Webhook已更新!")
        else:
            print("❌ 未找到DINGTALK_WEBHOOK配置行")
    except Exception as e:
        print(f"❌ 更新Webhook失败: {str(e)}")
        traceback.print_exc()

def update_email_config():
    """更新邮件配置"""
    print("\n===== 更新邮件配置 =====")
    
    print("请输入新的邮件配置（留空则保持不变）:")
    mail_server = input(f"邮件服务器 [{app.config['MAIL_SERVER']}]: ") or app.config['MAIL_SERVER']
    mail_port = input(f"邮件端口 [{app.config['MAIL_PORT']}]: ") or app.config['MAIL_PORT']
    mail_username = input(f"用户名 [{app.config['MAIL_USERNAME']}]: ") or app.config['MAIL_USERNAME']
    mail_password = input("密码 [输入新密码或留空]: ")
    
    try:
        # 读取main.py文件
        with open('info_user/main.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替换配置
        import re
        if mail_server != app.config['MAIL_SERVER']:
            pattern = r"app\.config\['MAIL_SERVER'\] = '([^']+)'"
            content = re.sub(pattern, f"app.config['MAIL_SERVER'] = '{mail_server}'", content)
        
        if str(mail_port) != str(app.config['MAIL_PORT']):
            pattern = r"app\.config\['MAIL_PORT'\] = (\d+)"
            content = re.sub(pattern, f"app.config['MAIL_PORT'] = {mail_port}", content)
        
        if mail_username != app.config['MAIL_USERNAME']:
            pattern = r"app\.config\['MAIL_USERNAME'\] = '([^']+)'"
            content = re.sub(pattern, f"app.config['MAIL_USERNAME'] = '{mail_username}'", content)
        
        if mail_password:
            pattern = r"app\.config\['MAIL_PASSWORD'\] = os\.environ\.get\('MAIL_PASSWORD', '([^']+)'\)"
            content = re.sub(pattern, f"app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', '{mail_password}')", content)
        
        # 写回文件
        with open('info_user/main.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ 邮件配置已更新!")
    except Exception as e:
        print(f"❌ 更新邮件配置失败: {str(e)}")
        traceback.print_exc()

def main():
    print("===== 通知功能诊断工具 =====")
    print("此工具将帮助您诊断和修复钉钉通知和邮件发送问题")
    
    while True:
        print("\n请选择操作:")
        print("1. 测试钉钉通知")
        print("2. 测试邮件发送")
        print("3. 更新钉钉Webhook")
        print("4. 更新邮件配置")
        print("0. 退出")
        
        choice = input("\n请输入选项 [0-4]: ")
        
        if choice == '1':
            test_dingtalk_notification()
        elif choice == '2':
            test_email_sending()
        elif choice == '3':
            update_dingtalk_webhook()
        elif choice == '4':
            update_email_config()
        elif choice == '0':
            print("退出程序")
            break
        else:
            print("无效选项，请重新输入")

if __name__ == '__main__':
    main() 