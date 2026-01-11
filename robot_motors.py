import requests 

class RobotControl:
    def __init__(self, base_url):
        self.base_url = base_url 
        

    def stop(self):
        url = self.base_url + "/api/stop"
        try:
            res = requests.get(url, timeout=1)
            if res.status_code == 200:
                print("Robot stopped:", res.json().get('msg'))
            else:
                print("Stop command failed")
            return res.json()
        except:
            print("Stop request error")
            return None

    def forward(self):
        url = self.base_url + "/api/forward"
        json_response = "Empty String"
        try:
            res = requests.get(url, timeout=1)
            if res.status_code == 200:
                print("Robot moving forward:", res.json().get('msg'))
                json_response = res.json
            else:
                print("Forward command failed")
                json_response = {"msg": "STOP", "code": 500, "status": "No response, Forward request error"}
        except:
            print("Forward request error")
            json_response = {"msg": "STOP", "code": 500, "status": "No response, Forward request error"}
            
        return json_response
            