from fastapi import APIRouter, HTTPException
from services.reddit_services import get_top_daily_posts
from backend.src.models.top_posts_request_model import TopPostsRequest

router = APIRouter ()

'''
This function will fetch daily posts, calculate their sentiment, then calculate the overall
winning probability of both parties, store them in their respective database.
'''
@router.post('/top')
async def top_daily_posts(payload: TopPostsRequest):
    subreddit = payload.subreddit
    time_interval = payload.time_interval
    if time_interval not in ["day", "week", "year"]:
        raise HTTPException (
            status_code=400,
            detail=f"Invalid time_interval '{time_interval}'. Must be 'day', 'week', or 'year'."
        )
    res = await get_top_daily_posts(subreddit, time_interval)
    return res