import psycopg2


# DATABASE_URL = os.getenv("DATABASE_URL").replace("postgres://", "postgresql://")


def create_tables(database_url):
    connection = psycopg2.connect(database_url)
    cursor = connection.cursor()
    cursor.execute(f'CREATE TABLE IF NOT EXISTS videos ('
                   f'id TEXT,'
                   f'creator_id TEXT, '
                   f'video_created_at TIMESTAMP,'
                   f'views_count INT, '
                   f'likes_count INT,'
                   f'comments_count INT,'
                   f'reports_count INT,'
                   f'created_at TIMESTAMP,'
                   f'updated_at TIMESTAMP)')
    connection.commit()
    connection.close()

    connection = psycopg2.connect(database_url)
    cursor = connection.cursor()
    cursor.execute(f'CREATE TABLE IF NOT EXISTS video_snapshots ('
                   f'id TEXT,'
                   f'video_id TEXT, '
                   f'views_count INT,'
                   f'likes_count INT, '
                   f'comments_count INT,'
                   f'reports_count INT,'
                   f'delta_views_count INT,'
                   f'delta_likes_count INT,'
                   f'delta_comments_count INT,'
                   f'delta_reports_count INT,'
                   f'created_at TIMESTAMP,'
                   f'updated_at TIMESTAMP)')
    connection.commit()
    connection.close()


def delete_table(database_url):
    connection = psycopg2.connect(database_url)
    cursor = connection.cursor()
    cursor.execute(f'DROP TABLE IF EXISTS test')
    connection.commit()
    connection.close()
