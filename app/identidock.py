import hashlib
from flask import Flask, Response, request
import requests
import redis


app = Flask(__name__)
default_name = '0xfreedom'
salt = 'UNIQUE_SALT'
cache = redis.StrictRedis(host='redis', port=6379, db=0)


@app.route('/', methods=['GET', 'POST'])
def mainpage():
    name = default_name
    if request.method == 'POST':
        name = request.form['name']
    
    salt_name = salt + name
    name_hash = hashlib.sha256(salt_name.encode()).hexdigest()
    header = '<html><head><title>Identidock</title></head><body>'
    body = '''<form method="POST">
              Hello <input type="text" name="name" value="{name}">
              <input type="submit" value="submit">
              </form>
              <p>You look like a:
              <img src="/monster/{name_hash}.png"/>
              '''.format(name=name, name_hash=name_hash)
    footer = '</body></html>'
    return header + body + footer


@app.route('/monster/<name>', methods=['GET'])
def get_identicon(name):
    image = cache.get(name)
    if image is None:
        print('Cache miss')
        r = requests.get('http://dnmonster:8080/monster/' + name + '?size=80')
        image = r.content
        cache.set(name, image)
    return Response(image, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
