from fastapi import APIRouter
from services.reddit_services import get_top_daily_posts

router = APIRouter ()

'''
This function will fetch daily posts, calculate their sentiment, then calculate the overall
winning probability of both parties, store them in their respective database.
'''
@router.post('/top')
async def top_daily_posts(subreddit: str, time_interval: str):
    posts_array = get_top_daily_posts(subreddit, time_interval)
    return posts_array