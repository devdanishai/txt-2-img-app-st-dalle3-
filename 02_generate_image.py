import openai
import requests
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Retrieve the OpenAI API key from the environment
openai.api_key = os.getenv("OPENAI_API_KEY")

# Make a request to OpenAI's API to generate images
response = openai.Image.create(
    prompt="A cute baby sea otter",  # The prompt for the image
    n=1,  # Number of images to generate (you can change this number)
    size="1024x1024"  # Image size
)

# Get the URL of the first generated image
image_url = response['data'][0]['url']

# Download the image from the URL
image_data = requests.get(image_url).content

# Save the image to a local file (e.g., "sea_otter.png")
with open('sea_otter.png', 'wb') as f:
    f.write(image_data)

print("Image saved successfully as sea_otter.png")
