import datetime
import logging
import json
from shared import utils
import azure.functions as func

def main(mytimer: func.TimerRequest) -> None:
    logging.info("Timer function started.")
    cutoff = datetime.datetime.utcnow() - datetime.timedelta(days=90)
    old_docs = utils.archive_old_documents(cutoff)

    if old_docs:
        blob_name = f"cosmos-archive-{datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')}.json"
        utils.upload_to_blob(blob_name, json.dumps(old_docs, default=str))
        collection = utils.connect_cosmos()
        for doc in old_docs:
            collection.delete_one({"_id": doc["_id"]})

    logging.info(f"Archived and deleted {len(old_docs)} documents.")
