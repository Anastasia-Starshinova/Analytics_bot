import asyncpg
from datetime import datetime


async def get_pool(database_url: str):
    return await asyncpg.create_pool(database_url)


async def query_database(pool, action: str, params: dict = None):
    params = params or {}

    if action == "total_videos":
        query = "SELECT COUNT(*) AS total FROM videos"
        result = await pool.fetchrow(query)
        return int(result["total"])

    elif action == "total_snapshots":
        query = "SELECT COUNT(*) AS total FROM video_snapshots"
        result = await pool.fetchrow(query)
        return int(result["total"])

    elif action == "top_likes":
        query = "SELECT MAX(likes_count) AS max_likes FROM videos"
        result = await pool.fetchrow(query)
        return int(result["max_likes"] or 0)

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
        return int(result["total"] or 0)

    elif action == "views_above_threshold":
        threshold = int(params.get("threshold", 100000))
        query = "SELECT COUNT(*) AS total FROM videos WHERE views_count >= $1"
        result = await pool.fetchrow(query, threshold)
        return int(result["total"] or 0)

    elif action == "snapshot_max_views":
        query = "SELECT MAX(views_count) AS max_views FROM video_snapshots"
        result = await pool.fetchrow(query)
        return int(result["max_views"] or 0)

    elif action == "snapshot_by_video":
        video_id = params.get("video_id")
        query = "SELECT COUNT(*) AS total FROM video_snapshots WHERE video_id = $1"
        result = await pool.fetchrow(query, video_id)
        return int(result["total"] or 0)

    elif action == "sum_views_by_date":
        date_str = params.get("date")  # "2025-11-28"
        if not date_str:
            return 0
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        query = """SELECT SUM(views_count) AS total FROM video_snapshots WHERE created_at::date = $1"""
        result = await pool.fetchrow(query, date_obj)
        return int(result["total"] or 0)

    elif action == "videos_with_views_on_date":
        date_str = params.get("date")  # "2025-11-27"
        if not date_str:
            return 0
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        query = """SELECT COUNT(DISTINCT video_id) AS total FROM video_snapshots WHERE created_at::date = $1
        AND views_count > 0"""
        result = await pool.fetchrow(query, date_obj)
        return int(result["total"] or 0)

    else:
        return 0
