from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.helpers import bounded_int, compact, list_values
from tools.webclaw_api import WebclawClient


class BatchTool(Tool):
    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        urls = list_values(tool_parameters.get("urls"))
        if not urls:
            raise ValueError("At least one URL is required.")
        if len(urls) > 50:
            raise ValueError("Batch accepts at most 50 URLs per Dify invocation.")

        payload = compact(
            {
                "urls": urls,
                "formats": list_values(tool_parameters.get("formats")) or ["markdown"],
                "concurrency": bounded_int(
                    tool_parameters.get("concurrency"), 5, "Concurrency", 1, 20
                ),
                "no_cache": tool_parameters.get("no_cache", False),
            }
        )
        result = WebclawClient(
            self.runtime.credentials.get("webclaw_api_key")
        ).post("/v1/batch", payload)
        yield self.create_json_message(result)
