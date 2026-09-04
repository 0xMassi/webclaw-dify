import pytest

from tools.webclaw_api import WebclawAPIError, WebclawClient


class FakeResponse:
    def __init__(self, payload, status_code=200):
        self.payload = payload
        self.status_code = status_code
        self.ok = status_code < 400

    def json(self):
        return self.payload


class FakeSession:
    def __init__(self, response):
        self.response = response
        self.request_data = None

    def request(self, method, url, **kwargs):
        self.request_data = {"method": method, "url": url, **kwargs}
        return self.response


def test_client_sends_authenticated_request_without_exposing_the_key_in_payload():
    session = FakeSession(FakeResponse({"ok": True}))

    result = WebclawClient("wc_test", session=session).post(
        "/v1/scrape", {"url": "https://example.com"}
    )

    assert result == {"ok": True}
    assert session.request_data["url"] == "https://api.webclaw.io/v1/scrape"
    assert session.request_data["headers"]["Authorization"] == "Bearer wc_test"
    assert session.request_data["json"] == {"url": "https://example.com"}


def test_client_turns_api_errors_into_clear_plugin_errors():
    session = FakeSession(
        FakeResponse(
            {"error": "Invalid API key", "code": "invalid_api_key"},
            status_code=401,
        )
    )

    with pytest.raises(WebclawAPIError, match="401: Invalid API key") as caught:
        WebclawClient("wc_bad", session=session).get_usage()

    assert caught.value.status_code == 401
    assert caught.value.code == "invalid_api_key"


def test_client_rejects_an_empty_key_before_network_access():
    with pytest.raises(ValueError, match="API key is required"):
        WebclawClient(" ")
