from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.helpers import bounded_int, compact, required_text
from tools.webclaw_api import WebclawClient


class SummarizeTool(Tool):
    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        max_sentences = tool_parameters.get("max_sentences")
        payload = compact(
            {
                "url": required_text(tool_parameters.get("url"), "URL"),
                "max_sentences": bounded_int(max_sentences, 5, "Maximum sentences", 1, 50)
                if max_sentences not in (None, "")
                else None,
                "no_cache": tool_parameters.get("no_cache", False),
            }
        )
        result = WebclawClient(
            self.runtime.credentials.get("webclaw_api_key")
        ).post("/v1/summarize", payload)
        summary = result.get("summary")
        if isinstance(summary, str) and summary:
            yield self.create_text_message(summary)
        yield self.create_json_message(result)
