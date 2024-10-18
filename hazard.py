# hazard reporting handling

# input from front end: image of hazard
# workflow: image processing -> text description -> open AI -> is this a hazard? 
# future plan would be to save to database if identified as a hazard

# used for testing - actual code will be transferred into a class in app.py


from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import openai

openai.api_key = YOUR_OPENAPI_KEY

# load the processor and model
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")


# function to generate image caption
def generate_caption(image_path):
    image = Image.open(image_path).convert('RGB')
    inputs = processor(image, return_tensors="pt")
    out = model.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True)
    return caption

# future improvements: 
#   conciseness/accuracy of caption
#   improve processing time (roughly ~ for the whole process)
# caption should indicate whether there is a blockage/how big it is to influence openai

image_path = "test_images/img5.jpg"
caption = generate_caption(image_path)
print("Generated Caption:", caption)

# caption = "construction workers work on the sidewalk in downtown"
# ask openai whether the image description could pose a hazard
def ask_openai(question):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": question}],
        max_tokens=1000,  
        temperature=0.3  # lower = more deterministic
    )
    return response

question_string = "Would " + caption + " block or obstruct the path of a wheelchair user?"
response = ask_openai(question_string)
print(response)
ai_response = response.choices[0].message.content.strip()
print(ai_response)