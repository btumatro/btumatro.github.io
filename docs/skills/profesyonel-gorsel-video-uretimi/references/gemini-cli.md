# Gemini API CLI

The Gemini API CLI repository provides an experimental command-line client for the Interactions API. It is installed at /Users/wildgenie/.local/bin/gemini-api from upstream commit 895be4d. The user wants it used where it fits; its experimental status is a constraint to communicate, not a reason to avoid it categorically.

- Confirm commands with gemini-api --help and gemini-api video --help. CLI commands and capabilities can change; inspect the installed binary rather than relying on this snapshot.
- Use --usage for a machine-readable command surface and --schema for request bodies.
- Before a paid/network request, preview with --dry-run.
- Use GEMINI_API_KEY from the environment; never print it or place it in shell history, prompts, files or metadata.
- Long generation may support --async and later status polling; confirm flags against the installed binary.
- Check output path, use ffprobe, inspect the generated frames and assemble with the requested editor.
- Do not run configure/keychain writes unless the user asks. Do not assume the CLI and SDK have identical support.
- Prefer this CLI when its currently exposed command supports the requested operation and output. Otherwise use the official SDK/API or another available tool; do not claim parity or production readiness.

Upstream: https://github.com/google-gemini/gemini-api-cli
