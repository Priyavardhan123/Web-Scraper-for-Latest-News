import pymongo
from webpush import send_user_notification
from webpush import send_group_notification

db_name = "web_scraper"
port = 27017
host = "localhost"
username = ""
password = ""
myclient = None

#Getting mongoDb access
def get_MongoClient():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["web_scraper"]
    return myclient, mydb

#Sending push notification
def send_pn(head, body):
    payload = {"head": head, "body": body, "icon": "/static/images/notification.png", "url": "http://127.0.0.1:8000/home"}
    try:
        send_group_notification(group_name="all", payload=payload, ttl=1000)
    except Exception as e:
        print(e)