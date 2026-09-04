from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.helpers import bounded_int, compact, required_text
from tools.webclaw_api import WebclawClient


class MapTool(Tool):
    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        payload = compact(
            {
                "url": required_text(tool_parameters.get("url"), "URL"),
                "search": tool_parameters.get("search"),
                "limit": bounded_int(tool_parameters.get("limit"), 100, "Page size", 1, 5000),
                "cursor": tool_parameters.get("cursor"),
            }
        )
        result = WebclawClient(
            self.runtime.credentials.get("webclaw_api_key")
        ).post("/v1/map", payload)
        yield self.create_json_message(result)
