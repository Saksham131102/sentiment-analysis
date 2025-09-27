from pydantic import BaseModel
from typing import Literal

class TopPostsRequest(BaseModel):
    subreddit: str
    time_interval: Literal["day", "week", "year"]