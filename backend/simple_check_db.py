import sqlite3

# 连接到SQLite数据库
db_path = 'f:\workspace\point\instance\database.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 尝试查询user表的所有记录
try:
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"数据库中的表: {tables}")
    
    if ('user',) in tables:
        cursor.execute("SELECT * FROM user;")
        users = cursor.fetchall()
        print(f"用户表中的记录数量: {len(users)}")
        
        # 获取表结构
        cursor.execute("PRAGMA table_info(user);")
        columns = cursor.fetchall()
        print("表结构:")
        for column in columns:
            print(f"- {column[1]} ({column[2]})")
    else:
        print("用户表不存在")
except sqlite3.Error as e:
    print(f"数据库错误: {e}")
finally:
    # 关闭连接
    cursor.close()
    conn.close()