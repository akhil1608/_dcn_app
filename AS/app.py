from flask import Flask, request
from random import randint

app = Flask(__name__)

type_ = 'A'

@app.route('/query', methods = ['GET'])
def query():
    response, code = '', 204
    name = request.args.get('name')
    type_ = request.args.get('type')
    with open('registry.csv', 'r') as f:
        for line in f:
          tokens = line.split(',')
          if tokens[1] == name:
              code = 200
              response = 'TYPE={0}<br>NAME={1}<br>VALUE={2}<br>TTL={3}<br>'.format(type_, name, tokens[2], tokens[3])
              break
    return response, code

@app.route('/register', methods = ['PUT'])
def register():
    name = request.json['name']
    ip = request.json['ip']
    ttl = generateTTL()
    entry = '{0},{1},{2},{3}\n'.format(type_, name, ip, ttl)
    with open('registry.csv', 'a') as f:
        f.write(entry)
    response = 'TYPE={0}<br>NAME={1}<br>VALUE={2}<br>TTL={3}<br>'.format(type_, name, ip, ttl)
    return response, 201

def generateTTL():
    return str(randint(100, 500))

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=53533, debug=False)