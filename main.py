from fastapi import FastAPI

import hackerNewsApi

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/top-stories")
async def top_stories():
    print("Getting top stories")
    top_stories = hackerNewsApi.get_top_stories()
    first_hundred_stories = top_stories[:100]
    stories = []
    for story_id in first_hundred_stories:
        story = hackerNewsApi.get_story_with_comments(
            story_id, comment_limit=50)
        stories.append(story)
    return {"top_stories": stories}
