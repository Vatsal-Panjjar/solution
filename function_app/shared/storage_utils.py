import os
import json
from datetime import datetime, timedelta
import pymongo
from azure.storage.blob import BlobServiceClient

def is_older_than_3_months(timestamp_str):
    """
    Checks if the given ISO 8601 timestamp is older than 90 days.
    """
    try:
        timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
        cutoff = datetime.utcnow() - timedelta(days=90)
        return timestamp < cutoff
    except Exception as e:
        raise ValueError(f"Invalid timestamp format: {timestamp_str}") from e

def get_blob_container():
    """
    Connects to the blob container using environment variables.
    Requires:
        - BlobStorageConnectionString
        - TargetContainerName
    """
    blob_conn_str = os.environ.get("BlobStorageConnectionString")
    container_name = os.environ.get("TargetContainerName")
    
    if not blob_conn_str or not container_name:
        raise EnvironmentError("Missing Blob storage connection settings.")

    blob_service = BlobServiceClient.from_connection_string(blob_conn_str)
    return blob_service.get_container_client(container_name)

def get_cosmos_collection():
    """
    Connects to the Cosmos DB collection using environment variables.
    Requires:
        - CosmosDbConnectionString
        - CosmosDbName
        - CosmosCollectionName
    """
    cosmos_conn_str = os.environ.get("CosmosDbConnectionString")
    db_name = os.environ.get("CosmosDbName")
    collection_name = os.environ.get("CosmosCollectionName")

    if not cosmos_conn_str or not db_name or not collection_name:
        raise EnvironmentError("Missing Cosmos DB connection settings.")

    client = pymongo.MongoClient(cosmos_conn_str)
    db = client[db_name]
    return db[collection_name]

def find_document_in_blob(container_client, doc_id):
    """
    Loops through blobs and returns a document if found.
    Warning: Inefficient for large data unless optimized.
    """
    for blob in container_client.list_blobs():
        blob_data = container_client.download_blob(blob.name).readall()
        try:
            documents = json.loads(blob_data)
        except:
            continue

        for doc in documents:
            if doc.get("_id") == doc_id:
                doc["_id"] = str(doc["_id"])
                return doc

    return None
