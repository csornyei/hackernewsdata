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
    stories = hackerNewsApi.get_stories_with_comments_parallel(
        first_hundred_stories, comment_limit=50)
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
    stories = hackerNewsApi.get_stories_with_comments_parallel(
        first_thirty_stories, comment_limit=100)

    comments = []
    for story in stories:
        if "comments" not in story:
            continue
        comments.extend(story["comments"])

    comments = list(
        filter(lambda comment: comment is not None and "text" in comment, comments))

    comments_text = [utils.clean_text(comment["text"]) for comment in comments]

    word_occurences = utils.get_word_occurences_parallel(comments_text)

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
    story_comments = hackerNewsApi.get_stories_with_all_comments_parallel(
        first_ten_stories)

    comments = []
    for story_comment in story_comments:
        comments.extend(story_comment)

    comments = list(
        filter(lambda comment: comment is not None and "text" in comment, comments))
    print(len(comments))

    comments_text = [utils.clean_text(comment["text"]) for comment in comments]

    word_occurences = utils.get_word_occurences_parallel(comments_text)

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
