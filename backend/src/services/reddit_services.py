import os
from httpx import AsyncClient
# import asyncio
from dotenv import load_dotenv
from fastapi import HTTPException
from typing import List, TypedDict

load_dotenv()

REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT')

'''
reddit apis can be accessed when authorized
So we need the authorization token
'''
async def get_reddit_token() -> str:
    async with AsyncClient(auth=(REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET)) as client:
        data = {'grant_type': 'client_credentials'}
        headers = {'User-Agent': REDDIT_USER_AGENT}
        response = await client.post(
            'https://www.reddit.com/api/v1/access_token',
            data=data,
            headers=headers
        )
        response.raise_for_status()
        token = response.json()['access_token']
        return token
    
# Type definition for a Reddit post object
class PostProp(TypedDict):
    post_id: str
    subreddit: str
    title: str
    selftext: str
    author: str
    created_utc: int

async def get_top_daily_posts(subreddit: str, time_interval: str = 'day'):
    token = await get_reddit_token()
    headers = {
        'User-Agent': REDDIT_USER_AGENT,
        'Authorization': f'bearer {token}'
    }
    async with AsyncClient() as client:
        url = f'https://oauth.reddit.com/r/{subreddit}/top?t={time_interval}'
        response = await client.get(
            url,
            headers = headers
        )

        '''
            If a subreddit doesn't exist, we get status code as 302.
            Because 'httpx' doesn't follow redirects automatically.
        '''
        if response.status_code == 302:
            raise HTTPException (
                status_code=404,
                detail=f"Subreddit '{subreddit}' does not exist"
            )

        response.raise_for_status()
        data = response.json()['data']['children']

        '''
            We need the below conditional statement it we set 'follow_redirects' for httpx as true.
            Because the subreddit, that doesn't exist, will be treated as the subreddit that exists,
            but with no posts
        '''
        if not data:
            raise HTTPException (
                status_code=404,
                detail='Subreddit either has no posts or does not exist'
            )
        
        posts: List[PostProp] = []
        for child in data:
            post = child['data']
            posts.append({
                'post_id': post['id'],
                'subreddit': post['subreddit'],
                'title': post['title'],
                'selftext': post['selftext'],
                'author': post['author'],
                'created_utc': post['created_utc']
            })
        return posts


# print(asyncio.run(get_reddit_token()))