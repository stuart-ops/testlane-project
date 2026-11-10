# ==============================================================================
# Module: bigquery-dataset — main resources
# ==============================================================================

resource "google_bigquery_dataset" "warehouse" {
  dataset_id    = "${var.client_name}_mart"
  project       = var.project_id
  location      = var.region
  friendly_name = "${var.client_name} Reporting Mart"
  description   = var.description

  access {
    role          = "OWNER"
    special_group = "projectOwners"
  }
}

resource "google_bigquery_dataset" "raw" {
  dataset_id    = var.client_name
  project       = var.project_id
  location      = var.region
  friendly_name = "${var.client_name} Raw Data"
  description   = "Raw ingested data for ${var.client_name}"

  access {
    role          = "OWNER"
    special_group = "projectOwners"
  }
}

resource "google_project_iam_member" "runtime_data_owner" {
  count   = var.runtime_service_account_email != null ? 1 : 0
  project = var.project_id
  role    = "roles/bigquery.dataOwner"
  member  = "serviceAccount:${var.runtime_service_account_email}"

  condition {
    title       = "Scope to ${var.client_name} datasets"
    expression  = "resource.name.startsWith(\"projects/${var.project_id}/datasets/${var.client_name}\")"
  }
}

output "dataset_id" {
  value = google_bigquery_dataset.warehouse.dataset_id
}

output "raw_dataset_id" {
  value = google_bigquery_dataset.raw.dataset_id
}