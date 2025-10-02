terraform {
    required_providers {
    google = {
        source = "hashicorp/google"
        version = "6.49.2"
        }
    }
}


provider "google" {
    project = var.project_id
    region  = var.region
}


variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "asia-southeast1"
}

resource "google_sql_database_instance" "DE_tryme" {
    name = "sandbox-sql-instance"
    database_version = "POSTGRES_15"
    region = var.region
    
    settings {
        # Second-generation instance tiers are based on the machine
        # type. See argument reference below.
        tier = "db-f1-micro"
        # RAM= "644245094"
        # kind= "sql#tier"
        # DiskQuota= "3279207530496"
    }
    

}