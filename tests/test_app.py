"""
Test module for the Flask app
"""

# pylint: disable=redefined-outer-name

import os

import pytest

from flask import Flask
from flask.testing import FlaskClient

from src import create_app
from src.utils import find, get_posts, get_post_data, get_related_posts

CURRENT_DIR = os.path.dirname(__file__)


@pytest.fixture()
def app():
    """
    Creates an instance of the Flask app

    Yields:
        Flask: app instance
    """
    application = create_app()
    application.config.update({
        "TESTING": True,
    })
    yield application


@pytest.fixture()
def client(app: Flask) -> FlaskClient:
    """
    Gets a test client from the test Flask instance

    Args:
        app (Flask): Flask app instance

    Returns:
        FlaskClient: test client 
    """
    return app.test_client()


class TestApp:
    """
    Flask app test class
    """

    # ===== Test Secure HTTP Headers =====

    def test_response_includes_content_security_policy(self, client: FlaskClient) -> None:
        """
        Assert response includes Content-Security-Policy header

        Args:
            client (FlaskClient): client returned by fixture
        """
        response = client.get("/")
        assert "Content-Security-Policy" in response.headers

    def test_response_includes_x_xss_protection(self, client: FlaskClient) -> None:
        """
        Assert response includes X-XSS-Protection header

        Args:
            client (FlaskClient): client returned by fixture
        """
        response = client.get("/")
        assert "X-XSS-Protection" in response.headers

    def test_response_includes_strict_transport_security(self, client: FlaskClient) -> None:
        """
        Assert response includes Strict-Transport-Security header

        Args:
            client (FlaskClient): client returned by fixture
        """
        response = client.get("/")
        assert "Strict-Transport-Security" in response.headers

    def test_response_includes_x_content_type_options(self, client: FlaskClient) -> None:
        """
        Assert response includes X-Content-Type-Options header

        Args:
            client (FlaskClient): client returned by fixture
        """
        response = client.get("/")
        assert "X-Content-Type-Options" in response.headers

    def test_response_includes_x_frame_options(self, client: FlaskClient) -> None:
        """
        Assert response includes X-Frame-Options header

        Args:
            client (FlaskClient): client returned by fixture
        """
        response = client.get("/")
        assert "X-Frame-Options" in response.headers

    # ===== Test App Routes =====

    # ===== / =====

    def test_core_index_returns_correct_page(self, client: FlaskClient) -> None:
        """
        Asserts the correct page is returned by core.index

        Args:
            client (FlaskClient): client returned by fixture
        """
        response = client.get("/")
        assert b"My Blog" in response.data

    def test_core_index_returns_200(self, client: FlaskClient) -> None:
        """
        Asserts the correct code is returned by core.index

        Args:
            client (FlaskClient): client returned by fixture
        """
        response = client.get("/")
        assert response.status_code == 200

    # ===== /posts =====

    def test_post_posts_returns_correct_page(self, client: FlaskClient) -> None:
        """
        Asserts the correct page is returned by posts.posts

        Args:
            client (FlaskClient): client returned by fixture
        """
        response = client.get("/posts")
        assert b"Posts" in response.data

    def test_post_posts_returns_200(self, client: FlaskClient) -> None:
        """
        Asserts the correct code is returned by posts.posts

        Args:
            client (FlaskClient): client returned by fixture
        """
        response = client.get("/posts")
        assert response.status_code == 200

    # ===== /search =====

    def test_post_search_returns_correct_page(self, client: FlaskClient) -> None:
        """
        Asserts the correct page is returned by posts.search

        Args:
            client (FlaskClient): client returned by fixture
        """
        response = client.get("/search")
        assert b"Search" in response.data

    def test_post_search_returns_200(self, client: FlaskClient) -> None:
        """
        Asserts the correct code is returned by posts.search

        Args:
            client (FlaskClient): client returned by fixture
        """
        response = client.get("/search")
        assert response.status_code == 200

    def test_post_search_returns_307(self, client: FlaskClient) -> None:
        """
        Asserts the correct code is returned by posts.search

        Args:
            client (FlaskClient): client returned by fixture
        """
        response = client.post("/search", data={"search": "test"})
        assert response.status_code == 307

    def test_post_search_displays_empty_search_message(self, client: FlaskClient) -> None:
        """
        Assert message is displayed to user if search box is empty on submit
        """
        response = client.post("/search", data={"search": ""})
        assert b"Please provide a term to search for" in response.data

    # ===== /results =====

    def test_post_results_returns_search_page(self, client: FlaskClient) -> None:
        """
        Asserts the search page is returned by posts.results without POST data

        Args:
            client (FlaskClient): client returned by fixture
        """
        response = client.get("/results")
        assert b"Search" in response.data

    def test_post_results_returns_200(self, client: FlaskClient) -> None:
        """
        Asserts the correct code is returned by posts.results

        Args:
            client (FlaskClient): client returned by fixture
        """
        response = client.get("/results")
        assert response.status_code == 200

    def test_post_results_returns_results_page_with_query_params(self, client: FlaskClient) -> None:
        """
        Asserts the results page is returned by posts.results without POST data

        Args:
            client (FlaskClient): client returned by fixture
        """
        response = client.post("/results?search=test")
        assert b"Results" in response.data

    def test_post_results_returns_200_with_query_params(self, client: FlaskClient) -> None:
        """
        Asserts the correct code is returned by posts.results

        Args:
            client (FlaskClient): client returned by fixture
        """
        response = client.post("/results?search=test")
        assert response.status_code == 200


