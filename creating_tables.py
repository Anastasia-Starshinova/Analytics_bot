import os
import psycopg2


DATABASE_URL = os.getenv("DATABASE_URL").replace("postgres://", "postgresql://")

conn = psycopg2.connect(DATABASE_URL)
print("✅ Подключение успешно")
conn.close()


def create_table():
    # today = datetime.now().date().isoformat()  # '2025-08-27'
    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()
    cursor.execute(f'CREATE TABLE test (id BIGSERIAL PRIMARY KEY, "name" TEXT)')
    connection.commit()
    connection.close()


create_table()

