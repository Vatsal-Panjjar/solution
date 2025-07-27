## Overview

This project contains an main file and Azure Function App written in Python that performs two main tasks:

1. **Archive Timer Trigger (`archive_timer`)**  
   - Runs on a schedule (e.g., once per month).
   - Moves data older than 3 months from Azure Cosmos DB into Azure Blob Storage.
   - Helps optimize costs by offloading rarely-accessed data.

2. **Data Query HTTP Trigger (`data_query`)**  
   - Accepts a `timestamp` and `document_id` via HTTP POST.
   - If the timestamp is older than 3 months: searches the document in **Blob Storage**.
   - Else: searches in **Cosmos DB**.

**Main.tf**
   - Install Terraform and Azure CLI.
   - Initialize Terraform: syntax: terraform init
   - Apply the Configuration: terraform apply


**Reference**
   - A word file and excel file has been uploaded in the reference folder with explanation and assumption for given scenario and use cases. 
   - I have also created a chatgpt file where i have wrote the prompt used to create this terraform code.
