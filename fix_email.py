import re
import traceback
from datetime import datetime
from flask_mail import Message

def test_email_config(app, mail, recipient):
    """测试邮件配置是否有效"""
    print(f"正在测试邮件发送到: {recipient}")
    
    with app.app_context():
        try:
            # 构建测试邮件
            msg = Message(
                subject='测试邮件 - 信息审核系统',
                recipients=[recipient]
            )
            msg.html = f"""
            <h1>测试邮件</h1>
            <p>这是一封测试邮件，用于验证邮件发送功能是否正常工作。</p>
            <p>发送时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            """
            
            # 发送邮件
            mail.send(msg)
            print("✅ 测试邮件发送成功!")
            return True
        except Exception as e:
            print(f"❌ 邮件发送失败: {str(e)}")
            traceback.print_exc()
            return False

def update_email_config_in_file(file_path, config):
    """更新文件中的邮件配置"""
    try:
        # 读取文件
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替换配置
        if 'server' in config:
            pattern = r"app\.config\['MAIL_SERVER'\] = '([^']+)'"
            content = re.sub(pattern, f"app.config['MAIL_SERVER'] = '{config['server']}'", content)
        
        if 'port' in config:
            pattern = r"app\.config\['MAIL_PORT'\] = (\d+)"
            content = re.sub(pattern, f"app.config['MAIL_PORT'] = {config['port']}", content)
        
        if 'use_ssl' in config:
            pattern = r"app\.config\['MAIL_USE_SSL'\] = (True|False)"
            content = re.sub(pattern, f"app.config['MAIL_USE_SSL'] = {config['use_ssl']}", content)
        
        if 'use_tls' in config:
            pattern = r"app\.config\['MAIL_USE_TLS'\] = (True|False)"
            content = re.sub(pattern, f"app.config['MAIL_USE_TLS'] = {config['use_tls']}", content)
        
        if 'username' in config:
            pattern = r"app\.config\['MAIL_USERNAME'\] = '([^']+)'"
            content = re.sub(pattern, f"app.config['MAIL_USERNAME'] = '{config['username']}'", content)
        
        if 'password' in config:
            pattern = r"app\.config\['MAIL_PASSWORD'\] = os\.environ\.get\('MAIL_PASSWORD', '([^']+)'\)"
            content = re.sub(pattern, f"app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', '{config['password']}')", content)
        
        if 'sender' in config:
            pattern = r"app\.config\['MAIL_DEFAULT_SENDER'\] = \('([^']+)', '([^']+)'\)"
            content = re.sub(pattern, f"app.config['MAIL_DEFAULT_SENDER'] = ('{config['sender_name']}', '{config['sender']}')", content)
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 已更新 {file_path} 中的邮件配置")
        return True
    except Exception as e:
        print(f"❌ 更新文件失败: {str(e)}")
        traceback.print_exc()
        return False

def get_common_email_configs():
    """获取常见邮件服务器配置"""
    return {
        "1": {
            "name": "阿里云企业邮箱",
            "server": "smtp.qiye.aliyun.com",
            "port": 465,
            "use_ssl": True,
            "use_tls": False
        },
        "2": {
            "name": "腾讯企业邮箱",
            "server": "smtp.exmail.qq.com",
            "port": 465,
            "use_ssl": True,
            "use_tls": False
        },
        "3": {
            "name": "腾讯QQ邮箱",
            "server": "smtp.qq.com",
            "port": 465,
            "use_ssl": True,
            "use_tls": False
        },
        "4": {
            "name": "网易163邮箱",
            "server": "smtp.163.com",
            "port": 465,
            "use_ssl": True,
            "use_tls": False
        },
        "5": {
            "name": "Gmail",
            "server": "smtp.gmail.com",
            "port": 587,
            "use_ssl": False,
            "use_tls": True
        },
        "6": {
            "name": "钉钉企业邮箱",
            "server": "smtp.dingtalk.com",
            "port": 465,
            "use_ssl": True,
            "use_tls": False
        }
    }

