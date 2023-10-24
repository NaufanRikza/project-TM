import requests

class Client:
    __baseUrl = None
    def __init__(self, url) -> None:
        self.__baseUrl = url

    def ping(self) -> bool:
        try:
            requests.get("https://www.google.com", timeout=(5, 5))
            return True
        except requests.ConnectionError:
            return False
    
    def get(self, url):
        try:
            res = requests.get(str.join(self.__baseUrl, url), timeout=(5, 5))
            return res.json()
        except Exception as e:
            print(e)
            raise Exception("Client get method error")
    
    def post(self, url, data):
        headers = {
            "Content-Type":"application/json"
        }
        res = requests.post(str.join(self.__baseUrl, url), data=data, headers=headers, timeout=(5, 5))