class TestErrorHandlers:
    """
    Flask app error handlers test class
    """

    def test_bad_route_returns_404(self, client: FlaskClient) -> None:
        """
        Asserts 404 response code returned when route not found

        Args:
            client (FlaskClient): client returned by fixture
        """
        response = client.get("/this/does/not/exist")
        assert response.status_code == 404

    def test_bad_route_returns_404_page(self, client: FlaskClient) -> None:
        """
        Asserts 404 response page returned

        Args:
            client (FlaskClient): client returned by fixture
        """
        response = client.get("/this/does/not/exist")
        assert b"<h1>Error 404</h1>" in response.data


class TestUtils:
    """
    Utility function test class
    """

    @classmethod
    def setup_class(cls) -> None:
        """
        Setup class method for test class
        """
        cls.file_path = None

    def setup_method(self) -> None:
        """
        Setup method for test class
        """
        self.file_path = f"{CURRENT_DIR}/index.test.json"

    def test_get_posts_returns_list(self) -> None:
        """
        Assert get_posts() returns posts list
        """
        posts = get_posts(self.file_path)
        assert isinstance(posts["posts"], list)

    def test_get_post_data_returns_correct_object(self) -> None:
        """
        Assert get_post_data() returns the right object
        """
        endpoint = "/test"
        post = get_post_data(endpoint, self.file_path)
        assert post["title"] == "Test Post"

    def test_get_post_data_returns_none(self) -> None:
        """
        Assert get_post_data() returns None if path not found
        """
        endpoint = "/does/not/exist"
        post = get_post_data(endpoint, self.file_path)
        assert post is None

    def test_get_related_posts_returns_empty_list(self) -> None:
        """
        Assert get_related_posts() returns empty list if no ids found
        """
        ids = []
        posts = get_related_posts(ids, self.file_path)
        assert not posts

    def test_get_related_posts_returns_list(self) -> None:
        """
        Assert get_related_posts() returns list of posts
        """
        ids = [1]
        posts = get_related_posts(ids, self.file_path)
        assert posts[0]["title"] == "Test Post"

    def test_find_returns_empty_list(self) -> None:
        """
        Assert no results are found for non-matching query
        """
        query = "Non-existent"
        assert not find(query, self.file_path)

    def test_find_returns_search_result(self) -> None:
        """
        Assert results list is returned for matching query
        """
        query = "Test"
        result = find(query, self.file_path)
        assert result[0]["title"] == "Test Post"
