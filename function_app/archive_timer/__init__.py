import datetime
import logging
import os
import json
import pymongo
from azure.storage.blob import BlobServiceClient
import azure.functions as func

def main(mytimer: func.TimerRequest) -> None:
    logging.info("Archive timer function started.")

    try:
        
        cosmos_conn = os.environ["CosmosDbConnectionString"]
        blob_conn = os.environ["BlobStorageConnectionString"]
        container_name = os.environ["TargetContainerName"]

        
        mongo_client = pymongo.MongoClient(cosmos_conn)
        db = mongo_client["<your-db-name>"]               
        collection = db["<your-collection-name>"]          

        blob_service = BlobServiceClient.from_connection_string(blob_conn)
        container_client = blob_service.get_container_client(container_name)

       
        cutoff_date = datetime.datetime.utcnow() - datetime.timedelta(days=90)

      
        old_docs = list(collection.find({"timestamp": {"$lt": cutoff_date}}))

        if not old_docs:
            logging.info("No documents older than 3 months found.")
            return

        
        for doc in old_docs:
            doc["_id"] = str(doc["_id"])
            doc["timestamp"] = doc["timestamp"].isoformat()

        archive_blob_name = f"archive_{datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')}.json"
        blob_client = container_client.get_blob_client(archive_blob_name)
        blob_client.upload_blob(json.dumps(old_docs), overwrite=True)
        logging.info(f"Archived {len(old_docs)} documents to blob '{archive_blob_name}'.")

        
        for doc in old_docs:
            collection.delete_one({"_id": pymongo.ObjectId(doc["_id"])})
        logging.info("Deleted archived documents from Cosmos DB.")

    except Exception as e:
        logging.error(f"Error during archive process: {e}")
