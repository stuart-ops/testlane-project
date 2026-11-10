# ==============================================================================
# Module: cloud-run-service — main resources
# ==============================================================================

resource "google_cloud_run_v2_service" "service" {
  name     = var.service_name
  location = var.region
  project  = var.project_id
  ingress  = var.ingress

  template {
    scaling {
      min_instance_count = var.min_instance_count
      max_instance_count = var.max_instance_count
    }

    timeout = "${var.timeout_seconds}s"

    containers {
      image = var.image

      resources {
        limits = {
          cpu    = var.cpu
          memory = var.memory
        }
      }

      dynamic "env" {
        for_each = var.env_vars
        content {
          name  = env.key
          value = env.value
        }
      }
    }

    dynamic "vpc_access" {
      for_each = var.vpc_network != null ? [1] : []
      content {
        network_interface {
          network    = var.vpc_network
          subnetwork = var.vpc_subnetwork
        }
        egress = "ALL_TRAFFIC"
      }
    }

    dynamic "service_account" {
      for_each = var.service_account_email != null ? [1] : []
      content {
        email = var.service_account_email
      }
    }
  }
}

resource "google_cloud_run_v2_service_iam_member" "public_access" {
  count    = var.allow_public_access ? 1 : 0
  project  = google_cloud_run_v2_service.service.project
  location = google_cloud_run_v2_service.service.location
  name     = google_cloud_run_v2_service.service.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

output "service_url" {
  value = google_cloud_run_v2_service.service.uri
}

output "service_name" {
  value = google_cloud_run_v2_service.service.name
}