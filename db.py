import asyncpg


async def get_pool(database_url: str):
    return await asyncpg.create_pool(database_url)


# async def get_top_videos(pool, limit: int = 5):
#     query = """
#         SELECT id, views_count, likes_count
#         FROM videos
#         ORDER BY likes_count DESC
#         LIMIT $1
#     """
#     return await pool.fetch(query, limit)

async def query_database(pool, action: str, params: dict = None):
    params = params or {}

    if action == "total_videos":
        query = "SELECT COUNT(*) AS total FROM videos"
        result = await pool.fetchrow(query)
        return result["total"]

    elif action == "top_likes":
        query = "SELECT MAX(likes_count) AS max_likes FROM videos"
        result = await pool.fetchrow(query)
        return result["max_likes"]

    elif action == "videos_by_creator":
        creator_id = params.get("creator_id")
        start_date = params.get("start_date")
        end_date = params.get("end_date")
        query = """
            SELECT COUNT(*) AS total
            FROM videos
            WHERE creator_id = $1 AND video_created_at BETWEEN $2 AND $3
        """
        result = await pool.fetchrow(query, creator_id, start_date, end_date)
        return result["total"]

    elif action == "views_above_threshold":
        threshold = params.get("threshold", 100000)
        query = "SELECT COUNT(*) AS total FROM videos WHERE views_count >= $1"
        result = await pool.fetchrow(query, threshold)
        return result["total"]

    else:
        return 0

