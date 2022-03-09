import json
import requests
import base64
import time
import hmac
import hashlib

def lambda_handler(event, context):

    for message in event["Records"]:
        #body = {"data":{"carrier_tn":"US32321321","current_status":"0","trackings":[{"status":"1","description":"RECEIVED","update_time":1640877906,"location":"New York"}]},"endpoint":{"url":"https:\/\/api.xxx.boo","secret":"my_password","account":"my_account"}}
        body = json.loads(message['body'])
        url = body['endpoint']['url']
        account = body['endpoint']['account']
        secret = body['endpoint']['secret']
        pedido = body['data']['carrier_tn']
        status = body['data']['current_status']
        del body['endpoint']
        date = int(time.time())
        timestamp = int(time.time())
        body["timestamp"] = timestamp
        header = { "alg": "HS256","typ": "JWT", "account": account}
        headersbase64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode()
        bodybase64 = base64.urlsafe_b64encode(json.dumps(body).encode()).decode()
        headersbase64 = bytes(headersbase64, 'utf-8')
        bodybase64 = bytes(bodybase64, 'utf-8')
        secret = bytes(secret, 'utf-8')
        signature = hmac.new(
                key=secret,
                msg=f'{headersbase64.decode()}.{bodybase64.decode()}'.encode(),
                digestmod=hashlib.sha256
            ).digest()
        JWT = f'{headersbase64.decode()}.{bodybase64.decode()}.{base64.urlsafe_b64encode(signature).decode()}'
        url = url.replace("\\", "")
        header = {
            "Content-Type": "application/json",
            "charset":"utf-8"
        }
        arraybody = {
            "jwt": JWT
        }
        arraybody = json.dumps(arraybody)
        x = requests.post(url, data = arraybody, headers=header)
        print(x.text)
        print("JWT = {0}".format(JWT))
        print("body = {0}".format(body))
        

