import psycopg2


# DATABASE_URL = os.getenv("DATABASE_URL").replace("postgres://", "postgresql://")


def create_table(database_url):
    connection = psycopg2.connect(database_url)
    cursor = connection.cursor()
    cursor.execute(f'CREATE TABLE test (id BIGSERIAL PRIMARY KEY, "name" TEXT)')
    connection.commit()
    connection.close()

