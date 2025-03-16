from info_user.main import app, db
from sqlalchemy import text

def add_original_password_column():
    print("===== 添加原始密码字段 =====")
    
    with app.app_context():
        try:
            # 检查字段是否已存在
            with db.engine.connect() as conn:
                result = conn.execute(text("SHOW COLUMNS FROM user_info LIKE 'original_password'"))
                if not result.fetchone():
                    # 添加original_password字段
                    conn.execute(text("ALTER TABLE user_info ADD COLUMN original_password VARCHAR(255)"))
                    conn.commit()
                    print("成功添加original_password字段到user_info表")
                else:
                    print("original_password字段已存在")
                
            print("\n数据库更新完成！")
            print("现在管理员可以在用户详情中查看用户提交的原始密码")
            
        except Exception as e:
            print(f"更新数据库时出错: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    add_original_password_column() 