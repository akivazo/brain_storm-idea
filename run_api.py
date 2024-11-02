import waitress, os
from pymongo import MongoClient
import waitress.server
from server.idea_api import server, set_mongo_client

if __name__ == "__main__":
    uri = os.environ["IDEA_MONGODB_URI"]
    mongo_client = MongoClient(uri)
    set_mongo_client(mongo_client=mongo_client)
    waitress.serve(server, host="0.0.0.0", port=5000)
    mongo_client.close()