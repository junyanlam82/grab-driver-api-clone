from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

drivers = [
    {
       'name': 'Embryo Mithen',
       'location':{
        'x':1,
        'y':2
       },
       'willDriveDistance':12, #what is the highest distance he can go by driving
        'carCapacity':4 #how many people can go in the car
     },
     {
       'name': 'Katie Mithen',
       'location':{
        'x':2,
        'y':5
       },
       'willDriveDistance':20, #what is the highest distance he can go by driving
        'carCapacity':6 #how many people can go in the car
     },
     {
       'name': 'Maria Anne',
       'location':{
        'x':7,
        'y':8
       },
       'willDriveDistance':14, #what is the highest distance he can go by driving
        'carCapacity':4 #how many people can go in the car
     },
]

#input queryString will be /api/search/drivers
customers = [
    {
        'customerName':'Raymond Reddington',
        'customerLocation':{#where the customer is now
            'x':2,
            'y':7
        },
        'customerDestination':{#where does customer want to go
            'x':7,
            'y':9
        },
        'customerGuestCount':2 #how many persons should be in the car
    }
]


class Customers(Resource):
    pass

class Drivers(Resource):
    def post(self):
        parser = reqparse.RequestParser() #initialize

        parser.add_argument('name',required=True)
        parser.add_argument('loc',required=True)
        parser.add_argument('des',required=True)
        parser.add_argument('count',required=True)

        args = parser.parse_args()
        location_X,location_Y = args['loc'].split(',')
        destination_X,destination_Y = args['des'].split(',')

        #store data from queryString 
        new_data = {

            'customerName':args['name'],
            'customerLocation':{
                'x':int(location_X),
                'y':int(location_Y)
            },
            'customerDestination':{
                'x':int(destination_X),
                'y':int(destination_Y)
            },
            'customerGuestCount':int(args['count']),
        }

        #find the closest driver to customer
        driverFound = findClosest(drivers,new_data)
        willDriveDistance = willDriveDist(
            [new_data['customerLocation']['x'],new_data['customerLocation']['y']],
            [new_data['customerDestination']['x'],new_data['customerDestination']['y']])
        #customers.append(new_data)
        carCapacity = new_data['customerGuestCount']
        return jsonify({
            '01_nearestDriver':driverFound,
            '02_loc_destDistance':willDriveDistance,
            '03_guestToSit':carCapacity,
        }) #if return only normal data, error[500] will prompt out
     
def findClosest(driverList,customerData):
    driverFound = None
    shortestDistancePrev = 0
    shortestDistanceAfter = 0
    for currentDriver in driverList:
        from_X = currentDriver['location']['x']
        from_y = currentDriver['location']['y']
        to_X = customerData['customerLocation']['x']
        to_y = customerData['customerLocation']['y']

        shortestDistanceAfter = calculateDist([from_X,from_y],[to_X,to_y])

        if shortestDistancePrev == 0: #initialization
            driverFound = currentDriver
            shortestDistancePrev = shortestDistanceAfter 
            # before => prev = 0 , after = 2
            # after  => prev = 2 , after = 2
        elif shortestDistancePrev >= shortestDistanceAfter:
            # before => prev = 2 , after = 1
            # after  => prev = 1 , after = 1
            driverFound = currentDriver
            shortestDistancePrev = shortestDistanceAfter

    return driverFound
    
def willDriveDist(source,destination):
    return calculateDist(source,destination)

def calculateDist(src_pt,dest_pt):
    return abs(dest_pt[0] - src_pt[0] ) + abs(dest_pt[1] - src_pt[1] )

api.add_resource(Drivers,'/api/search/drivers')
api.add_resource(Customers,'/customers')

@app.route("/")
def index():
    if request.method == "GET":
    #return jsonify(calculateShortest([1,2],[2,7]))
        return jsonify("Grab Driver API Clone")


@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)