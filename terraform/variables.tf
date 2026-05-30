variable "kube_config_path" {
  description = "caminho para o kubeconfig"
  type        = string
  default     = "~/.kube/config"
}

variable "namespace" {
  description = "namespace do projeto no kubernetes"
  type        = string
  default     = "lojaveloz"
}

variable "environment" {
  description = "ambiente: dev, staging ou production"
  type        = string
  default     = "production"
}
