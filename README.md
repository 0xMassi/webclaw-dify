# Webclaw for Dify

Webclaw gives Dify agents, chatflows, and workflows reliable web scraping,
search, site mapping, summarization, batch extraction, and structured data
extraction through the hosted Webclaw API.

## Tools

- **Scrape:** turn one URL into clean Markdown, text, or LLM-ready content.
- **Search:** search the web, with content extraction when requested.
- **Map:** discover URLs published by a website.
- **Extract:** extract structured data from a page using a prompt or JSON Schema.
- **Summarize:** summarize a webpage with an optional sentence limit.
- **Batch:** scrape up to 50 URLs in one workflow step.

## Configuration

1. Create a Webclaw API key at <https://webclaw.io/dashboard/api-keys>.
2. Install the plugin in Dify.
3. Open **Plugins → Webclaw → Authorize**.
4. Paste the API key and save.

Dify sends the key to `https://api.webclaw.io` as a Bearer token. The plugin
uses no other destination.

## Connection and security

The Dify runtime needs outbound HTTPS access to `api.webclaw.io`. The plugin
connects only to that fixed API endpoint; Webclaw performs requests to the URLs
selected by the user. The hosted API rejects private and internal destinations,
including redirects to them, before fetching content. Requests time out after
120 seconds, and credentials are never included in tool output or error logs.

## Local development

This plugin requires Python 3.12 and `uv`.

```bash
cp .env.example .env
uv sync
uv run python -m main
```

Get the remote debugging host, port, and key from Dify's Plugin Management
page, then replace the placeholders in `.env`.

Run the tests with:

```bash
uv run pytest
```

Marketplace-compatible dependencies are also listed in `requirements.txt`.

Package the plugin from the parent directory with:

```bash
dify plugin package ./webclaw-dify
```

## Privacy

See [PRIVACY.md](PRIVACY.md) and the
[Webclaw Privacy Policy](https://webclaw.io/privacy).

## Support

Open an issue at <https://github.com/0xMassi/webclaw-dify/issues>.
