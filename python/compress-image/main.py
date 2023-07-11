import base64
import json
import tinify
import requests


def krakenio_impl(variables):
    error = None
    optimized_image = None
    # Kraken Url for uploading media
    url = 'https://api.kraken.io/v1/'
    api_endpoint = url + 'upload'

    # Headers for post request
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/40.0.2214.85 Safari/537.36'
    }
    # File that we will pass in
    files = {'file': variables['decoded_image']}
    # Parameters for post request
    params = {
        "auth": {
            "api_key": variables['api_key'],
            "api_secret": variables['api_secret_key']
        },
        "wait": True,  # Optional: Wait for the optimization to complete
        "dev": False  # Optional: Set to false to use API
    }    
    try:
        response = requests.post(url=api_endpoint,
                                 headers=headers,
                                 files=files,
                                 data={'data': json.dumps(params)},
                                 timeout=10)
        response.raise_for_status()

    except (requests.exceptions.HTTPError, requests.exceptions.ReadTimeout,
             requests.exceptions.ConnectionError) as error:
        raise type(error)(str(error))

    except Exception as error:
        raise Exception(str(error))
    
    # Check status code of response
    if response.status_code == 200:
        # Request successful, parse the response
        data = response.json()
        if data["success"] is True:
            optimized_url = data["kraked_url"]
            optimized_image = requests.get(optimized_url, timeout=10).content
            
    return (optimized_image)


def tinypng_impl(variables):
    tinify.key = variables['api_key']
    try:
        optimized_image = tinify.from_buffer(variables['decoded_image']).to_buffer()
    except (tinify.errors.AccountError, tinify.errors.ClientError, KeyError) as error:
        raise type(error)(str(error))
    except Exception as error:
        raise Exception(str(error))
    return optimized_image


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
    except (ValueError, KeyError) as error:
        return res.json({
            "success": False,
            str(type(error).__name__): str(error)
        })

    implementations = {
        "krakenio": krakenio_impl,
        "tinypng": tinypng_impl
    }

    try:
        optimized_image = implementations[variables["provider"]](variables)
    except (requests.exceptions.HTTPError, requests.exceptions.ReadTimeout,
            requests.exceptions.ConnectionError, tinify.errors.AccountError,
            tinify.errors.ClientError, KeyError) as error:
        return res.json({
            "success": False,
            str(type(error).__name__): str(error)
        })
    except Exception as error:
        return res.json({
            "success": False,
            "Error": str(error)
        })
    return res.json({
        "success:": True,
        "image": str(base64.b64encode(optimized_image))
    })
