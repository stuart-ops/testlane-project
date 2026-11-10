# ==============================================================================
# Module: cloud-run-job
# Standardised scheduled Cloud Run job with Cloud Scheduler trigger
# ==============================================================================

variable "job_name" {
  description = "Cloud Run job name"
  type        = string
}

variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "GCP Region"
  type        = string
}

variable "image" {
  description = "Container image URL"
  type        = string
}

variable "command" {
  description = "Container entrypoint command"
  type        = list(string)
  default     = null
}

variable "args" {
  description = "Container entrypoint args"
  type        = list(string)
  default     = null
}

variable "cpu" {
  description = "CPU limit"
  type        = string
  default     = "1000m"
}

variable "memory" {
  description = "Memory limit"
  type        = string
  default     = "1Gi"
}

variable "timeout_seconds" {
  description = "Job timeout in seconds"
  type        = number
  default     = 3600
}

variable "max_retries" {
  description = "Max retries on failure"
  type        = number
  default     = 0
}

variable "service_account_email" {
  description = "Service account email"
  type        = string
}

variable "schedule" {
  description = "Cron schedule expression"
  type        = string
  default     = "0 5 * * *"
}

variable "time_zone" {
  description = "Scheduler time zone"
  type        = string
  default     = "Europe/London"
}

variable "scheduler_service_account_email" {
  description = "Service account for Cloud Scheduler"
  type        = string
}

variable "env_vars" {
  description = "Environment variables"
  type        = map(string)
  default     = {}
}