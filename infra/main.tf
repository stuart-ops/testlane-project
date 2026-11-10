# ==============================================================================
# Testlane.ai Sovereign AI Infrastructure
# Google Cloud Run + Cloudflare Zero Trust + BigQuery Isolation
# ==============================================================================

terraform {
  required_version = ">= 1.5.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 4.0"
    }
  }
  backend "gcs" {
    bucket = "testlane-terraform-state"
    prefix = "sovereign-ai"
  }
}

# ==============================================================================
# CLOUD RUN — Public Website Service
# ==============================================================================

resource "google_cloud_run_v2_service" "website" {
  name     = "testlane-site"
  location = var.region
  project  = var.project_id
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    scaling {
      min_instance_count = 0
      max_instance_count = var.max_instance_count
    }

    containers {
      image = "${var.region}-docker.pkg.dev/${var.project_id}/testlane-site/testlane-site:latest"

      resources {
        limits = {
          cpu    = "1000m"
          memory = "512Mi"
        }
      }

      env {
        name  = "GCP_PROJECT"
        value = var.project_id
      }
      env {
        name  = "DJANGO_SETTINGS_MODULE"
        value = "semilattice_project.settings"
      }
      env {
        name  = "DEBUG"
        value = "False"
      }
      env {
        name  = "TRUST_CLOUDFLARE"
        value = "1"
      }
    }
  }
}

resource "google_cloud_run_v2_service_iam_member" "website_public" {
  project  = google_cloud_run_v2_service.website.project
  location = google_cloud_run_v2_service.website.location
  name     = google_cloud_run_v2_service.website.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# ==============================================================================
# CLOUDFLARE — DNS, WAF, Zero Trust
# ==============================================================================

resource "cloudflare_record" "apex" {
  zone_id = var.cloudflare_zone_id
  name    = "@"
  value   = "ghs.googlehosted.com"
  type    = "CNAME"
  proxied = true
  ttl     = 1
}

resource "cloudflare_record" "www" {
  zone_id = var.cloudflare_zone_id
  name    = "www"
  value   = "ghs.googlehosted.com"
  type    = "CNAME"
  proxied = true
  ttl     = 1
}

# ==============================================================================
# CLOUD RUN — Scheduled Nightly Jobs (per-client)
# ==============================================================================

module "client_warehouse" {
  source   = "./modules/bigquery-dataset"
  for_each = var.client_deployments

  project_id  = var.project_id
  client_name = each.key
  region      = var.region
}

# ==============================================================================
# OUTPUTS
# ==============================================================================

output "website_url" {
  value = "https://testlane.ai"
}

output "project_id" {
  value = var.project_id
}