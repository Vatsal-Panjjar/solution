output "function_app_url" {
  description = "URL of the Azure Function App"
  value       = azurerm_function_app.function.default_hostname
}

output "storage_account_name" {
  description = "The name of the storage account"
  value       = azurerm_storage_account.str_ac.name
}

output "container_name" {
  description = "The name of the blob container"
  value       = azurerm_storage_container.container.name
}
