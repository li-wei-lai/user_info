import requests
import json
import re
from datetime import datetime

def test_webhook(webhook_url):
    """测试钉钉webhook是否有效"""
    print(f"正在测试webhook: {webhook_url}")
    
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
        response = requests.post(webhook_url, headers=headers, data=json.dumps(message), timeout=10)
        
        # 检查响应
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        response_data = response.json()
        if response.status_code == 200 and response_data.get('errcode') == 0:
            print("✅ 钉钉通知发送成功!")
            return True
        else:
            print(f"❌ 钉钉通知发送失败: {response_data.get('errmsg', '未知错误')}")
            return False
    except Exception as e:
        print(f"❌ 请求异常: {str(e)}")
        return False

def update_webhook_in_file(file_path, new_webhook):
    """更新文件中的webhook配置"""
    try:
        # 读取文件
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替换webhook
        pattern = r'DINGTALK_WEBHOOK = "([^"]+)"'
        if re.search(pattern, content):
            new_content = re.sub(pattern, f'DINGTALK_WEBHOOK = "{new_webhook}"', content)
            
            # 写回文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✅ 已更新 {file_path} 中的webhook配置")
            return True
        else:
            print(f"❌ 在 {file_path} 中未找到webhook配置")
            return False
    except Exception as e:
        print(f"❌ 更新文件失败: {str(e)}")
        return False

def main():
    print("===== 钉钉通知修复工具 =====")
    
    # 获取当前webhook
    try:
        from info_user.main import DINGTALK_WEBHOOK
        current_webhook = DINGTALK_WEBHOOK
        print(f"当前webhook: {current_webhook}")
    except ImportError:
        current_webhook = ""
        print("无法导入当前webhook配置")
    
    # 提供常见的钉钉机器人安全设置选项
    print("\n钉钉机器人安全设置建议:")
    print("1. 使用自定义关键词: 添加关键词'测试通知'和'新的信息提交'")
    print("2. 使用IP地址段: 添加您的服务器IP地址")
    
    # 获取新的webhook
    print("\n请从钉钉管理后台获取新的webhook URL")
    print("步骤: 打开钉钉群 -> 群设置 -> 智能群助手 -> 添加机器人 -> 自定义 -> 添加 -> 复制webhook URL")
    
    new_webhook = input("\n请输入新的webhook URL: ")
    if not new_webhook:
        print("未提供新的webhook URL，退出程序")
        return
    
    # 测试新的webhook
    print("\n正在测试新的webhook...")
    if test_webhook(new_webhook):
        # 更新配置文件
        file_path = 'info_user/main.py'
        if update_webhook_in_file(file_path, new_webhook):
            print("\n✅ 钉钉通知已修复!")
            print("请重启应用以应用新的配置")
        else:
            print("\n⚠️ 自动更新失败，请手动更新配置文件")
            print(f"文件路径: {file_path}")
            print(f"将DINGTALK_WEBHOOK的值更改为: {new_webhook}")
    else:
        print("\n❌ 新的webhook测试失败，请检查URL是否正确")
        print("常见问题:")
        print("1. URL复制不完整")
        print("2. 机器人安全设置不正确")
        print("3. 网络连接问题")

if __name__ == "__main__":
    main() 