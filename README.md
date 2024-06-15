# GCP-Terraform-App-Deployment

---

![image](./img/readme.png)

---

## Deployment of a simple python application on Google Cloud Run using Terraform

Terraform is an open-source infrastructure as code (IaC) tool developed by HashiCorp. It’s designed to help users define, provision, and manage infrastructure resources and services in a declarative and efficient manner. Terraform enables version control, collaboration, and documentation of infrastructure changes, making it easier to track and manage infrastructure configurations over time.

It supports multiple cloud providers and can manage resources across different cloud environments and on-premises infrastructure, promoting flexibility and avoiding vendor lock-in. By automating the provisioning and configuring of infrastructure, Terraform reduces the risk of manual errors and ensures that environments are consistent and reproducible. Terraform can manage both small-scale and large-scale infrastructures, making it suitable for projects of varying sizes and complexities.

In this project, we're creating a simple infrastructure on GCP, including a state bucket, clusters, and nodes. we’ll also push a Docker image to the Artifact Registry and will deploy a simple application on Google Cloud Run using Terraform. To achieve this, we’ll write scripts in Terraform files that are already created for we as .tf files in the /usercode directory of this project. For wer ease, the application to be deployed on Cloud Run is also available in the /usercode/Application directory. To complete this project, we’ll execute the commands in the terminal, where all the utilities are already installed.

---

To run the application:

```bash
cd Application
python3 manage.py runserver 0.0.0.0:8080
```

we can stop the server by pressing `Ctrl + C`

---

### Prepare Docker image

Prepare a Docker image for the web application that will be deployed on Cloud Run by the end of this project:

1. Log in to wer Docker Hub using the CLI command.
2. Build the Docker image using the Dockerfile file available in the /usercode/application/ directory.
3. Push the image to wer Docker Hub repository.

```bash
docker login -u <wer username>
cd /usercode/Application
docker build -t <wer repository name>/<desired image name>:<desired tag> .
docker push <wer repository name>/<desired image name>:<desired tag>
```

---

### Create billing account and service account

1. Use the following command to log in to the gcloud CLI:

   ```bash
   gcloud auth login --no-launch-browser
   Note: After running the command, follow the instructions provided in the terminal.
   ```

2. Use the following code to create a project:

   ```bash
   export PROJECT_ID=<Project ID>
   gcloud projects create $PROJECT_ID
   gcloud config set project $PROJECT_ID
   gcloud projects list
   Use the following code to create the service account:
   gcloud iam service-accounts create <service_account_name> --project $PROJECT_ID --display-name <display_name>
   ```

---

### Create a service account key pair

To access and interact with GCP resources securely, gcloud uses a service account key pair consisting of a public key and a private key. The private key is used by the service account to authenticate itself to GCP services securely, and the public key is used by GCP services to verify the authenticity of requests made by the service account.

These keys are generated as a JSON file that resides inside the working directory to authenticate the service account with gcloud. In this task, we’ll create a key pair for the service account and assign sufficient permission to it for accessing and creating resources in GCP. To create a key pair, we’ll use the service account that was created in Task 2.

To do this, perform the following tasks:

Once the keys are generated, add appropriate policy bindings on the service account.

Use the following code to create the key pair:

```bash
export SERVICE_ACCOUNT=<weR_SERVICE_ACCOUNT>@${PROJECT_ID}.iam.gserviceaccount.com
gcloud iam service-accounts keys create account.json --iam-account $SERVICE_ACCOUNT --project $PROJECT_ID
```

List the keys using the following command:

```bash
gcloud iam service-accounts keys list --iam-account $SERVICE_ACCOUNT --project $PROJECT_ID
```

Bind the permission to service account using the following command:

```bash
gcloud projects add-iam-policy-binding $PROJECT_ID --member serviceAccount:$SERVICE_ACCOUNT --role roles/owner
```

---

### Set up GKE cluster

Enable Kubernetes Engine API using the following command:

```bash
gcloud services enable container.googleapis.com
```

Use the following command to find validMasterVersions:

```bash
gcloud container get-server-config --region <wer_region_name> --project $PROJECT_ID | grep -A 1 validMasterVersion
```

Add the following code to the main.tf file:

```tf
resource "google_container_cluster" "primary" {
   name     = var.cluster_name
   location = var.region
   remove_default_node_pool = true
   initial_node_count = var.min_node_count
   deletion_protection = false

}
```

Since nothing is to be changed in the existing infrastructure, execute the terraform apply command and enter “yes” when prompted.

