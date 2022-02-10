from datetime import datetime
import requests
import json
requests.packages.urllib3.disable_warnings() # suppress SSL certificate warnings when ssl_verify=False

class WebIMS:
    def __init__(self, endpoint, sessionId):
        self.endpoint = endpoint
        self.sessionId = sessionId

    def inventory_import(self, warehouseId, file):
        now = datetime.now()
        
        bodyData = json.loads('{}')
        bodyData.update({"warehouseId":warehouseId})
        bodyData.update({"file":file})
        
        response = requests.put(self.endpoint + '/api/inventory/import.php', json=bodyData, headers={'Auth-Key': self.sessionId}, verify=False)
        
        print (response.content)

        if response.status_code == 200:
            print (now.strftime("%d/%m/%Y %H:%M:%S") + ": Data Imported " + str(response.content.decode('utf-8')))   
        else:
            print (now.strftime("%d/%m/%Y %H:%M:%S") + ": Error occured!")