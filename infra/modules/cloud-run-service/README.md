# Module: cloud-run-service

Standardised Cloud Run service with scale-to-zero, VPC egress, Cloud NAT, and configurable IAM.

## Usage

```hcl
module "dashboard" {
  source = "./modules/cloud-run-service"

  service_name        = "my-dash"
  project_id          = "my-project"
  region              = "europe-west2"
  image               = "europe-west2-docker.pkg.dev/my-project/my-dash/my-dash:latest"
  max_instance_count  = 5
  ingress             = "INGRESS_TRAFFIC_INTERNAL_LOAD_BALANCER"
  allow_public_access = false

  env_vars = {
    GCP_PROJECT = "my-project"
  }

  vpc_network           = google_compute_network.vpc.name
  vpc_subnetwork        = google_compute_subnetwork.subnet.name
  service_account_email = google_service_account.runtime.email
}
```

## Key Security Settings

- `max_instance_count` is mandatory (denial-of-wallet).
- `ingress` should be `INGRESS_TRAFFIC_INTERNAL_LOAD_BALANCER` for protected services.
- Set `allow_public_access = true` only for public-facing websites behind Cloudflare.