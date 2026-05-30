output "namespace" {
  description = "namespace criado"
  value       = kubernetes_namespace.lojaveloz.metadata[0].name
}
