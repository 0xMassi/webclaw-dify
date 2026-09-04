from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.helpers import bounded_int, compact, list_values, required_text
from tools.webclaw_api import WebclawClient


class SearchTool(Tool):
    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        scrape = bool(tool_parameters.get("scrape", False))
        payload = compact(
            {
                "query": required_text(tool_parameters.get("query"), "Query"),
                "num_results": bounded_int(
                    tool_parameters.get("num_results"), 5, "Number of results", 1, 10
                ),
                "scrape": scrape,
                "formats": list_values(tool_parameters.get("formats")) if scrape else [],
                "country": tool_parameters.get("country"),
                "lang": tool_parameters.get("lang"),
                "no_cache": tool_parameters.get("no_cache", False),
            }
        )
        result = WebclawClient(
            self.runtime.credentials.get("webclaw_api_key")
        ).post("/v1/search", payload)
        yield self.create_json_message(result)
