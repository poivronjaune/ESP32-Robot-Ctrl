import requests 

class RobotControl:
    def __init__(self, base_url):
        self.base_url = base_url 
        self.commands = {
            "STOP" : "/api/stop",
            "FORWARD": "/api/forward",
            "BACKWARD": "/api/backward",
            "LEFT": "/api/left",
            "RIGHT": "/api/right"            
        }
    
    def execute(self, command):
        url = self.base_url + self.commands.get(command)
        try:
            res = requests.get(url, timeout=1)
            if res.status_code == 200:
                json_response = res.json()
            else:
                json_response = {"msg": "ERROR", "code": res.status_code, "status": f"Server did not execute {command} command"}
        except:
            json_response = {"msg": "ERROR", "code": 500, "status": f"No response from server, {command} command"}
        
        return json_response
