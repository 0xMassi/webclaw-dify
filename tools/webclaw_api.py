from __future__ import annotations

from typing import Any

import requests

BASE_URL = "https://api.webclaw.io"
REQUEST_TIMEOUT = 120


class WebclawAPIError(RuntimeError):
    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        code: str | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.code = code


class WebclawClient:
    def __init__(self, api_key: str | None, session: requests.Session | None = None) -> None:
        if not api_key or not api_key.strip():
            raise ValueError("Webclaw API key is required.")
        self._api_key = api_key.strip()
        self._session = session or requests.Session()

    def get_usage(self) -> dict[str, Any]:
        return self._request("GET", "/v1/usage")

    def post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        return self._request("POST", path, payload)

    def _request(
        self,
        method: str,
        path: str,
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        try:
            response = self._session.request(
                method,
                f"{BASE_URL}{path}",
                json=payload,
                headers={
                    "Authorization": f"Bearer {self._api_key}",
                    "Content-Type": "application/json",
                    "User-Agent": "webclaw-dify/0.1.0",
                },
                timeout=REQUEST_TIMEOUT,
            )
        except requests.RequestException as exc:
            raise WebclawAPIError(f"Could not reach the Webclaw API: {exc}") from exc

        try:
            data = response.json()
        except ValueError as exc:
            raise WebclawAPIError(
                f"Webclaw API returned an invalid response ({response.status_code})."
            ) from exc

        if not response.ok:
            detail = "request failed"
            code = None
            if isinstance(data, dict):
                detail = str(data.get("error") or data.get("message") or detail)
                code = data.get("code")
            raise WebclawAPIError(
                f"Webclaw API returned {response.status_code}: {detail}",
                status_code=response.status_code,
                code=str(code) if code else None,
            )
        if not isinstance(data, dict):
            raise WebclawAPIError("Webclaw API returned an unexpected response shape.")
        return data
