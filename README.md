## Overview

This project contains an Azure Function App written in Python that performs two main tasks:

1. **Archive Timer Trigger (`archive_timer`)**  
   - Runs on a schedule (e.g., once per day).
   - Moves data older than 3 months from Azure Cosmos DB into Azure Blob Storage.
   - Helps optimize costs by offloading rarely-accessed data.

2. **Data Query HTTP Trigger (`data_query`)**  
   - Accepts a `timestamp` and `document_id` via HTTP POST.
   - If the timestamp is older than 3 months: searches the document in **Blob Storage**.
   - Else: searches in **Cosmos DB**.

3. **Reference**
   - I have uploaded a word file and the excel file om how i have assumed the data for billing records in Azure Cosmos DB and how i have made changes and optimized the cost on how it was recommended.
   - I have also created a chatgpt file where i have wrote the prompt used to create this terraform code.
