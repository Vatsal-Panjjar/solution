provider "azurerm" {
  features {}
subscription_id = ""
} 
 
resource "azurerm_resource_group" "RG"
{
location = "centralIndia"
name= "RG"
}

resource "azurerm_storage_account" "str-ac"
{
name  = "mycosmosblobsa"
resource_group_name = azurerm_resource_group.RG.name
location = azurerm_resource_group.RG.location
account_tier = "standard"
account_replication_type = "GRS"
}

resource "azurerm_storage_container" "container"
{
name = "container"
storage_account_id= azurerm_storage_account.str-ac.id
container_access_type = "private"
}

resource "azurerm_app_service_plan" "plan"
{
name ="function-app-plan"
location = azurerm_resource_group.RG.location
resource_group_name = azurerm_resource_group.RG.name
kind = "FunctionApp"

sku{
tier= "dynamic"
size = "Y1"
}
}



resource "azurerm_function_app" "function" {
  name                       = "cosmos-to-blob-func"
  location                   = azurerm_resource_group.rg.location
  resource_group_name        = azurerm_resource_group.rg.name
  app_service_plan_id        = azurerm_app_service_plan.plan.id
  storage_account_name       = azurerm_storage_account.str-ac.name
  storage_account_access_key = azurerm_storage_account.str-ac.primary_access_key
  version                    = "~4"
  os_type                    = "windows"

  app_settings = {
    FUNCTIONS_WORKER_RUNTIME      = "python"
    AzureWebJobsStorage           = azurerm_storage_account.str-ac.primary_connection_string
    CosmosDbConnectionString      = "<your-cosmos-connection-string>" # Replace with KeyVault or directly (not recommended)
    BlobStorageConnectionString   = azurerm_storage_account.str-ac.primary_connection_string
    TargetContainerName           = azurerm_storage_container.container.name
  }

  site_config {
    application_stack {
      python_version = "3.13.5"
    }
  }
}

