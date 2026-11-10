# ==============================================================================
# OUTPUTS — Printed after terraform apply
# ==============================================================================

output "testlane_ai_url" {
  description = "Public website URL"
  value       = "https://${var.root_domain}"
}

output "gcp_project" {
  description = "Active GCP project"
  value       = var.project_id
}

output "gcp_region" {
  description = "Active GCP region"
  value       = var.region
}

output "cloud_run_service_name" {
  description = "Cloud Run service name"
  value       = google_cloud_run_v2_service.website.name
}