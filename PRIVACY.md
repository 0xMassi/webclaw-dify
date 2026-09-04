# Webclaw for Dify Privacy Policy

Last updated: September 4, 2026

## Data handled by the plugin

The plugin sends the following data to the Webclaw API after a user runs a tool:

- the configured Webclaw API key;
- URLs, search queries, extraction prompts, JSON Schemas, and tool options
  supplied by the user or a Dify workflow.

The plugin does not add analytics, advertising identifiers, cookies, or its own
persistent storage. It does not write the API key to logs. Dify stores the
credential using its secret-input mechanism.

## Purpose and destination

The data is transmitted to `https://api.webclaw.io` to perform the requested
scraping, search, mapping, extraction, summarization, or batch operation.
Webclaw may fetch the user-selected websites, whose operators can receive
ordinary web request data such as request headers and the source network
address. Results are returned to the requesting Dify instance.

Webclaw's processing, subprocessors, retention, security, and deletion terms
are described in the [Webclaw Privacy Policy](https://webclaw.io/privacy).

## Sharing

The plugin sends data to Webclaw and the websites selected by the user. It
sends data nowhere else. Webclaw lists its service providers in the Webclaw
Privacy Policy linked above.

## User controls

Users control which data they submit through each tool and can remove the
Webclaw credential from Dify at any time. Account and deletion requests can be
sent to privacy@webclaw.io.
