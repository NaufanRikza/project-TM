import requests
import os

class Client:
    __baseUrl = None

    def __init__(self, url) -> None:
        self.__baseUrl = url

    def ping(self) -> bool:
        try:
            requests.get("https://www.google.com", timeout=(4, 4))
            return True
        except requests.ConnectionError:
            return False

    def get(self, url, params=None):
        try:
            res = requests.get("{0}{1}".format(
                self.__baseUrl, url), timeout=(5, 5), params=params)
            return res.json()
        except Exception as e:
            print(e)
            raise Exception("Client get method error")

    def post(self, url, data=None, params=None, files=None):
        try:
            res = requests.post("{0}{1}".format(
                self.__baseUrl, url),
                data=data, timeout=(5, 5), params=params, files=files, headers={"Authorization" : "{0} {1}".format("Bearer", os.getenv("API_KEY"))})

            return res.json()
        except Exception as e:
            print(e)
            raise Exception("Client post method error")
        
    def put(self, url, key):
        try:
            res = requests.put("{0}{1}".format(
                self.__baseUrl, url),
                data={ 
                    "data": {
                        "id": 1,
                        "attributes": {
                            key : False
                        }
                    },
                    "meta": {}
                    }, timeout=(5, 5),
                headers={"Authorization" : "{0} {1}".format("Bearer", os.getenv("API_KEY"))})

            return res.json()
        except Exception as e:
            print(e)
            raise Exception("Client put method error")        
