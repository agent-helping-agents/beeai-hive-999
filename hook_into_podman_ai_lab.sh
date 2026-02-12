#!/usr/bin/env bash
set -euo pipefail

SERVICE_NAME="${SERVICE_NAME:-marco01-brain-engine}"
SERVICE_PORT="${SERVICE_PORT:-56625}"
BASE_URL="http://localhost:${SERVICE_PORT}"

echo "[Federation] Verifying ${SERVICE_NAME} is online at ${BASE_URL}…"

if ! podman ps --format '{{.Names}}' | grep -q "^${SERVICE_NAME}$"; then
  echo "[Federation][ERROR] Container ${SERVICE_NAME} is not running."
  echo "  Start it first, then re-run this hook script."
  exit 1
fi

# Quick health probe
if command -v curl >/dev/null 2>&1; then
  echo "[Federation] Sending a small health check request…"
  curl -s "${BASE_URL}/v1/chat/completions" \
    -H "Content-Type: application/json" \
    -d '{
          "model": "marco-o1-gguf",
          "messages": [
            {"role": "system", "content": "You are a diagnostic probe."},
            {"role": "user", "content": "Reply with a single word: OK."}
          ],
          "max_tokens": 4
        }' | sed 's/\\n/\n/g' | head -c 400 || true
  echo
else
  echo "[Federation][WARN] curl not found, skipping HTTP health check."
fi

cat <<EOF

[Federation] Hooking guidance for Podman AI Lab:

1. Open Podman Desktop → AI Lab.[web:22]
2. Go to **Models** and ensure your GGUF-based "Marco-o1-local" model is imported
   (pointing to the same GGUF you used for ${SERVICE_NAME}).[web:2][web:24]
3. Start a **Model Server** for that model (if you want AI Lab to manage its own container),
   OR keep using this standalone ${SERVICE_NAME} as an external service.

To use this existing OpenAI-style backend in tools and code:

- Base URL  : ${BASE_URL}
- Endpoint  : /v1/chat/completions
- Model name: marco-o1-gguf  (label, not enforced by llama.cpp)[web:28][web:44]

You can:
- Configure VS Code or other editors to use ${BASE_URL} as a custom OpenAI endpoint.
- Point LangChain / LangChain4j / Quarkus LangChain4j to this URL as an OpenAI-compatible model.[web:17]
- Use the generated Python client (marco_client.py) from any project on this host.

To stop the engine:
  podman stop ${SERVICE_NAME} && podman rm ${SERVICE_NAME}

[Federation] The local nexus is now ready; you may retire hostile Docker stacks at your leisure.
EOF
