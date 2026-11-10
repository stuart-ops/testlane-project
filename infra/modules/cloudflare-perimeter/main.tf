# ==============================================================================
# Module: cloudflare-perimeter — main resources
# ==============================================================================

resource "cloudflare_record" "dns" {
  zone_id = var.zone_id
  name    = var.subdomain
  value   = var.target
  type    = "CNAME"
  proxied = var.proxied
  ttl     = 1
}

output "fqdn" {
  value = var.subdomain == "@" ? cloudflare_record.dns.zone_id : "${cloudflare_record.dns.name}.${cloudflare_record.dns.zone_id}"
}

output "record_name" {
  value = cloudflare_record.dns.name
}