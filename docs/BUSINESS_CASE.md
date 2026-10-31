# Business case: GCP Terraform App Deployment

**Repeatable Google Cloud infrastructure for a small web app, defined in code.**

## Who buys this

The buyer is a technical founder or the one-person platform team at a small company that deploys a web app to Google Cloud by clicking through the console. The users are the developers who need a staging or production environment that matches the last one.

## The problem and what it costs

Infrastructure set up by hand can't be reviewed, repeated or rebuilt quickly. When the one person who knows the setup is away, nobody can recreate the environment. Terraform turns that setup into code that can be reviewed in a pull request and applied the same way every time.

For a small app the hosting is cheap. Cloud Run's monthly free tier includes **180,000 vCPU-seconds, 360,000 GiB-seconds and 2 million requests** for request-billed services ([Google Cloud Run pricing](https://cloud.google.com/run/pricing)). The cost that matters is people's time.

## How the repo solves it

| Need | What in the repo does it |
|---|---|
| Shared Terraform state | A GCS state bucket (`main.tf`) |
| A place for images | Artifact Registry |
| Serverless hosting | A Cloud Run service running the Django app in `Application/` |
| Kubernetes, when needed | A GKE cluster and node pool in the same configuration |
| Inputs and outputs | `variables.tf` and `output.tf` |

The README labels this as a guided project. A reworked, multi-cloud version of these modules now lives in [ovokpus/GKE-Cluster-Management](https://github.com/ovokpus/GKE-Cluster-Management/tree/main/terraform).

## Use-case scenarios

All of these organisations are fictional.

1. **A two-developer start-up** creates a staging environment identical to production with one `terraform apply`, and removes it with `terraform destroy` after a demo.
2. **An agency launching client microsites** reuses the same configuration for each client, changing only the variables.
3. **A team going through a security review** points the reviewer at the Terraform files instead of screenshots of the console.

## ROI: a worked model (illustrative)

These figures are **illustrative assumptions**.

| Input | Value | Basis |
|---|---|---|
| Environments created or rebuilt a year | 6 | Assumption |
| Developer hours to set one up by hand | 8 | Assumption |
| Developer hours with Terraform, after the first time | 1 | Assumption |
| Developer hourly cost | US$83 | BLS May 2024 median for software developers, $63.98 an hour ([BLS OEWS](https://www.bls.gov/news.release/archives/ocwage_04022025.pdf)). Multiplied by an assumed 1.3. |

Saving: 6 × 7 hours = **42 hours, about US$3,500 a year**, plus fewer configuration mistakes. That is small, which is honest for a project this size.

## Path to production

1. Use the reworked modules in GKE-Cluster-Management instead of this configuration.
2. Authenticate with workload identity federation, not a service-account key file. The original `main.tf` refers to an `account.json` file, which should never be committed.
3. Add CI with `terraform fmt`, `validate`, `tflint` and a security scan, and require review before any apply.

## Risks and limits

- **This is the weakest case in the set.** It is a guided lab project, so the business value comes from the pattern, not from this code.
- A `kubeconfig` file is committed. It holds no secret, but it does expose a cluster endpoint, and it shouldn't be in source control.
- Running GKE alongside Cloud Run costs money even when idle. Destroy lab environments.

## Sources

- Google Cloud, Cloud Run pricing: https://cloud.google.com/run/pricing
- U.S. Bureau of Labor Statistics, OEWS May 2024 (software developers): https://www.bls.gov/news.release/archives/ocwage_04022025.pdf
