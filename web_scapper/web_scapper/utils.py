import pymongo

db_name = "web_scraper"
port = 27017
host = "localhost"
username = ""
password = ""
myclient = None


def get_MongoClient():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["web-scraper"]
    return myclient, mydb



# def get_db_handle():
#     db_handle = {}
#     client ={}
#     client = MongoClient(host=host,
#                          port=int(port),
#                          username=username,
#                          password=password
#                         )
#     db_handle = client[db_name]
#     return db_handle, client


# def get_collection_handle(db_handle, collection_name):
#     return db_handle[collection_name]