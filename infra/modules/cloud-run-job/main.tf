# ==============================================================================
# Module: cloud-run-job — main resources
# ==============================================================================

resource "google_cloud_run_v2_job" "job" {
  name     = var.job_name
  location = var.region
  project  = var.project_id

  template {
    task_count = 1

    template {
      containers {
        image = var.image

        dynamic "command" {
          for_each = var.command != null ? [1] : []
          content {
            command = var.command
          }
        }

        dynamic "args" {
          for_each = var.args != null ? [1] : []
          content {
            args = var.args
          }
        }

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

      timeout          = "${var.timeout_seconds}s"
      max_retries      = var.max_retries
      service_account  = var.service_account_email
    }
  }
}

resource "google_cloud_scheduler_job" "trigger" {
  name        = "${var.job_name}-trigger"
  description = "Trigger ${var.job_name} on schedule: ${var.schedule}"
  schedule    = var.schedule
  time_zone   = var.time_zone
  region      = var.region
  project     = var.project_id

  http_target {
    http_method = "POST"
    uri         = "https://${var.region}-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/${var.project_id}/jobs/${google_cloud_run_v2_job.job.name}:run"

    oauth_token {
      service_account_email = var.scheduler_service_account_email
    }
  }
}

output "job_name" {
  value = google_cloud_run_v2_job.job.name
}