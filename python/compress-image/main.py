import base64
import tinify
import tempfile
import os
import json
import requests

'''
input base 64 format : iVBORw0KGgoAAAANSUhEUgAAAaQAAALiCAY...QoH9hbkTPQAAAABJRU5ErkJggg== 
output : bytes 
'''
def decode(encoded_value):
    decoded = base64.b64decode(encoded_value)
    return decoded

'''
input : open media file, bytes
output : encoded base 64 
'''
def encode(plaintext):
    encoded = base64.b64encode(plaintext)
    return encoded

res = None

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
    # We are making a new optimized_image.jpg into temp directory
    optimized_image_path = os.path.join(temp_dir, "optimized_image.jpg")

    with open(decoded_image_path, "wb") as i:
        i.write(decoded_image)
    
    if provider == 'krakenio':
      # path = os.getcwd()
      init_file_path = "/usr/local/src/userlib/__init__.py"
      kraken_replace_path = "/usr/local/src/userlib/runtime-env/lib/python3.10/site-packages/krakenio/__init__.py"

      init_file = open(init_file_path, "rt")
      with open(kraken_replace_path, "w") as kraken_file:
        kraken_file.write(init_file.read())
      os.remove(init_file_path)

      from krakenio import Client

      api_secret_key = variable['SECRET_API_KEY']
      # Authenticate the API Key and Secret Key
      api = Client(api_key, api_secret_key)
      data = {
          'wait': True,
          'dev': True
      }
      # Uploading the decoded_image_path to the KrakenIO
      result = api.upload(decoded_image_path, data)
      if result.get('success'):
          optimized_image_url = result.get('kraked_url')
          # Opening the newly created file and writing to the empty file
          with open(optimized_image_path, 'wb') as f:
              optimized_image = requests.get(optimized_image_url, stream=True).content
              f.write(optimized_image)
      else:
        os.remove(decoded_image_path)
        os.remove(optimized_image_path)
        os.rmdir(temp_dir)
        return res.json({"success": False, "message": "krakenio failed to compress image"})
    else:
      # Authenticating api key
      tinify.key = api_key
      # Use that cloned file path to compress image using TinyPNG api
      optimized_image = tinify.from_file(decoded_image_path)
      optimized_image.to_file(optimized_image_path)
      
    # Package by encoding the file in base64 format
    o = open(optimized_image_path, "rb")
    encoded_optimized_image = encode(o.read())
    o.close()

    os.remove(decoded_image_path)
    os.remove(optimized_image_path)
    os.rmdir(temp_dir)
    # Return a response in JSON
    return res.json(
    {
      "success:" : True,
      "image": str(encoded_optimized_image)
    })
  except Exception as e:
    return res.json(
      {
        "success": False, 
        "message": str(e)
      })