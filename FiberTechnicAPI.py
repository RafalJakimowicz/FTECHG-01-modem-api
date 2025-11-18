import requests
import json
import hashlib
import datetime

class FiberTechnicAPI:
    def __init__(self, ip: str, username: str, password: str):
        #sets ip adress of device
        self.MODEM_IP = ip

        #sets username and password
        self.USERNAME = username
        self.PASSWORD = password
        self.PASSWORD_HASH = self.get_password_hash(password)

        #endpoints
        self.POST_URL = f"http://{self.MODEM_IP}/post.json"
        self.GET_URL = f"http://{self.MODEM_IP}/get.json"

        #header that mimics browser 
        self.HEADER = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Content-Type": "application/json",
            "Referer": f"http://{self.MODEM_IP}/login.html",
            "Origin": f"http://{self.MODEM_IP}",
            "Accept": "application/json, text/plain, */*"
        }

        self.SESSION = self.login_and_get_session()

    def get_password_hash(self, password: str) -> str:
        #password is hashed to be send to modem by md5
        hash_bytes = hashlib.md5(password.encode())
        hash_string = str(hash_bytes.hexdigest())
        return hash_string
    
    def login_and_get_session(self, debug=False) -> requests.Session:
        '''
        Login to device get session and cookies
        '''
        session = requests.Session()
        # Ustawiamy domyślne nagłówki dla całej sesji
        session.headers.update(self.HEADER)
        
        payload = {
            "module": "login",
            "username": self.USERNAME,
            "encryPassword": self.PASSWORD_HASH
        }
        
        try:
            print(f"Logging as {self.USERNAME}...")
            response = session.post(self.POST_URL, json=payload, timeout=10)
            
            try:
                data = response.json()
            except json.JSONDecodeError:
                print("Error: Server didnt return JSON. Chech IP or if you are blocked.")
                return None

            if data.get("code") == 0:
                cookie = session.cookies.get_dict().get("session")
                self.HEADER["Cookie"] = f"session={cookie}"
                session.headers.update({"Authorization": cookie})
                print(f"Signed successfully {datetime.datetime.now()}")

                if debug:
                    print("[DEBUG] Response:")
                    print(json.dumps(data, indent=2))

                return session
            else:
                print(f"Error while signing in error code: {data.get('code')}")
                return None

        except Exception as e:
            print(f"Connection error: {e}")
            return None
        
    def send_get(self, params: dict, debug=False) -> dict:
        """
        Sends GET request to device returns response
        """
        try:
            response = self.SESSION.get(self.GET_URL, params=params)
            data = response.json()
            
            if data.get("code") == 0:
                if debug:
                    print(json.dumps(data, indent=4))
                return data
            else:
                print(f"Error while fetching data. Code: {data.get('code')}")
                
        except Exception as e:
            print(f"Error while fetching data: {e}")
        
    def send_post(self, payload: dict, debug=False) -> dict:
        """
        Sends POST request to device returns response
        """
        try:
            response = self.SESSION.post(self.POST_URL, params=payload)
            data = response.json()
            
            if data.get("code") == 0:
                if debug:
                    print(json.dumps(data, indent=4, ensure_ascii=False))
                return data
            else:
                print(f"While fetching data. Code: {data.get('code')}")
                
        except Exception as e:
            print(f"Error while fetching data: {e}")
