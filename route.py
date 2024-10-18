# use mapbox api to generate route using the roads

# REQUIRED: pip install requests
# problem: a point on the route can only be excluded in driving mode (mapbox limitation)
# try different apis

# used for testing - actual code in app.py

import requests

MAPBOX_KEY = YOUR_MAPBOX_KEY


# assume no obstructions
# inputs: start_coords (list) = starting point [longitude, latitude]
#         end_coords (list) = end point [longitude, latitude]
# outputs: route_coordinates (list) = list of [longitude, latitude] coordinates
#          route_distance (float) = distance of journey in metres
def get_route():
    # default coordinates
    start_coords = [144.98787920571158, -37.83360117708017] # user's home (492 punt rd)
    end_coords = [144.98234802465515, -37.83354253194787] # royal botanic gardens

    url = f'https://api.mapbox.com/directions/v5/mapbox/driving/{start_coords[0]},{start_coords[1]};{end_coords[0]},{end_coords[1]}'
    params = {
        'access_token': MAPBOX_KEY,
        'geometries': 'geojson',  
        'overview': 'full'        
    }
    response = requests.get(url, params=params)

    # save outputs if successful
    if response.status_code == 200:
        data = response.json()
        route = data['routes'][0]
        route_coordinates = route['geometry']['coordinates']
        route_distance = route['distance']
        print(route_coordinates)
        return route_coordinates, route_distance
    else:
        print("Error:", response.status_code, response.text)
        return
    

# catch an obstruction and choose a new route
# inputs: start_coords (list) = starting point [longitude, latitude]
#         end_coords (list) = end point [longitude, latitude]
#         exclude (list) = point to avoid [longitude, latitude]
# outputs: route_coordinates (list) = list of [longitude, latitude] coordinates
#          route_distance (float) = distance of journey in metres
def get_new_route():
    # default coordinates
    start_coords = [144.98787920571158, -37.83360117708017] # user's home (492 punt rd)
    end_coords = [144.98234802465515, -37.83354253194787] # royal botanic gardens
    exclude = [144.983353, -37.834236]

    url = f"https://api.mapbox.com/directions/v5/mapbox/walking/{start_coords[0]},{start_coords[1]};{end_coords[0]},{end_coords[1]}"
    params = {
        'access_token': MAPBOX_KEY,
        'geometries': 'geojson',  
        'overview': 'full',
        'exclude': f'point({exclude[0]} {exclude[1]})'      
        }
    response = requests.get(url, params=params)

    # save outputs if successful
    if response.status_code == 200:
        data = response.json()
        route = data['routes'][0]
        route_coordinates = route['geometry']['coordinates']
        route_distance = route['distance']
        print(route_coordinates)
        return route_coordinates, route_distance
    else:
        print("Error:", response.status_code, response.text)
        return
    

def get_geoapify_route():
    # default coordinates
    start_coords = [-37.83360117708017, 144.98787920571158] # user's home (492 punt rd)
    end_coords = [-37.83354253194787, 144.98234802465515] # royal botanic gardens

    GEOAPIFY_KEY = "2bbca442cf0f483fa1a37f2b899e49eb"

    # Construct the API request URL
    url = 'https://api.geoapify.com/v1/routing'

    # Parameters for the API request
    params = {
        'waypoints': f'{start_coords[0]},{start_coords[1]}|{end_coords[0]},{end_coords[1]}',
        'mode': 'walk',
        'apiKey': GEOAPIFY_KEY,
    }

    # Make the API request
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        # Check if the response contains routes
        if 'features' in data:
            route = data['features'][0]  # Get the first route
            properties = route['properties']
            distance = properties['distance']  # Distance in meters
            time = properties['time']  # Duration in seconds
            
            # Print route information
            print(f"Route duration: {time/60:.2f} minutes")
            print(f"Route distance: {distance/1000:.2f} kilometers")
            print(route['geometry']['coordinates'])

            return route['geometry']['coordinates']
        else:
            print("No routes found in the response.")
    else:
        print(f"Request failed with status code: {response.status_code}")
        print("Response:", response.text)


def get_new_geoapify_route():
    # default coordinates
    start_coords = [-37.83360117708017, 144.98787920571158] # user's home (492 punt rd)
    end_coords = [-37.83354253194787, 144.98234802465515] # royal botanic gardens
    exclude = [-37.834642, 144.987375]

    GEOAPIFY_KEY = "2bbca442cf0f483fa1a37f2b899e49eb"

    # Construct the API request URL
    url = 'https://api.geoapify.com/v1/routing'

    # Parameters for the API request
    params = {
        'waypoints': f'{start_coords[0]},{start_coords[1]}|{end_coords[0]},{end_coords[1]}',
        'mode': 'walk',
        'apiKey': GEOAPIFY_KEY,
        'avoid': f'location:{exclude[0]},{exclude[1]}'
    }

    # Make the API request
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        # Check if the response contains routes
        if 'features' in data:
            route = data['features'][0]  # Get the first route
            properties = route['properties']
            distance = properties['distance']  # Distance in meters
            time = properties['time']  # Duration in seconds
            
            # Print route information
            print(f"Route duration: {time/60:.2f} minutes")
            print(f"Route distance: {distance/1000:.2f} kilometers")
            print(route['geometry']['coordinates'])

            return route['geometry']['coordinates']
        else:
            print("No routes found in the response.")
    else:
        print(f"Request failed with status code: {response.status_code}")
        print("Response:", response.text)



# testing purposes
# get_route()
# get_new_route()
get_geoapify_route()
get_new_geoapify_route()