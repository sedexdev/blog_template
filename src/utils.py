"""
Utility functions to aid the application backend
"""

import json
import os

CURRENT_DIR = os.path.dirname(__file__)


def get_posts(file_path: str = None) -> list:
    """
    Gets and returns post data objects from
    index.json

    Args:
        file_path (str): path to data file | None

    Returns:
        list: list of post metadata objects
    """
    if file_path is None:
        file_path = f"{CURRENT_DIR}/index.json"
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.loads(file.read())
    return data


def get_post_data(path: str, file_path: str = None) -> dict:
    """
    Reads index.json and returns the object
    with the matching path

    Args:
        path (str): app endpoint
        file_path (str): path to data file | None

    Returns:
        dict: deserialized Python dict
    """
    if file_path is None:
        file_path = f"{CURRENT_DIR}/index.json"
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.loads(file.read())
    for entry in data["posts"]:
        if entry["path"] == path:
            return entry
    return None


def get_related_posts(ids: list, file_path: str = None) -> list:
    """
    Reads index.json and returns the objects
    with the matching post ids

    Args:
        ids (list): list of post ids
        file_path (str): path to data file | None

    Returns:
        list: list of deserialized Python dicts
    """
    if file_path is None:
        file_path = f"{CURRENT_DIR}/index.json"
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.loads(file.read())
    related_posts = []
    for entry in data["posts"]:
        if entry["id"] in ids:
            related_posts.append(entry)
    return related_posts


def find(query: str, file_path: str = None) -> list:
    """
    Uses the query string to find post data
    objects with fields matching the query.

    Compared fields are:
        - title
        - tags
        - meta_description

    Args:
        query (str): search query string
        file_path (str): path to data file | None

    Returns:
        list: list of posts matching
    """
    results = []
    if file_path is None:
        file_path = f"{CURRENT_DIR}/index.json"
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.loads(file.read())
    for entry in data["posts"]:
        if query.lower() in entry["title"].lower():
            results.append(entry)
        elif query.lower() in entry["tags"]:
            results.append(entry)
        elif query.lower() in entry["meta_description"].lower():
            results.append(entry)
    return results
