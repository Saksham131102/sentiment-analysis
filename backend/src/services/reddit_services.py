import os
from httpx import AsyncClient
import asyncio
from dotenv import load_dotenv

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
    


# print(asyncio.run(get_reddit_token()))