from flask import Flask, request
import requests, json

app = Flask(__name__)

@app.route('/register', methods=['PUT'])
def register():
    hostname = request.json['hostname']
    ip = request.json['ip']
    as_ip = request.json['as_ip']
    as_port = request.json['as_port']
    dns = "http://{0}:{1}/register".format(as_ip, as_port)
    data = {
        'name': hostname, 
        'ip': ip
    }
    headers = {"Content-Type": "application/json"}
    dns_res = requests.put(dns, data=json.dumps(data), headers=headers)
    return str(dns_res.content), 201

@app.route('/fibonacci', methods = ['GET'])
def fibonacci():
    number = request.args.get('number')
    if number.isdigit() and int(number) >= 0:
        return str(fib(int(number)))
    else:
        return 'Bad Format', 400
    
def fib(n):
    if n == 0:
        return 0
    elif n == 1 or n == 2:
        return 1
    else:
        return fib(n-1) + fib(n-2)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9090, debug=False)