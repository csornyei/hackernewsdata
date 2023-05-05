import requests
from concurrent.futures import ThreadPoolExecutor


def get_top_stories():
    resp = requests.get(
        "https://hacker-news.firebaseio.com/v0/topstories.json")
    return resp.json()


def get_item_details(id: str):
    resp = requests.get(
        f"https://hacker-news.firebaseio.com/v0/item/{id}.json")
    return resp.json()


def get_story_with_comments(id: str, **kwargs):
    story_details = get_item_details(id)

    if "kids" not in story_details:
        story_details["comments"] = []
        return story_details

    comment_ids = story_details["kids"] if "comment_limit" not in kwargs else story_details["kids"][:kwargs["comment_limit"]]

    comments = [get_item_details(comment_id)
                for comment_id in comment_ids]

    del story_details["kids"]
    story_details["comments"] = comments

    return story_details


def get_story_all_comments(id: str):
    story_details = get_item_details(id)

    if "kids" not in story_details:
        return []

    comment_ids = story_details["kids"]
    comments = []

    for comment_id in comment_ids:
        comment = get_item_details(comment_id)
        if "kids" in comment:
            comments.extend(get_story_all_comments(comment_id))
        comments.append(comment)

    return comments


def get_stories_with_comments_parallel(story_ids: list, **kwargs):
    with ThreadPoolExecutor() as executor:
        stories = executor.map(
            lambda story_id: get_story_with_comments(story_id, **kwargs), story_ids)
    return list(stories)


def get_stories_with_all_comments_parallel(story_ids: list):
    with ThreadPoolExecutor() as executor:
        comments = executor.map(
            lambda story_id: get_story_all_comments(story_id), story_ids)
    return list(comments)
