import base64
import requests
import tinify
import json


def krakenio_impl(variables):
    # Kraken Url for uploading media
    url = 'https://api.kraken.io/v1/'
    api_endpoint = url + 'upload'

    # Headers for post request
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.85 Safari/537.36'
    }
    # File that we will pass in
    files = {'file': variables['decoded_image']}
    # Parameters for post request
    params = {
        "auth": {
            "api_key": variables['api_key'],
            "api_secret":variables['api_secret_key']
        },
        "wait": True,  # Optional: Wait for the optimization to complete
        "dev": False  # Optional: Set to false to use API
    }
    response = requests.post(url=api_endpoint,
                             headers=headers,
                             files=files,
                             data={'data': json.dumps(params)},
                             timeout=10)

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
        raise ValueError("KrakenIO failed to compress.")


def tinypng_impl(variables):
    tinify.key = variables['api_key']
    result_data = tinify.from_buffer(variables['decoded_image']).to_buffer()
    return {"success": True, "optimized_image": result_data}


def validate_payload(req):
    # Accessing payload
    if req.payload == {}:
        raise ValueError("Missing payload")

    # Accessing provider from payload
    if req.payload['provider'] is None or req.payload['provider'].lower(
    ) not in ['krakenio', 'tinypng']:
        raise ValueError("Invalid provider.")

    # Acccessing variables
    if req.variables == {}:
        raise ValueError("Missing variables.")

    # Accessing api_key from variables
    if req.variables['API_KEY'] == "":
        raise ValueError("Missing API key.")

    # Accessing encoded image from payload
    if req.payload['image'] == "":
        raise ValueError("Missing encoded image.")

    result = {
        "provider": req.payload['provider'],
        "api_key": req.variables['API_KEY'],
        "decoded_image": base64.b64decode(req.payload['image'])
    }

    # Get secret key
    if req.payload['provider'] == "krakenio":
        if req.variables['SECRET_API_KEY'] == "":
            raise ValueError("Missing api secret key.")
        result["api_secret_key"] = req.variables['SECRET_API_KEY']
    return result


def main(req, res):
    try:
        variables = validate_payload(req)
    except Exception as validate_message:
        return res.json({"success": False, "Invalid Request": str(validate_message)})

    # Run the api function
    try:
        if variables['provider'].lower() == 'krakenio':
            result = krakenio_impl(variables)
        else:
            result = tinypng_impl(variables)
    except RuntimeError as api_message:
        return res.json({"success": False, "API Failed to compress image": api_message})
        
    # Return a response in JSON
    return res.json({
        "success:": True,
        "image": str(base64.b64encode(result['optimized_image']))
    })