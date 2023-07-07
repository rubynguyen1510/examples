import base64
import tinify
import tempfile
import os
import requests

# There is an error with KrakenIO for Python3. 
# We provided a solution by replacing init.py inside KrakenIO.
init_file_path = os.getcwd() + "/userlib/__init__.py"
kraken_replace_path = os.getcwd() + "/userlib/runtime-env/lib/python3.10/site-packages/krakenio/__init__.py"

init_file = open(init_file_path, "rt")
with open(kraken_replace_path, "w") as kraken_file:
    kraken_file.write(init_file.read())
os.remove(init_file_path)
from krakenio import Client


def check_size(optimized_image_path, decoded_image_path):
    optimize_size = os.path.getsize(optimized_image_path)
    decode_size = os.path.getsize(decoded_image_path)
    return optimize_size < decode_size


'''
input: variable, api_key, decoded_image_path, optimized_image_path
'''
def krakenio_impl(api_key, api_secret_key, decoded_image_path, optimized_image_path):
  # Authenticate the API Key and Secret Key
  api = Client(api_key, api_secret_key)
  data = {
    'wait': True,
    # If you are testing, make sure to have dev -> True. If false then we will use API data.
    'dev': True
  }
  # Uploading the decoded_image_path to the KrakenIO
  result = api.upload(decoded_image_path, data)

  # Check if the result is successful
  if result.get('success'):
    optimized_image_url = result.get('kraked_url')
    # Writing the contents from KrakenIO into the optimized image path.
    with open(optimized_image_path, 'wb') as f:
      optimized_image = requests.get(optimized_image_url, stream=True).content
      f.write(optimized_image)
    # Check if the api compression worked. Compares the optimized file and the original file sizes.
    return check_size(optimized_image_path, decoded_image_path)


def tinypng_impl(api_key, decoded_image_path, optimized_image_path):
  # Authenticating Tinypng API Key
  tinify.key = api_key
  # Compress image using Tinypng and write it to optimized image path.
  optimized_image = tinify.from_file(decoded_image_path)
  optimized_image.to_file(optimized_image_path)

  # Check if the api compression worked. Compares the optimized file and the original file sizes.
  return check_size(optimized_image_path, decoded_image_path)


res = None

def main(req, res):
  try:
    # Accessing payload
    payload = req.payload
    if payload == {}:
      raise ValueError("Missing payload")

    # Accessing provider from payload
    provider = payload['provider']
    if provider is None or provider.lower() not in ['krakenio', 'tinypng']:
      raise ValueError("Invalid provider.")

    # Acccessing variables
    variable = req.variables
    if variable == {}:
      raise ValueError("Missing variables.")

    # Accessing api_key from variables
    api_key = variable['API_KEY']
    if api_key == "":
      raise ValueError("Missing API key.")

    # Get secret key if krakenio
    if provider == "krakenio":
      api_secret_key = variable['SECRET_API_KEY']
      if api_secret_key == "":
        raise ValueError("Missing API secret key.")

    # Accessing encoded image from payload
    encoded_image = payload['image']
    # if encoded_image == "":
    #   raise ValueError("Missing encoded image.")

    # Decoding the encoded image
    decoded_image = base64.b64decode(encoded_image)
    # Create a temp directory inside of the current working directory. Prefix it as "temp"
    temp_dir = tempfile.mkdtemp(prefix='temp', dir=os.getcwd())
    # Generate a copy of the decoded image data as non_optimized.jpg
    decoded_image_path = os.path.join(temp_dir, "non_optimized_image.jpg")
    # We are making a new optimized_image.jpg into temp directory
    optimized_image_path = os.path.join(temp_dir, "optimized_image.jpg")

  except Exception as e:
    return res.json({"success": False, "message": str(e)})

  with open(decoded_image_path, "wb") as i:
    i.write(decoded_image)

  # Run the api function
  sucessful = False
  if provider.lower() == 'krakenio':
    sucessful = krakenio_impl(api_key, api_secret_key, decoded_image_path,
                              optimized_image_path)
  else:
    sucessful = tinypng_impl(api_key, decoded_image_path, optimized_image_path)

  # Package by encoding the file in base64 format
  o = open(optimized_image_path, "rb")
  encoded_optimized_image = base64.b64encode(o.read())
  o.close()

  # Delete the decoded image and the optimized image, then delete the temporary directory
  # os.remove(decoded_image_path)
  # os.remove(optimized_image_path)
  # os.rmdir(temp_dir)

  # Return a response in JSON
  if sucessful:
    return res.json({"success:": True, "image": str(encoded_optimized_image)})
  else:
    return res.json({"success:": False, "image": "Image failed to compress."})