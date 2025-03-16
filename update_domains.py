import os
import re

def update_domains():
    try:
        # 获取用户输入的域名
        print("请输入各系统的域名配置")
        dashboard_domain = input("全域驾驶舱域名 (默认: https://omnipilot.mpsmedia.com.cn/account/login): ") or "https://omnipilot.mpsmedia.com.cn/account/login"
        compass_domain = input("供需罗盘域名 (默认: https://compass.mpsmedia.com.cn/account/login): ") or "https://compass.mpsmedia.com.cn/account/login"
        cube_domain = input("智投魔方域名 (默认: https://smartcube.mpsmedia.com.cn/account/login): ") or "https://smartcube.mpsmedia.com.cn/account/login"
        
        # 确保域名格式正确
        for domain in [dashboard_domain, compass_domain, cube_domain]:
            if not domain.startswith(('http://', 'https://')):
                print(f"警告: 域名 {domain} 不包含协议前缀 (http:// 或 https://)")
                if input("是否自动添加 https:// 前缀? (y/n): ").lower() == 'y':
                    if domain == dashboard_domain:
                        dashboard_domain = f"https://{dashboard_domain}"
                    elif domain == compass_domain:
                        compass_domain = f"https://{compass_domain}"
                    elif domain == cube_domain:
                        cube_domain = f"https://{cube_domain}"
        
        # 构建配置文件内容
        config_content = f"""# 系统域名配置
SYSTEM_DOMAINS = {{
    'dashboard': '{dashboard_domain}',  # 全域驾驶舱域名
    'compass': '{compass_domain}',      # 供需罗盘域名
    'cube': '{cube_domain}'             # 智投魔方域名
}}

# 系统名称配置
SYSTEM_NAMES = {{
    'dashboard': '全域驾驶舱',
    'compass': '供需罗盘',
    'cube': '智投魔方'
}}
"""
        
        # 写入配置文件
        config_path = os.path.join('info_user', 'config.py')
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(config_content)
        
        print(f"\n配置已更新到 {config_path}")
        print("\n当前系统域名配置:")
        print(f"  全域驾驶舱: {dashboard_domain}")
        print(f"  供需罗盘: {compass_domain}")
        print(f"  智投魔方: {cube_domain}")
        
    except Exception as e:
        print(f"更新域名配置失败: {str(e)}")

if __name__ == '__main__':
    update_domains() 