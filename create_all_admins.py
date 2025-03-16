import sys
import os

# 导入创建管理员的脚本
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from create_superadmin import create_superadmin
from create_system_admins import create_system_admins

if __name__ == '__main__':
    print("=== 开始创建超级管理员 ===")
    create_superadmin()
    print("\n=== 开始创建系统管理员 ===")
    create_system_admins()
    print("\n所有管理员账号创建完成！")
    print("请使用以下账号登录系统：")
    print("1. 超级管理员：superadmin / Admin@123")
    print("2. 全域驾驶舱管理员：dashboard_admin / Dashboard@123")
    print("3. 供需罗盘管理员：compass_admin / Compass@123")
    print("4. 智投魔方管理员：cube_admin / Cube@123") 