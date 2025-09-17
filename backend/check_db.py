from app import create_app, db
from models import User

app = create_app()

with app.app_context():
    # 查看数据库中的所有用户
    users = User.query.all()
    
    print(f"数据库中的用户数量: {len(users)}")
    
    # 打印每个用户的信息
    for user in users:
        print(f"用户ID: {user.id}, 用户名: {user.username}, 邮箱: {user.email}")

    # 检查是否存在user表
    inspector = db.inspect(db.engine)
    tables = inspector.get_table_names()
    print(f"数据库中的表: {tables}")