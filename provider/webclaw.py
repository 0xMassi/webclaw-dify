from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from tools.webclaw_api import WebclawAPIError, WebclawClient


class WebclawProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            WebclawClient(credentials.get("webclaw_api_key")).get_usage()
        except WebclawAPIError as exc:
            # Scoped keys cannot access the non-billable usage endpoint, but
            # this specific response proves the API authenticated the key.
            if exc.status_code == 403 and exc.code == "api_key_scope_denied":
                return
            raise ToolProviderCredentialValidationError(str(exc)) from exc
        except ValueError as exc:
            raise ToolProviderCredentialValidationError(str(exc)) from exc
