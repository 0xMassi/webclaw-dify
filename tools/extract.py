from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.helpers import compact, json_object, required_text
from tools.webclaw_api import WebclawClient


class ExtractTool(Tool):
    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        prompt = str(tool_parameters.get("prompt") or "").strip() or None
        schema = json_object(tool_parameters.get("schema"), "JSON Schema")
        if prompt is None and schema is None:
            raise ValueError("Prompt or JSON Schema is required.")

        payload = compact(
            {
                "url": required_text(tool_parameters.get("url"), "URL"),
                "prompt": prompt,
                "schema": schema,
            }
        )
        result = WebclawClient(
            self.runtime.credentials.get("webclaw_api_key")
        ).post("/v1/extract", payload)
        yield self.create_json_message(result)
