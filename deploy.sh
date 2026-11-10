#!/usr/bin/env bash
# Deploys the Testlane Sovereign AI website to Google Cloud Run in europe-west2.
# Usage: PROJECT_ID=testlane-chelsea-wh ./deploy.sh
set -euo pipefail
PROJECT_ID="${PROJECT_ID:-testlane-chelsea-wh}"
REGION="${REGION:-europe-west2}"
SERVICE_NAME="testlane-web"
REPO="testlane"
IMAGE="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO}/${SERVICE_NAME}:$(date +%Y%m%d-%H%M%S)"

echo "== Setting GCP Project to ${PROJECT_ID}"
gcloud config set project "${PROJECT_ID}"

echo "== Enabling APIs"
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com

echo "== Artifact Registry"
gcloud artifacts repositories describe "${REPO}" --location "${REGION}" >/dev/null 2>&1 || \
  gcloud artifacts repositories create "${REPO}" --repository-format docker --location "${REGION}"

echo "== Building and Submitting Container Image via Cloud Build"
gcloud builds submit --tag "${IMAGE}" .

echo "== Deploying Cloud Run Service (${SERVICE_NAME})"
gcloud run deploy "${SERVICE_NAME}" \
  --image "${IMAGE}" \
  --region "${REGION}" \
  --platform managed \
  --allow-unauthenticated \
  --min-instances 0 \
  --max-instances 5 \
  --memory 512Mi \
  --cpu 1 \
  --set-env-vars "DJANGO_DEBUG=False,ALLOWED_HOSTS=testlane.ai,www.testlane.ai,.a.run.app"

echo "== Done! Service URL:"
SERVICE_URL=$(gcloud run services describe "${SERVICE_NAME}" --region "${REGION}" --format "value(status.url)")
echo "${SERVICE_URL}"
echo ""
echo "== Cloudflare DNS Mapping:"
echo "1. CNAME @ -> ghs.googlehosted.com (Orange Cloud Proxied: ON)"
echo "2. CNAME www -> ghs.googlehosted.com (Orange Cloud Proxied: ON)"
