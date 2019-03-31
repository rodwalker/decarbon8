from flask import Flask, request, jsonify
from redis import Redis

from google.appengine.ext import ndb

app = Flask(__name__)
redis = Redis(host="redis", db=0, socket_timeout=5, charset="utf-8", decode_responses=True)

class Appliance(ndb.Model):
  """ Household appliance with power profile  """
  apptype = ndb.String.Property()
  model = ndb.String.Property()
  program = ndb.String.Property()

@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        name = request.json['name']
        redis.rpush('students', {'name': name,'other':'poo'})
        return jsonify({'name': name})

    if request.method == 'GET':
        loadDefaults()
        return jsonify(redis.lrange('appliances', 0, -1))
#        return jsonify(redis.lrange('students', 0, -1))
    

def loadDefaults():
#create default appliances                                                     
    appliance={'type':'Dishwasher','model':'default','profile':[2,3,0.2,0.2]}
    redis.rpush('appliances', appliance)
    