Note: After executing terraform apply, Terraform will provide a long list of resources to be added. The process will take some time to create the cluster.

If the workspace disconnects, reconnect and log in again to gcloud. Also note that in case of disconnectivity during cluster creation, the process will continue deployment on gcloud.

---

### Node Pools

Nodes represent a pool of VMs that act as workers within a GKE cluster. These nodes are used to run containerized workloads orchestrated by Kubernetes. we can define a google_container_node_pool resource to create and configure a group of worker nodes within a GKE cluster, setting properties like machine type, disk type, and the number of nodes.

---

### Set up connection with workers

Now that the cluster and the nodes have been deployed, it’s time to connect with the cluster to find more information about the nodes. In this task, we’ll establish a connection to the cluster. To complete this task, perform the following steps:

Set the KUBECONFIG environment variable to specify the location where the Kubernetes configuration file should be created.

- Connect with the cluster using the gcloud container clusters command.
- Create admin role bindings with the cluster using the kubectl create clusterrolebinding command.
- Find the number of nodes running in the cluster at present.

```bash
export KUBECONFIG=$PWD/kubeconfig


gcloud container clusters get-credentials $(terraform output --raw cluster_name) --project $(terraform output --raw project_id) --region $(terraform output --raw region)

kubectl create clusterrolebinding cluster-admin-binding --clusterrole cluster-admin --user $(gcloud config get-value account)

kubectl get nodes
```

### Artifact Registry

The Artifact Registry is a managed repository service provided by Google Cloud. It is used for storing, managing, and versioning software artifacts, dependencies, and container images. In this task, we’ll create an Artifact Repository to push the containerized image created earlier in Task 1. For this purpose, we’ll also need to bind the IAM policy to the Artifact Repository and assign roles to let we push the container to the newly created repository.

```bash

```

### Push image to the artifact registry

Now that the Artifact Registry has been created and sufficient roles have been assigned to access it, you’ll push the image created in Task 1 to the repository. It’s important to note that to deploy the application to Cloud Run and to configure Docker with gcloud, you’ll need to perform authentication with gcloud first.

This is done by authorizing access to Google Cloud services using Application Default Credentials (ADC), which provide a simple way for applications and services running on Google Cloud to obtain credentials for authenticating with Google APIs.

To complete this task, perform the following steps:

- Authenticate with gcloud application.
- Configure gcloud for Docker authentication with the desired image type for pushing the image.
- Pull the image from your Docker Hub repository.
- Tag the image with an appropriate name, pointing to its location on the Artifact Registry.
- Push the image to the Artifact Registry.

```bash
gcloud auth application-default login

gcloud auth configure-docker us-central1-docker.pkg.dev

docker image pull ovokpus/terraform-gcp:0.0.1

docker image tag ovokpus/terraform-gcp:0.0.1 us-central1-docker.pkg.dev/$PROJECT_ID/cloud-run-artifact-regsitry/terraform-gcp:0.0.1

docker push us-central1-docker.pkg.dev/$PROJECT_ID/cloud-run-artifact-regsitry/terraform-gcp:0.0.1
```

### Cloud Run API

The Cloud Run API allows you to interact programmatically with Cloud Run, a fully managed compute platform that enables you to deploy and run containerized applications in a serverless environment. The API allows you to perform various operations, such as deploying new services, managing revisions, and scaling applications. It’s important to enable the API before deploying the resource on Cloud Run.

### Deploy image

In this task, you’ll deploy the image pushed on the Artifact Registry to Cloud Run. To perform this task, complete the following steps:

1. Use the google_cloud_run_service block resource along with the address of the image from the Artifact Repository to deploy on Cloud Run.
2. Fetch the policy binding information about the members that are allowed to send invoke requests to Cloud Run using the data block called google_iam_policy.
3. Assign public access to the deployed services using the resource google_cloud_run_service_iam_policy block.
4. Apply the changes.

### Destroy all Resources

Using Terraform to manage infrastructure allows for repeatability and automation. It also ensures that you can remove resources cleanly when they’re no longer required, reducing infrastructure costs and maintaining good resource hygiene. Destroying resources is useful when you want to decommission or delete all the resources defined in your Terraform configuration files and return your environment to its previous state or to clean up resources that are no longer needed. To complete this task, perform the following operations:

- Delete the Kubernetes cluster.
- Destroy the Terraform infrastructure created in this project.
- Delete the Google Cloud project.
