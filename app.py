import time
import json
import redis

from flask import Flask,redirect,url_for,render_template,request

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def dump_json():
    gps_coords= [
        {'uuid':'123', 'url':'....', 'x':'52.49015802952927', 'y':'13.415608457497155'},
        {'uuid':'234', 'url':'....', 'x':'52.490131898467695', 'y':' 13.425682834308834'}
    ]

    # Convert python dict to JSON str and save to Redis
    json_gps_coords = json.dumps(gps_coords)
    cache.set('gps_coords', json_gps_coords)

def get_gpscoods():
    unpacked_gps_coords = json.loads(cache.get('gps_coords').decode('utf-8'))
    gps_coords == unpacked_gps_coords

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    dump_json()
    count = get_hit_count()
    return render_template('index.html', hits=count)

