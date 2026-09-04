import pytest

from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from provider.webclaw import WebclawProvider
from tools.webclaw_api import WebclawAPIError, WebclawClient


def make_provider():
    return object.__new__(WebclawProvider)


def test_provider_validates_an_unscoped_key(monkeypatch):
    monkeypatch.setattr(WebclawClient, "get_usage", lambda self: {"credits_remaining": 10})

    make_provider()._validate_credentials({"webclaw_api_key": "wc_test"})


def test_provider_accepts_an_authenticated_scoped_key(monkeypatch):
    def deny_usage(self):
        raise WebclawAPIError(
            "Webclaw API returned 403: API key is not allowed to access this endpoint.",
            status_code=403,
            code="api_key_scope_denied",
        )

    monkeypatch.setattr(WebclawClient, "get_usage", deny_usage)

    make_provider()._validate_credentials({"webclaw_api_key": "wc_scoped"})


def test_provider_rejects_an_invalid_key(monkeypatch):
    def reject_key(self):
        raise WebclawAPIError(
            "Webclaw API returned 401: Invalid API key",
            status_code=401,
            code="invalid_api_key",
        )

    monkeypatch.setattr(WebclawClient, "get_usage", reject_key)

    with pytest.raises(ToolProviderCredentialValidationError, match="Invalid API key"):
        make_provider()._validate_credentials({"webclaw_api_key": "wc_bad"})
