import psycopg2
import json
from psycopg2 import sql


# DATABASE_URL = os.getenv("DATABASE_URL").replace("postgres://", "postgresql://")

# if check_tables(DATABASE_URL, ['videos', 'video_snapshots']) is True:
#     pass
# else:
#     create_tables(DATABASE_URL)
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
            for key in data:
                if key == "snapshots":
                    snapshots_data = data.get("snapshots")
                    print(f'snapshots_data = {snapshots_data}')
                else:
                    print('else:')
                    print(f'key = {key}')
                    print(f'data.get("key") = {data.get(key)}')

        # {"id": "ecd8a4e4-1f24-4b97-a944-35d17078ce7c", "video_created_at": "2025-08-19T08:54:35+00:00",
            # "snapshots": [
            #         #         {
            #         #             "id": "466bb5862d3f47fd85f11ca0dc1e6629",
            #         #             "video_id": "ecd8a4e4-1f24-4b97-a944-35d17078ce7c",
            #         #             "views_count": 1461,]}

        # {
        #     "id": "ecd8a4e4-1f24-4b97-a944-35d17078ce7c",
        #     "video_created_at": "2025-08-19T08:54:35+00:00",
        #     "views_count": 1461,
        #     "likes_count": 35,
        #     "reports_count": 0,
        #     "comments_count": 0,
        #     "creator_id": "aca1061a9d324ecf8c3fa2bb32d7be63",
        #     "created_at": "2025-11-26T11:00:08.983295+00:00",
        #     "updated_at": "2025-12-01T10:00:00.236609+00:00",
        #     "snapshots": [
        #         {
        #             "id": "466bb5862d3f47fd85f11ca0dc1e6629",
        #             "video_id": "ecd8a4e4-1f24-4b97-a944-35d17078ce7c",
        #             "views_count": 1461,
        #             "likes_count": 35,
        #             "reports_count": 0,
        #             "comments_count": 0,
        #             "delta_views_count": 1461,
        #             "delta_likes_count": 35,
        #             "delta_reports_count": 0,
        #             "delta_comments_count": 0,
        #             "created_at": "2025-11-26T11:00:09.053200+00:00",
        #             "updated_at": "2025-11-26T11:00:09.053200+00:00"
        #         },
        #         {
        #             "id": "b6765497d60e4eae8d7aebf2fa307bf0",
        #             "video_id": "ecd8a4e4-1f24-4b97-a944-35d17078ce7c",
        #             "views_count": 1461,
        #             "likes_count": 35,
        #             "reports_count": 0,
        #             "comments_count": 0,
        #             "delta_views_count": 0,
        #             "delta_likes_count": 0,
        #             "delta_reports_count": 0,
        #             "delta_comments_count": 0,
        #             "created_at": "2025-11-26T12:00:09.334212+00:00",
        #             "updated_at": "2025-11-26T12:00:09.334212+00:00"
        #         },


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
