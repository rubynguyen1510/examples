import base64
import tinify
import tempfile
import os
import requests
import json
def check_size(optimized_image_path, decoded_image_path):
    optimize_size = os.path.getsize(optimized_image_path)
    decode_size = os.path.getsize(decoded_image_path)
    return optimize_size < decode_size


def krakenio_impl(api_key, api_secret_key, encoded_image):
    url = 'https://api.kraken.io/v1/'
    api_endpoint = url + 'upload'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.85 Safari/537.36'
    }
    files = {
            'file': base64.b64decode(encoded_image)
    }
    params = {
        "auth": {
            "api_key": api_key,
            "api_secret": api_secret_key
        },
        "wait": True,  # Optional: Wait for the optimization to complete
        "dev": True
    }
    response = requests.post(url=api_endpoint, headers=headers, files=files, data={'data': json.dumps(params)}, timeout=10)
    print(response.json())
    if response.status_code == 200:
        # Request successful, parse the response
        data = response.json()
        if data["success"]:
            optimized_url = data["kraked_url"]
            # Process the optimized image URL as needed
            print("Optimized URL:", optimized_url)
        else:
            # Request unsuccessful, handle the error
            error_message = data["error"]
            print("Kraken.io API error:", error_message)
    else:
        # Request unsuccessful, handle the error
        print("Request failed with status code:", response.status_code)


def tinypng_impl(api_key, encoded_image):
    # # Authenticating Tinypng API Key
    # tinify.key = api_key
    # # Compress image using Tinypng and write it to optimized image path.
    # optimized_image = tinify.from_file(decoded_image_path)
    # optimized_image.to_file(optimized_image_path)

    # # Check if the api compression worked. 
    # # Compares the optimized file and the original file sizes.
    # return check_size(optimized_image_path, decoded_image_path)


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
        # Create a temp directory inside of the current working directory.
        # Prefix it as "temp"
        temp_dir = tempfile.mkdtemp(prefix='temp', dir=os.getcwd())
        # Generate a copy of the decoded image data as non_optimized.jpg
        decoded_image_path = os.path.join(temp_dir, "non_optimized_image.jpg")
        # We are making a new optimized_image.jpg into temp directory
        optimized_image_path = os.path.join(temp_dir, "optimized_image.jpg")
    except Exception as e:
        return res.json({"success": False, "message": str(e)})
    
    with open(decoded_image_path, "wb") as i:
        i.write(decoded_image)

    # Run the API function
    successful = False
    if provider.lower() == 'krakenio':
        successful = krakenio_impl(api_key, api_secret_key, decoded_image_path, optimized_image_path)
    else:
        successful = tinypng_impl(api_key, decoded_image_path, optimized_image_path)

    # Package by encoding the file in base64 format
    with open(optimized_image_path, "rb") as o:
        encoded_optimized_image = base64.b64encode(o.read())

    # Delete the decoded image and the optimized image, then delete the temporary directory
    # os.remove(decoded_image_path)
    # os.remove(optimized_image_path)
    # os.rmdir(temp_dir)

    # Return a response in JSON
    if successful:
        return res.json({"success:": True, "image": str(encoded_optimized_image)})
    else:
        return res.json({"success:": False, "image": "Image failed to compress."})
