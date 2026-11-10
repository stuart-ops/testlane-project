# ==============================================================================
# Module: bigquery-dataset
# Isolated BigQuery dataset with IAM bindings
# ==============================================================================

variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "client_name" {
  description = "Client short name for dataset naming"
  type        = string
}

variable "region" {
  description = "BigQuery dataset location"
  type        = string
}

variable "description" {
  description = "Dataset description"
  type        = string
  default     = "Client analytical warehouse"
}

variable "runtime_service_account_email" {
  description = "Service account for runtime access"
  type        = string
  default     = null
}