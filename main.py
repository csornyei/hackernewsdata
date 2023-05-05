from fastapi import FastAPI

import hackerNewsApi
import utils

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/top-stories")
async def top_stories():
    top_stories = hackerNewsApi.get_top_stories()
    first_hundred_stories = top_stories[:100]
    stories = []
    for story_id in first_hundred_stories:
        story = hackerNewsApi.get_story_with_comments(
            story_id, comment_limit=50)
        stories.append(story)
    return {"top_stories": stories}


@app.get("/most-used-words")
async def most_used_words():
    top_stories = hackerNewsApi.get_top_stories()
    first_thirty_stories = top_stories[:30]
    comments = []
    for story_id in first_thirty_stories:
        story = hackerNewsApi.get_story_with_comments(
            story_id, comment_limit=100)
        comments.extend(story["comments"])

    word_occurences = {}
    for comment in comments:
        comment_text = comment["text"]
        if comment_text is None:
            continue
        cleaned_text = utils.clean_text(comment_text)
        comment_word_occurences = utils.get_word_occurences(cleaned_text)
        word_occurences = utils.combine_word_occurences(
            word_occurences, comment_word_occurences)

    sorted_word_occurences = sorted(
        word_occurences.items(), key=lambda x: x[1], reverse=True)

    return {"most_used_words": sorted_word_occurences[:10]}
