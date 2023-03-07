from flask import Flask, request
import requests, json
from random import randint

app = Flask(__name__)

type_ = 'A'
params = ['hostname', 'fs_port', 'number', 'as_ip', 'as_port']

@app.route('/fibonacci')
def fibonacci():
    # verifying parameters
    if not verifyParams(request.args.keys()):
        return 'Bad Format', 400
    
    # getting parameters
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    n = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')
    
    # request urls
    dns = "http://{0}:{1}/query?name={2}&type={3}".format(as_ip, as_port, hostname, type_)
    fs = "http://127.0.0.1:{0}/".format(fs_port)
    
    # fetching ip from AS
    dns_res = requests.get(dns)
    if dns_res.status_code == 204:
        # register if ip not found
        ip = generateIP()
        fsr = fs + "register"
        data = {
            'hostname': hostname, 
            'ip': ip, 
            'as_ip': as_ip, 
            'as_port': as_port
        }
        headers = {"Content-Type": "application/json"}
        requests.put(fsr, data=json.dumps(data), headers=headers)
    else:
        content = str(dns_res.content).split('=')
        ip = content[3].split('<br>')[0]
    
    # calculate fibonacci value for sequence
    fsn = fs + "fibonacci?number=" + n
    fsn_res = requests.get(fsn)
        
    return fsn_res.content, 200

def verifyParams(p):
    return sorted(params) == sorted(p)

def generateIP():
    return ".".join(str(randint(0, 255)) for _ in range(4))

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=False)