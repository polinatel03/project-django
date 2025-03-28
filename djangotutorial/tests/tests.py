from playwright.sync_api import sync_playwright
rom django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from polls.models import ReportData

def test_open_page():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://127.0.0.1:8000/")
        assert page.title() == "Api Root – Django REST framework"
        browser.close()