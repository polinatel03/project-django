from locust import HttpUser, task, between
import random
from datetime import datetime, timedelta
import re
class ShopUser(HttpUser):
    host = "http://localhost:8000"
    wait_time = between(1, 5)

    @task(1)
    def view_shop(self):
        self.client.get("/shop/product/add")
    
    @task(2)
    def view_shop(self):
        self.client.get("/shop/product/success")
    