def main():
    print("===== 邮件发送修复工具 =====")
    
    # 导入应用和邮件配置
    try:
        from info_user.main import app, mail
        
        # 显示当前配置
        print("\n当前邮件配置:")
        print(f"服务器: {app.config['MAIL_SERVER']}")
        print(f"端口: {app.config['MAIL_PORT']}")
        print(f"使用SSL: {app.config['MAIL_USE_SSL']}")
        print(f"使用TLS: {app.config['MAIL_USE_TLS']}")
        print(f"用户名: {app.config['MAIL_USERNAME']}")
        print(f"默认发件人: {app.config['MAIL_DEFAULT_SENDER']}")
    except ImportError:
        print("❌ 无法导入应用配置，请确保在正确的目录中运行此脚本")
        return
    
    # 显示常见邮件服务器配置
    configs = get_common_email_configs()
    print("\n常见邮件服务器配置:")
    for key, config in configs.items():
        print(f"{key}. {config['name']} - {config['server']}:{config['port']} (SSL: {config['use_ssl']}, TLS: {config['use_tls']})")
    
    # 选择配置
    choice = input("\n请选择邮件服务器配置 [1-6] 或输入 'c' 自定义配置: ")
    
    new_config = {}
    if choice in configs:
        # 使用预设配置
        new_config.update(configs[choice])
        print(f"\n已选择 {new_config['name']} 配置")
    elif choice.lower() == 'c':
        # 自定义配置
        print("\n请输入自定义配置:")
        new_config['server'] = input("SMTP服务器地址: ")
        new_config['port'] = int(input("SMTP端口: "))
        new_config['use_ssl'] = input("使用SSL (y/n): ").lower() == 'y'
        new_config['use_tls'] = input("使用TLS (y/n): ").lower() == 'y'
    else:
        print("❌ 无效选择，退出程序")
        return
    
    # 输入邮箱账号信息
    new_config['username'] = input(f"\n邮箱用户名 [{app.config['MAIL_USERNAME']}]: ") or app.config['MAIL_USERNAME']
    new_config['password'] = input("邮箱密码或授权码: ")
    
    # 设置发件人信息
    sender_name, sender_email = app.config['MAIL_DEFAULT_SENDER']
    new_config['sender'] = input(f"发件人邮箱 [{sender_email}]: ") or sender_email
    new_config['sender_name'] = input(f"发件人名称 [{sender_name}]: ") or sender_name
    
    # 更新应用配置
    app.config['MAIL_SERVER'] = new_config['server']
    app.config['MAIL_PORT'] = new_config['port']
    app.config['MAIL_USE_SSL'] = new_config['use_ssl']
    app.config['MAIL_USE_TLS'] = new_config['use_tls']
    app.config['MAIL_USERNAME'] = new_config['username']
    app.config['MAIL_PASSWORD'] = new_config['password']
    app.config['MAIL_DEFAULT_SENDER'] = (new_config['sender_name'], new_config['sender'])
    
    # 测试新配置
    test_recipient = input("\n请输入测试收件人邮箱: ")
    if not test_recipient:
        print("❌ 未提供测试收件人，跳过测试")
    else:
        print("\n正在测试新的邮件配置...")
        if test_email_config(app, mail, test_recipient):
            # 更新配置文件
            file_path = 'info_user/main.py'
            if update_email_config_in_file(file_path, new_config):
                print("\n✅ 邮件配置已修复!")
                print("请重启应用以应用新的配置")
            else:
                print("\n⚠️ 自动更新失败，请手动更新配置文件")
                print(f"文件路径: {file_path}")
                print("请使用以下配置:")
                for key, value in new_config.items():
                    print(f"- {key}: {value}")
        else:
            print("\n❌ 邮件测试失败，请检查配置是否正确")
            print("常见问题:")
            print("1. 邮箱密码或授权码错误")
            print("2. 邮箱安全设置不允许第三方应用登录")
            print("3. 服务器地址或端口错误")
            print("4. SSL/TLS配置错误")

if __name__ == "__main__":
    main() 