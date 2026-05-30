terraform {
  required_version = ">= 1.5"
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.30"
    }
  }
}

provider "kubernetes" {
  config_path = var.kube_config_path
}

resource "kubernetes_namespace" "lojaveloz" {
  metadata {
    name = var.namespace
    labels = {
      environment = var.environment
      project     = "loja-veloz"
    }
  }
}

# limita o quanto o namespace pode consumir de recursos
resource "kubernetes_resource_quota" "lojaveloz" {
  metadata {
    name      = "lojaveloz-quota"
    namespace = kubernetes_namespace.lojaveloz.metadata[0].name
  }
  spec {
    hard = {
      "requests.cpu"    = "2"
      "requests.memory" = "2Gi"
      "limits.cpu"      = "4"
      "limits.memory"   = "4Gi"
      "pods"            = "20"
    }
  }
}
