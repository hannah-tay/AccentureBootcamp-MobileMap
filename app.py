from flask import request
from flask_restx import Resource
import requests
import traceback
from typing import Dict 
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import openai 


class GetCurrentLocation(Resource):
    def get(self):
        return [-37.83360117708017, 144.98787920571158] # user's home (492 punt rd)
    
class GetEndLocation(Resource):
    def get(self):
        return [-37.83354253194787, 144.98234802465515] # royal botanic gardens
    
class GetExcludeLocation(Resource):
    def get(self):
        return [-37.834642, 144.987375] # point along default route

class Route(Resource):
    def post(self):
        GEOAPIFY_KEY = YOUR_GEOAPIFY_KEY
        request_json: Dict = request.get_json()
        start_coords = request_json.get('start_coords')
        end_coords = request_json.get('end_coords')

        url = 'https://api.geoapify.com/v1/routing'
        params = {
            'waypoints': f'{start_coords[0]},{start_coords[1]}|{end_coords[0]},{end_coords[1]}',
            'mode': 'walk',
            'apiKey': GEOAPIFY_KEY,
        }

        response = requests.get(url, params=params)
        
        # save outputs if successful
        # if response.status_code == 200:
        # Check if the request was successful
        try:
            data = response.json()
            # Check if the response contains routes
            if 'features' in data:
                route = data['features'][0]  # Get the first route
                properties = route['properties']
                distance = properties['distance']  # Distance in meters
                time = properties['time']  # Duration in seconds
                
                # Print route information
                print(f"Route duration: {time/60:.2f} minutes")
                print(f"Route distance: {distance/1000:.2f} kilometres")
                print(route['geometry']['coordinates'])

                return f'Route found! Duration: {time/60:.2f} minutes. Distance: {distance/1000:.2f} kilometres.', route['geometry']['coordinates']
            else:
                print("No routes found in the response.")
        
        except Exception as e:
            traceback.print_exc()
            print("Error:", response.status_code, response.text)
            print(e)
            return f"Error: {e}",500
        
class NewRoute(Resource):
    def post(self):
        GEOAPIFY_KEY = YOUR_GEOAPIFY_KEY
        request_json: Dict = request.get_json()
        start_coords = request_json.get('start_coords')
        end_coords = request_json.get('end_coords')
        except_coords = request_json.get('except_coords')

        url = 'https://api.geoapify.com/v1/routing'
        params = {
            'waypoints': f'{start_coords[0]},{start_coords[1]}|{end_coords[0]},{end_coords[1]}',
            'mode': 'walk',
            'apiKey': GEOAPIFY_KEY,
            'avoid': f'location:{except_coords[0]},{except_coords[1]}'
        }

        response = requests.get(url, params=params)
        
        # save outputs if successful
        # if response.status_code == 200:
        # Check if the request was successful
        try:
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

                return f'New route found to avoid identified hazard! Duration: {time/60:.2f} minutes. Distance: {distance/1000:.2f} kilometres.', route['geometry']['coordinates']
            else:
                print("No routes found in the response.")
        
        except Exception as e:
            traceback.print_exc()
            print("Error:", response.status_code, response.text)
            print(e)
            return f"Error: {e}",500
        
class HazardIdentification(Resource):
    def post(self):
        openai.api_key = YOUR_OPENAPI_KEY

        # load the processor and model
        processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

        # function to generate image caption
        def generate_caption(image_path, model, processor):
            image = Image.open(image_path).convert('RGB')
            inputs = processor(image, return_tensors="pt")
            out = model.generate(**inputs)
            caption = processor.decode(out[0], skip_special_tokens=True)
            return caption

        # future improvements: concise/accuracy of caption, note processing time roughly for the whole process
        # caption should indicate whether there is a blockage/how big it is to influence openai

        image = request.files.get('image')
        image.save(f'test_images/{image.filename}')
        caption = generate_caption(f'test_images/{image.filename}', model, processor)
        print("Generated Caption:", caption)

        # ask openai whether the image description could pose a hazard
        def ask_openai(question):
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": question}],
                max_tokens=1000,  
                temperature=0.3  
            )
            return response

        question_string = "Would " + caption + " block or obstruct the path of a wheelchair user?"
        response = ask_openai(question_string)
        ai_response = response.choices[0].message.content.strip()
        return ai_response