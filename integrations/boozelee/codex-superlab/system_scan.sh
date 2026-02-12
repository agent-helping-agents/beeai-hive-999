#!/bin/bash
mkdir -p "$HOME/my-gemini-cli"
cd "$HOME/my-gemini-cli" || { echo "Failed to navigate to ~/my-gemini-cli"; exit 1; }
echo "System scan at $(date)" >> brain_research_results.txt
echo "Compute Engine instances..." >> brain_research_results.txt
gcloud compute instances list --project=mythicnode >> brain_research_results.txt
echo "Cloud Storage buckets..." >> brain_research_results.txt
gcloud storage ls --project=mythicnode >> brain_research_results.txt
for BUCKET in gs://my-gcp-tfstate-bucket gs://my-gcp-tfstate-bucket-1760864481; do
  echo "Files in $BUCKET:" >> brain_research_results.txt
  gcloud storage ls -r "$BUCKET" >> brain_research_results.txt || echo "Failed to list $BUCKET" >> brain_research_results.txt
done
echo "Artifact Registry repositories..." >> brain_research_results.txt
gcloud artifacts repositories list --project=mythicnode >> brain_research_results.txt
cat brain_research_results.txt
