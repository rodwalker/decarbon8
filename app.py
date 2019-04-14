from flask import Flask, request, jsonify, render_template
from redis import Redis

import intensity

app = Flask(__name__)
redis = Redis(host="redis", db=0, socket_timeout=5, charset="utf-8", decode_responses=True)
intensity = intensity.Intensity()


#class Appliance(ndb.Model):
#  """ Household appliance with power profile  """
#  apptype = ndb.String.Property()
#  model = ndb.String.Property()
#  program = ndb.String.Property()

@app.route('/', methods=['POST', 'GET'])
def student():
   return render_template('appliance.html')

@app.route('/delay', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        name = request.json['name']
        redis.rpush('students', {'name': name,'other':'poo'})
        return jsonify({'name': name})

    if request.method == 'GET':
        #country = request.form['country']
        #maxDelay = request.form['maxDelay']
        country = request.args.get('country')
        maxDelay = request.args.get('maxDelay')
#        loadDefaults()
        return jsonify(intensity.getDelay(country,int(maxDelay)))
#        return jsonify(redis.lrange('appliances', 0, -1))
#        return jsonify(redis.lrange('students', 0, -1))
    

def loadDefaults():
#create default appliances                                                     
    appliance={'type':'Dishwasher','model':'default','profile':[2,3,0.2,0.2]}
    redis.rpush('appliances', appliance)
    
