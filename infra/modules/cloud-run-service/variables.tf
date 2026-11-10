# ==============================================================================
# Module: cloud-run-service
# Standardised Cloud Run service with scale-to-zero, VPC egress, Cloud NAT
# ==============================================================================

variable "service_name" {
  description = "Cloud Run service name"
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

variable "max_instance_count" {
  description = "Max instances (denial-of-wallet cap)"
  type        = number
  default     = 5
}

variable "min_instance_count" {
  description = "Min instances (0 = scale-to-zero)"
  type        = number
  default     = 0
}

variable "cpu" {
  description = "CPU limit per instance"
  type        = string
  default     = "1000m"
}

variable "memory" {
  description = "Memory limit per instance"
  type        = string
  default     = "512Mi"
}

variable "ingress" {
  description = "Ingress setting"
  type        = string
  default     = "INGRESS_TRAFFIC_INTERNAL_LOAD_BALANCER"
}

variable "env_vars" {
  description = "Environment variables"
  type        = map(string)
  default     = {}
}

variable "vpc_network" {
  description = "VPC network name for VPC access"
  type        = string
  default     = null
}

variable "vpc_subnetwork" {
  description = "VPC subnetwork name for VPC access"
  type        = string
  default     = null
}

variable "service_account_email" {
  description = "Service account email for the runtime"
  type        = string
  default     = null
}

variable "allow_public_access" {
  description = "Grant allUsers invoker role (public web)"
  type        = bool
  default     = false
}

variable "timeout_seconds" {
  description = "Request timeout in seconds"
  type        = number
  default     = 300
}