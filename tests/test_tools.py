from types import SimpleNamespace

import pytest

from tools.batch import BatchTool
from tools.extract import ExtractTool
from tools.map import MapTool
from tools.scrape import ScrapeTool
from tools.search import SearchTool
from tools.summarize import SummarizeTool
from tools.webclaw_api import WebclawClient


def make_tool(tool_class):
    tool = object.__new__(tool_class)
    tool.runtime = SimpleNamespace(credentials={"webclaw_api_key": "wc_test"})
    tool.create_json_message = lambda value: {"type": "json", "value": value}
    tool.create_text_message = lambda value: {"type": "text", "value": value}
    return tool


def test_all_tools_build_expected_api_requests(monkeypatch):
    calls = []

    def fake_post(self, path, payload):
        calls.append((path, payload))
        if path == "/v1/scrape":
            return {"markdown": "# Example"}
        if path == "/v1/summarize":
            return {"summary": "Short summary."}
        return {"ok": True}

    monkeypatch.setattr(WebclawClient, "post", fake_post)

    assert list(
        make_tool(ScrapeTool)._invoke(
            {
                "url": "https://example.com",
                "formats": ["markdown"],
                "only_main_content": True,
            }
        )
    ) == [
        {"type": "text", "value": "# Example"},
        {"type": "json", "value": {"markdown": "# Example"}},
    ]
    list(make_tool(SearchTool)._invoke({"query": "web extraction", "num_results": 3}))
    list(make_tool(MapTool)._invoke({"url": "https://example.com", "limit": 25}))
    list(
        make_tool(ExtractTool)._invoke(
            {"url": "https://example.com", "schema": '{"type":"object"}'}
        )
    )
    assert list(
        make_tool(SummarizeTool)._invoke(
            {"url": "https://example.com", "max_sentences": 3}
        )
    ) == [
        {"type": "text", "value": "Short summary."},
        {"type": "json", "value": {"summary": "Short summary."}},
    ]
    list(
        make_tool(BatchTool)._invoke(
            {"urls": "https://a.example,\nhttps://b.example", "concurrency": 2}
        )
    )

    assert calls == [
        (
            "/v1/scrape",
            {
                "url": "https://example.com",
                "formats": ["markdown"],
                "only_main_content": True,
                "no_cache": False,
            },
        ),
        (
            "/v1/search",
            {
                "query": "web extraction",
                "num_results": 3,
                "scrape": False,
                "no_cache": False,
            },
        ),
        ("/v1/map", {"url": "https://example.com", "limit": 25}),
        (
            "/v1/extract",
            {"url": "https://example.com", "schema": {"type": "object"}},
        ),
        (
            "/v1/summarize",
            {
                "url": "https://example.com",
                "max_sentences": 3,
                "no_cache": False,
            },
        ),
        (
            "/v1/batch",
            {
                "urls": ["https://a.example", "https://b.example"],
                "formats": ["markdown"],
                "concurrency": 2,
                "no_cache": False,
            },
        ),
    ]


def test_extract_requires_a_prompt_or_schema():
    with pytest.raises(ValueError, match="Prompt or JSON Schema"):
        list(make_tool(ExtractTool)._invoke({"url": "https://example.com"}))


def test_batch_caps_dify_invocations_at_fifty_urls():
    urls = ",".join(f"https://{index}.example" for index in range(51))
    with pytest.raises(ValueError, match="at most 50"):
        list(make_tool(BatchTool)._invoke({"urls": urls}))
