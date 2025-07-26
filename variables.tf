variable "subscription_id" {
  description = "Azure subscription ID"
  type        = string
}

variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
  default     = "RG"
}

variable "location" {
  description = "Azure region"
  type        = string
  default     = "Central India"
}

variable "storage_account_name" {
  description = "Storage account name"
  type        = string
  default     = "mycosmosblobsa"
}

variable "container_name" {
  description = "Blob container name"
  type        = string
  default     = "container"
}

variable "function_app_name" {
  description = "Name of the Azure Function App"
  type        = string
  default     = "cosmos-to-blob-func"
}

variable "cosmos_connection_string" {
  description = "Cosmos DB connection string"
  type        = string
}
