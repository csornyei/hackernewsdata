from fastapi import FastAPI, Request

import hackerNewsApi
import utils

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/top-stories")
async def top_stories(req: Request):
    story_count = req.query_params.get("story-count")
    if story_count is None:
        story_count = 10
    else:
        story_count = int(story_count)
    top_stories = hackerNewsApi.get_top_stories()
    first_hundred_stories = top_stories[:story_count]
    stories = []
    for story_id in first_hundred_stories:
        story = hackerNewsApi.get_story_with_comments(
            story_id, comment_limit=50)
        stories.append(story)
    return {"top_stories": stories}


@app.get("/most-used-words")
async def most_used_words(req: Request):
    story_count = req.query_params.get("story-count")
    if story_count is None:
        story_count = 30
    else:
        story_count = int(story_count)
    top_stories = hackerNewsApi.get_top_stories()
    first_thirty_stories = top_stories[:story_count]
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

    word_count_param = req.query_params.get("word-count")

    if word_count_param == "all":
        return {"most_used_words": sorted_word_occurences}

    if word_count_param is None:
        word_count = 10
    else:
        word_count = int(word_count_param)

    return {"most_used_words": sorted_word_occurences[:word_count]}


@app.get("/most-used-words-all")
async def most_used_words_all(req: Request):
    story_count = req.query_params.get("story-count")
    if story_count is None:
        story_count = 10
    else:
        story_count = int(story_count)
    top_stories = hackerNewsApi.get_top_stories()
    first_ten_stories = top_stories[:story_count]
    comments = []
    for story_id in first_ten_stories:
        comments = hackerNewsApi.get_story_all_comments(story_id)

    word_occurences = {}
    for comment in comments:
        if "text" not in comment:
            continue
        comment_text = comment["text"]
        cleaned_text = utils.clean_text(comment_text)
        comment_word_occurences = utils.get_word_occurences(cleaned_text)
        word_occurences = utils.combine_word_occurences(
            word_occurences, comment_word_occurences)

    sorted_word_occurences = sorted(
        word_occurences.items(), key=lambda x: x[1], reverse=True)

    word_count_param = req.query_params.get("word-count")
    if word_count_param == "all":
        return {"most_used_words": sorted_word_occurences}

    if word_count_param is None:
        word_count = 10
    else:
        word_count = int(word_count_param)

    return {"most_used_words": sorted_word_occurences[:word_count]}
