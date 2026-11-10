# ==============================================================================
# Module: cloudflare-perimeter
# DNS record with Orange Cloud, WAF rules
# ==============================================================================

variable "zone_id" {
  description = "Cloudflare Zone ID"
  type        = string
  sensitive   = true
}

variable "subdomain" {
  description = "Subdomain (use @ for apex)"
  type        = string
}

variable "target" {
  description = "DNS target (e.g. ghs.googlehosted.com)"
  type        = string
  default     = "ghs.googlehosted.com"
}

variable "proxied" {
  description = "Orange Cloud: proxy through Cloudflare"
  type        = bool
  default     = true
}