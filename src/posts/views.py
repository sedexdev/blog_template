"""
Post app views module 
"""

from flask import Blueprint, redirect, render_template, Response, request, url_for

from src.utils import find, get_posts, get_post_data, get_related_posts

post_bp = Blueprint(
    "posts",
    __name__,
    template_folder="templates"
)


@post_bp.route("/posts")
def posts() -> Response:
    """
    Returns the posts template with data
    read from 'index.json'

    Returns:
        Response: app response object
    """
    data = get_posts()
    return render_template("posts.html", posts=data["posts"], title="Posts")


@post_bp.route("/search", methods=["GET", "POST"])
def search() -> Response:
    """
    Returns the search template

    Returns:
        Response: app response object
    """
    if request.method == "POST":
        params = request.form["search"]
        if not params:
            message = "Please provide a term to search for"
            return render_template("search.html", message=message, title="Search")
        return redirect(url_for("posts.results", search=params), code=307)
    return render_template("search.html", title="Search")


@post_bp.route("/results", methods=["GET", "POST"])
def results() -> Response:
    """
    Returns the results template

    Args:
        result (list): list of search results
    Returns:
        Response: app response object
    """
    if request.method == "POST":
        query = request.args.get("search")
        result = find(query)
        return render_template("results.html", query=query, posts=result, title="Results")
    return render_template("search.html", title="Search")


@post_bp.route("/test")
def test() -> Response:
    """
    Returns Test Post post template

    Returns:
        Response: app Response object
    """
    post = get_post_data(request.path)
    related = get_related_posts(post["related"])
    return render_template("test_post.html", post=post, related=related, title=f"{post['title']}")
