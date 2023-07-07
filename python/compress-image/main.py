import base64
import requests
import tinify
import json


def krakenio_impl(api_key, api_secret_key, decoded_image):
    # Kraken Url for uploading media
    url = 'https://api.kraken.io/v1/'
    api_endpoint = url + 'upload'

    # Headers for post request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.85 Safari/537.36'
    }
    # File that we will pass in
    files = {
            'file': decoded_image
    }
    # Parameters for post request
    params = {
        "auth": {
            "api_key": api_key,
            "api_secret": api_secret_key
        },
        "wait": True,  # Optional: Wait for the optimization to complete
        "dev": False  # Optional: Set to false to use API
    }
    response = requests.post(url=api_endpoint, headers=headers, files=files, data={'data': json.dumps(params)}, timeout=10)

    # Check status code of response
    if response.status_code == 200:
        # Request successful, parse the response
        data = response.json()
        if data["success"] is True:
            optimized_url = data["kraked_url"]
            # Return the contents of the url as decoded
            return {
                "success": True,
                "optimized_image": requests.get(optimized_url).content
            }
    else:
        return {
            "success": False
        }


def tinypng_impl(api_key, decoded_image):
    tinify.key = api_key
    result_data = tinify.from_buffer(decoded_image).to_buffer()
    return {
        "success": True,
        "optimized_image": result_data
    }


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
        if encoded_image == "":
            raise ValueError("Missing encoded image.")

        # Decoding the encoded image
        decoded_image = base64.b64decode(encoded_image)

    except Exception as message:
        return res.json({"success": False, "message": str(message)})

    # Run the api function
    if provider.lower() == 'krakenio':
        result = krakenio_impl(api_key, api_secret_key, decoded_image)
    else:
        result = tinypng_impl(api_key, decoded_image)

    # Return a response in JSON
    if result['success']:
        optimized_image = result['optimized_image']
        return res.json({"success:": True,
                         "image": str(base64.b64encode(optimized_image))})
    else:
        return res.json({"success:": False, "image":
                         "Image failed to compress."})
