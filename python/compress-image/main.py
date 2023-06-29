import base64
import tinify
import tempfile
import os
import json

def decode(encoded_value):
    decoded = base64.b64decode(encoded_value)
    return decoded

def encode(plaintext):
    encoded = base64.b64encode(plaintext)
    return encoded

def main(req, res):
  try:
    # Accessing payload
    payload = req.payload
    # Accessing provider from payload
    provider = payload['provider']
    # Acccessing variables
    variable = req.variables
    # Accessing api_key from variables
    api_key = variable['API_KEY']
    # Accessing encoded image from payload
    encoded_image = payload['image']
    # Decoding the encoded image
    decoded_image = decode(encoded_image)

    # Create a temp directory inside of the current working directory. Prefix it as "temp"
    temp_dir = tempfile.mkdtemp(prefix='temp', dir=os.getcwd())
      
    # Generate a copy of the decoded image data as non_optimized.jpg
    decoded_image_path = os.path.join(temp_dir, "non_optimized_image.jpg")

    with open(decoded_image_path, "wb") as i:
        i.write(decoded_image)

    if provider == 'krakenio':
      api_secret_key = variable['SECRET_API_KEY']
      return res.json(
          {
              "success": True,
              "image" : 123
          })
        
    elif provider == 'tinypng':
      # Authenticating api key
      tinify.key = api_key
      # Use that cloned file path to compress image using TinyPNG api

      optimized_image = tinify.from_file(decoded_image_path)
      optimized_image_path = os.path.join(temp_dir, "optimized_image.jpg")
      optimized_image.to_file(optimized_image_path)
      
      # Package by encoding the file in base64 format
      o = open(optimized_image_path, "rb")
      encoded_optimized_image = encode(o.read())
        
      # Return a response in JSON
      return res.json(
          {
            "success:" : True,
            "image": str(encoded_optimized_image)
          })
  except Exception as e:
    return res.json({"success": False, "message": str(e)})