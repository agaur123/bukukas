# test_capitalize.py
import pytest
import requests


def test_get_200():
     response = requests.get("http://hello-world.info/get/abc")
     assert response.status_code == 200

def test_set_key():
     response = requests.get("http://hello-world.info/set/ccc-2?value=13")
     assert response.status_code == 200

def test_search_key_preffix():
     response = requests.get("http://hello-world.info/search?prefix=abc")
     assert response.status_code == 200

def test_search_key_suffix():
     response = requests.get("http://hello-world.info/search?suffix=-1")
     assert response.status_code == 200