import asyncpg


async def get_pool(database_url: str):
    return await asyncpg.create_pool(database_url)


async def get_top_videos(pool, limit: int = 5):
    query = """
        SELECT id, views_count, likes_count
        FROM videos
        ORDER BY likes_count DESC
        LIMIT $1
    """
    return await pool.fetch(query, limit)