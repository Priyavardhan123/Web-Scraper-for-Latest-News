from django.test import TestCase
from django.test import Client

c = Client()

response1 = c.get('http://127.0.0.1:8000/home')
print("Status Code :", response1.status_code)   