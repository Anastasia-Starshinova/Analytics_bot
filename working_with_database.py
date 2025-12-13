import psycopg2
import json
from psycopg2 import sql

# keys_videos = ['id', 'creator_id', 'video_created_at', 'views_count', 'likes_count', 'comments_count',
#                'reports_count', 'created_at', 'updated_at']
# keys_video_snapshots = ['id', 'video_id', 'views_count', 'likes_count', 'comments_count', 'reports_count',
#                         'delta_views_count', 'delta_likes_count', 'delta_comments_count', 'delta_reports_count',
#                         'created_at', 'updated_at']


def check_tables(database_url, tables_list):
    count_of_true = 0
    # try:
    connection = psycopg2.connect(database_url)
    cursor = connection.cursor()

    for table in tables_list:
        print(f'table = {table}')
        cursor.execute(sql.SQL("""SELECT EXISTS (SELECT FROM information_schema.tables 
        WHERE table_schema = 'public' AND table_name = %s);"""), [table])
        exists = cursor.fetchone()[0]
        if exists is True:
            count_of_true += 1

    if count_of_true == len(tables_list):
        print('if count_of_true == len(tables_list):')
        return True
    # except Exception as e:
    #     print("Ошибка при проверке таблиц:", e)
    # finally:
    #     if cursor:
    #         cursor.close()
    #     if connection:
    #         connection.close()
    #
    # return results


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

    with open("videos.json", "r", encoding="utf-8") as file:
        all_data = json.load(file)
        all_data = all_data.get('videos')

        print(type(all_data))
        print(len(all_data))

        for data in all_data:
            data_id = data.get('id')
            creator_id = data.get('creator_id')
            video_created_at = data.get('video_created_at')
            views_count = data.get('views_count')
            likes_count = data.get('likes_count')
            comments_count = data.get('comments_count')
            reports_count = data.get('reports_count')
            created_at = data.get('created_at')
            updated_at = data.get('updated_at')

            connection = psycopg2.connect(database_url)
            cursor = connection.cursor()
            cursor.execute(f'INSERT INTO videos '
                           f'(id, creator_id, video_created_at, views_count, likes_count,'
                           f'comments_count, reports_count, created_at,'
                           f'updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                           (data_id, creator_id, video_created_at, views_count, likes_count, comments_count,
                            reports_count, created_at, updated_at))
            connection.commit()
            connection.close()

            snapshots_data = data.get("snapshots")
            print(f'snapshots_data = {snapshots_data}')
            if snapshots_data:
                for dict_data in snapshots_data:
                    snapshots_id = dict_data.get('id')
                    video_id = dict_data.get('video_id')
                    views_count = dict_data.get('views_count')
                    likes_count = dict_data.get('likes_count')
                    comments_count = dict_data.get('comments_count')
                    reports_count = dict_data.get('reports_count')
                    delta_views_count = dict_data.get('delta_views_count')
                    delta_likes_count = dict_data.get('delta_likes_count')
                    delta_comments_count = dict_data.get('delta_comments_count')
                    delta_reports_count = dict_data.get('delta_reports_count')
                    created_at = dict_data.get('created_at')
                    updated_at = dict_data.get('updated_at')

                    connection = psycopg2.connect(database_url)
                    cursor = connection.cursor()
                    cursor.execute(f'INSERT INTO video_snapshots '
                                   f'(id, video_id, views_count, likes_count, comments_count,'
                                   f'reports_count, delta_views_count, delta_likes_count,'
                                   f'delta_comments_count, delta_reports_count, '
                                   f'created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,'
                                   f'%s, %s, %s)', (snapshots_id, video_id, views_count, likes_count,
                                                    comments_count, reports_count, delta_views_count,
                                                    delta_likes_count, delta_comments_count, delta_reports_count,
                                                    created_at, updated_at))
                    connection.commit()
                    connection.close()


def delete_table(database_url):
    connection = psycopg2.connect(database_url)
    cursor = connection.cursor()
    cursor.execute(f'DROP TABLE IF EXISTS videos')
    connection.commit()
    connection.close()

    connection = psycopg2.connect(database_url)
    cursor = connection.cursor()
    cursor.execute(f'DROP TABLE IF EXISTS video_snapshots')
    connection.commit()
    connection.close()
