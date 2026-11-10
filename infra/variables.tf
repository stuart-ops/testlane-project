# ==============================================================================
# VARIABLES — Values in terraform.tfvars (never commit to git)
# ==============================================================================

variable "project_id" {
  description = "GCP Project ID for the Testlane Sovereign AI deployment"
  type        = string
}

variable "region" {
  description = "GCP Region (London default)"
  type        = string
  default     = "europe-west2"
}

variable "root_domain" {
  description = "Base domain for DNS"
  type        = string
  default     = "testlane.ai"
}

variable "cloudflare_zone_id" {
  description = "Cloudflare Zone ID for testlane.ai"
  type        = string
  sensitive   = true
}

variable "max_instance_count" {
  description = "Denial-of-wallet cap: max Cloud Run instances"
  type        = number
  default     = 5
}

variable "client_deployments" {
  description = "Map of client deployments for per-client infrastructure"
  type = map(object({
    subdomain              = string
    allowed_emails         = string
    max_instance_count     = optional(number, 2)
    enable_scheduled_sync  = optional(bool, true)
    sync_schedule          = optional(string, "0 5 * * *")
  }))
  default = {}
}