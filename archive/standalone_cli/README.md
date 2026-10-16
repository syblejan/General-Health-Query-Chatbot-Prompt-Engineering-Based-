# Archived assistant-added CLI

This folder preserves the later standalone Mistral Small CLI, tests and workflows. It is not the author's original Colab implementation. The repository root README describes the original source and its historical demonstrations.

The workflow files here are archival copies; GitHub Actions does not load them from this location. Offline tests can be run from this folder with `python -m unittest discover -s tests -v`. The CLI and live smoke script require an API key; their real API checks previously stopped on HTTP 429 responses. Do not treat those runs as successful original-project tests.
