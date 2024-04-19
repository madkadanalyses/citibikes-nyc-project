variable "credentials" {
  description = "My Credentials"
  default     = "~/dtc-de-project-32a2d69c356c.json"
  #ex: if you have a directory where this file is called keys with your service account json file
  #saved there as my-creds.json you could use default = "./keys/my-creds.json"
}


variable "project" {
  description = "Project"
  default     = "dtc-de-project"
}

variable "region" {
  description = "Region"
  #Update the below to your desired region
  default = "us-central1"
}

variable "location" {
  description = "Project Location"
  #Update the below to your desired location
  default = "US"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  #Update the below to what you want your dataset to be called
  default = "citibikes"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  #Update the below to a unique bucket name
  default = "dtc-de-project"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}

variable "dataproc_cluster_name" {
  description = "Dataproc Cluster Name"
  #Update the below to what you want your dataset to be called
  default = "dtc-de-project-dataproc"
}