#!/bin/bash
set -e

TARGET_PROJECT="$1"

if [ -z "$TARGET_PROJECT" ]; then
  echo "Usage: ./integrate_codex.sh <path-to-your-project>"
  exit 1
fi

echo "🧠 Integrating Codex SuperLab into: $TARGET_PROJECT"

cd "$TARGET_PROJECT"

# Copy core files
cp ~/codex-superlab/ai_brain_framework.py .
cp ~/codex-superlab/enhanced_project_scanner.py .
cp ~/codex-superlab/brain_perplexity_research.py .

# Create codex_boost.sh
cat > codex_boost.sh <<'BOOST'
#!/bin/bash
set -e
echo "🧠 Running Codex SuperLab Analysis..."

python3 brain_perplexity_research.py
python3 ai_brain_framework.py
python3 enhanced_project_scanner.py

echo "✅ Codex analysis complete!"
echo "📊 Results: brain_research_results.txt"
echo "📈 Scan: project_scan.log"
BOOST

chmod +x codex_boost.sh

echo "✅ Codex SuperLab integrated!"
echo "Run: ./codex_boost.sh"
