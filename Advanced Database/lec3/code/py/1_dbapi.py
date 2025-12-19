import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# 数据库连接参数
db_params = {
    "dbname": "dbapi_",  # 数据库名称
    "user": "postgres",         # 数据库用户名
    "password": "1",     # 数据库密码
    "host": "localhost",             # 数据库主机地址
    "port": "5432"                   # 数据库端口
}

def connect_to_db():
    """连接到 PostgreSQL 数据库"""
    try:
        connection = psycopg2.connect(**db_params)
        print("数据库连接成功")
        return connection
    except Exception as e:
        print(f"连接数据库失败：{e}")
        return None

def create_table(connection):
    """创建表"""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                age INT,
                department VARCHAR(50)
            );
        """)
        connection.commit()
        print("表创建成功")
    except Exception as e:
        print(f"创建表失败：{e}")
        connection.rollback()

def insert_data(connection):
    """插入数据"""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO employees (name, age, department) VALUES (%s, %s, %s);
        """, ("Alice", 30, "HR"))
        cursor.execute("""
            INSERT INTO employees (name, age, department) VALUES (%s, %s, %s);
        """, ("Bob", 25, "Engineering"))
        connection.commit()
        print("数据插入成功")
    except Exception as e:
        print(f"插入数据失败：{e}")
        connection.rollback()

def query_data(connection):
    """查询数据"""
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM employees;")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except Exception as e:
        print(f"查询数据失败：{e}")

def update_data(connection):
    """更新数据"""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE employees SET age = %s WHERE name = %s;
        """, (31, "Alice"))
        connection.commit()
        print("数据更新成功")
    except Exception as e:
        print(f"更新数据失败：{e}")
        connection.rollback()

def delete_data(connection):
    """删除数据"""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            DELETE FROM employees WHERE name = %s;
        """, ("Bob",))
        connection.commit()
        print("数据删除成功")
    except Exception as e:
        print(f"删除数据失败：{e}")
        connection.rollback()

def drop_table(connection):
    """删除表"""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            DROP TABLE IF EXISTS employees;
        """)
        connection.commit()
        print("表删除成功")
    except Exception as e:
        print(f"删除表失败：{e}")
        connection.rollback()

def main():
    connection = connect_to_db()
    if connection:
        create_table(connection)
        insert_data(connection)
        query_data(connection)
        update_data(connection)
        query_data(connection)
        delete_data(connection)
        query_data(connection)
        drop_table(connection)
        connection.close()
        print("数据库连接关闭")

if __name__ == "__main__":
    main()
