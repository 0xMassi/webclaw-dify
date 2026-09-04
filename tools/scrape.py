from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.helpers import compact, list_values, required_text
from tools.webclaw_api import WebclawClient


class ScrapeTool(Tool):
    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        formats = list_values(tool_parameters.get("formats")) or ["markdown"]
        payload = compact(
            {
                "url": required_text(tool_parameters.get("url"), "URL"),
                "formats": formats,
                "include_selectors": list_values(tool_parameters.get("include_selectors")),
                "exclude_selectors": list_values(tool_parameters.get("exclude_selectors")),
                "only_main_content": tool_parameters.get("only_main_content", False),
                "no_cache": tool_parameters.get("no_cache", False),
            }
        )
        result = WebclawClient(
            self.runtime.credentials.get("webclaw_api_key")
        ).post("/v1/scrape", payload)

        for format_name in ("markdown", "text", "llm"):
            content = result.get(format_name)
            if format_name in formats and isinstance(content, str) and content:
                yield self.create_text_message(content)
                break
        yield self.create_json_message(result)
