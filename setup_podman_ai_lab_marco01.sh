#!/usr/bin/env bash
set -euo pipefail

### 0. Galactic preamble #######################################################
echo "[Federation] Initializing local AI stronghold with Podman AI Lab + Marco-o1…"

### 1. System check ###########################################################
echo "[Federation] Detecting system capabilities…"

CPU_INFO=$(lscpu | sed -n '1,5p' || true)
MEM_INFO=$(grep MemTotal /proc/meminfo || true)
GPU_INFO=$(lspci | grep -Ei 'vga|3d|nvidia|amd|intel' || true)
DISK_INFO=$(df -h / | tail -n 1 || true)

echo "---- CPU ----"
echo "$CPU_INFO"
echo "---- RAM ----"
echo "$MEM_INFO"
echo "---- GPU ----"
echo "$GPU_INFO"
echo "---- DISK / ----"
echo "$DISK_INFO"

### 2. Install Podman engine if missing #######################################
if ! command -v podman >/dev/null 2>&1; then
  echo "[Federation] Podman not found, attempting installation (you may be prompted for sudo)…"
  if command -v apt >/dev/null 2>&1; then
    sudo apt update
    sudo apt install -y podman
  elif command -v dnf >/dev/null 2>&1; then
    sudo dnf install -y podman
  elif command -v pacman >/dev/null 2>&1; then
    sudo pacman -Sy --noconfirm podman
  else
    echo "[Federation][WARN] Unknown package manager. Install Podman manually, then re-run this script."
  fi
else
  echo "[Federation] Podman already installed."
fi

### 3. Install Podman Desktop via Flatpak #####################################
if ! flatpak list | grep -q "io.podman_desktop.PodmanDesktop"; then
  echo "[Federation] Installing Podman Desktop via Flatpak…"
  flatpak remote-add --if-not-exists --user flathub https://flathub.org/repo/flathub.flatpakrepo
  flatpak install -y --user flathub io.podman_desktop.PodmanDesktop
else
  echo "[Federation] Podman Desktop already installed."
fi

### 4. Launch Podman Desktop once #############################################
echo "[Federation] Launching Podman Desktop (first run may take a bit)…"
flatpak run io.podman_desktop.PodmanDesktop &>/dev/null & disown || true

echo "[Federation] Open Podman Desktop UI, go to Extensions → Catalog → install 'Podman AI Lab' extension."
echo "[Federation] Press ENTER after you have installed the AI Lab extension from the GUI."
read -r _

### 5. Prepare Marco-o1 model directory #######################################
MARCO_DIR="${HOME}/.local/share/podman-ai-lab/models/marco-o1"
mkdir -p "${MARCO_DIR}"

echo "[Federation] Downloading recommended Marco-o1 GGUF (Q4_K_M as a strong general-purpose choice)…"
cd "${MARCO_DIR}"

# Adjust the filename if the upstream repo changes:
GGUF_URL="https://huggingface.co/QuantFactory/Marco-o1-GGUF/resolve/main/Marco-o1-Q4_K_M.gguf"
GGUF_FILE="Marco-o1-Q4_K_M.gguf"

if [ ! -f "${GGUF_FILE}" ]; then
  if command -v wget >/dev/null 2>&1; then
    wget -O "${GGUF_FILE}" "${GGUF_URL}"
  elif command -v curl >/dev/null 2>&1; then
    curl -L "${GGUF_URL}" -o "${GGUF_FILE}"
  else
    echo "[Federation][ERROR] Neither wget nor curl found. Install one, then re-run."
    exit 1
  fi
else
  echo "[Federation] GGUF file already present: ${GGUF_FILE}"
fi

### 6. Launch a llama.cpp-style model service via Podman ######################
# This uses a generic llama.cpp image compatible with GGUF and an OpenAI API.
# Podman AI Lab itself uses similar containers behind the scenes.[web:19][web:2]

SERVICE_NAME="marco01-brain-engine"
SERVICE_PORT="${1:-56625}"

echo "[Federation] Starting local Marco-o1 model service with Podman…"
podman run -d \
  --name "${SERVICE_NAME}" \
  -p "${SERVICE_PORT}:8080" \
  -v "${MARCO_DIR}:/models:Z" \
  ghcr.io/ggerganov/llama.cpp:full \
  --model /models/"${GGUF_FILE}" \
  --ctx-size 4096 \
  --threads "$(nproc)" \
  --host 0.0.0.0 \
  --port 8080 \
  --api-openai

echo "[Federation] Marco-o1 service should now be reachable at:"
echo "  http://localhost:${SERVICE_PORT}/v1/chat/completions"
echo "[Federation] This endpoint speaks the OpenAI Chat Completions dialect (chat models only).[web:2][web:17]"

### 7. Test the local brain engine ###########################################
echo "[Federation] Testing the local brain engine with a sample request…"

cat > /tmp/test_marco01_request.json <<'EOF'
{
  "model": "marco-o1-gguf",
  "messages": [
    {"role": "system", "content": "You are a precise Galactic Federation reasoning engine."},
    {"role": "user", "content": "Briefly describe your mission in one sentence."}
  ],
  "max_tokens": 128,
  "temperature": 0.2
}
EOF

if command -v curl >/dev/null 2>&1; then
  curl -s http://localhost:${SERVICE_PORT}/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d @/tmp/test_marco01_request.json | sed 's/\\n/\n/g' | head -c 800
  echo
else
  echo "[Federation][WARN] curl not found, skipping automatic test."
fi

echo
echo "[Federation] Setup complete. Use this endpoint in your tools instead of Dockerized OpenAI clones."echo "[Federation] To stop the service: podman stop ${SERVICE_NAME} && podman rm ${SERVICE_NAME}"
