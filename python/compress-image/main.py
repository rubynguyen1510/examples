
"""
base64 import
"""
import base64
import json
import tinify
import requests


def krakenio_impl(variables):
    """
    Implements image optimization using the Kraken.io API.

    Input:
        variables (dict): A dictionary containing the
                          required variables for optimization.

    Returns:
        str: Base64 encoded optimized image.

    Raises:
        requests.exceptions.HTTPError: If there is an HTTP
                                       error during the API request.
        requests.exceptions.ReadTimeout: If the API request times out.
        requests.exceptions.ConnectionError: If there is a connection error.
        Exception: For any other unexpected errors.
    """
    optimized_image = None
    # Kraken Url for uploading media
    url = "https://api.kraken.io/v1/"
    api_endpoint = url + "upload"
    # Headers for post request
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/40.0.2214.85 Safari/537.36"
    }
    # File that we will pass in
    files = {"file": variables["decoded_image"]}
    # Parameters for post request
    params = {
        "auth": {
            "api_key": variables["api_key"],
            "api_secret": variables["api_secret_key"]
        },
        "wait": True,  # Optional: Wait for the optimization to complete
        "dev": False  # Optional: Set to false to use API
    }
    try:
        response = requests.post(url=api_endpoint,
                                 headers=headers,
                                 files=files,
                                 data={"data": json.dumps(params)},
                                 timeout=10)
        response.raise_for_status()
    except (requests.exceptions.HTTPError, requests.exceptions.ReadTimeout,
            requests.exceptions.ConnectionError) as request_error:
        raise type(request_error)(str(request_error))
    except Exception as exception_error:
        raise Exception(str(exception_error))
    # Check status code of response
    if response.status_code == 200:
        # Request successful, parse the response
        data = response.json()
        if data["success"] is True:
            optimized_url = data["kraked_url"]
            optimized_image = requests.get(optimized_url, timeout=10).content
    return str(base64.b64encode(optimized_image))


def tinypng_impl(variables):
    """
    Implements image optimization using the Tinypng API.

    Input:
        variables (dict): A dictionary containing the required variables
        for optimization. Includes api_key and decoded_image.

    Returns:
        str: Base64 encoded optimized image.

    Raises:
        tinify.errors.AccountError: If there is an account-related error
                                    during the API request.
        tinify.errors.ClientError: If there is a client-related error during
                                   the API request.
        KeyError: If a required key is missing in the variables dictionary.
        Exception: For any other unexpected errors.
    """
    tinify.key = variables["api_key"]
    try:
        optimized_image = (tinify.from_buffer(variables["decoded_image"]).
                           to_buffer())
    except (tinify.errors.AccountError, tinify.errors.ClientError, KeyError) as tinify_error:
        raise type(tinify_error)(str(tinify_error))
    except Exception as exception_error:
        raise Exception(str(exception_error))
    return str(base64.b64encode(optimized_image))


def validate_request(req):
    """
    Validates the request and extracts the necessary information.

    Input:
        req: The request object containing the payload and variables.

    Returns:
        dict: A dictionary containing the validated payload information.

    Raises:
        ValueError: If any required value is missing or invalid.
    """
    # Accessing payload
    if req.payload == {}:
        raise ValueError("Missing payload")
    # Accessing provider from payload
    if req.payload["provider"] is None or req.payload["provider"].lower(
    ) not in ["krakenio", "tinypng"]:
        raise ValueError("Invalid provider.")
    # Acccessing variables
    if req.variables == {}:
        raise ValueError("Missing variables.")
    # Accessing api_key from variables
    if req.variables["API_KEY"] == "":
        raise ValueError("Missing API key.")
    # Accessing encoded image from payload
    if req.payload["image"] == "":
        raise ValueError("Missing encoded image.")
    result = {
        "provider": req.payload["provider"],
        "api_key": req.variables["API_KEY"],
        "decoded_image": base64.b64decode(req.payload["image"])
    }
    # Get secret key
    if req.payload["provider"] == "krakenio":
        if req.variables["SECRET_API_KEY"] == "":
            raise ValueError("Missing api secret key.")
        result["api_secret_key"] = req.variables["SECRET_API_KEY"]
    return result


def main(req, res):
    """
    The main function that runs Validate Payload and calls implementations.

    Input:
        req: The request object.
        res: The response object.

    Returns:
        dict: A JSON response containing the optimization results.
    """
    try:
        variables = validate_request(req)
    except (ValueError, KeyError) as payload_error:
        return res.json({
            "success": False,
            str(type(payload_error).__name__): str(payload_error)
        })
    implementations = {
        "krakenio": krakenio_impl,
        "tinypng": tinypng_impl
    }
    try:
        optimized_image = implementations[variables["provider"]](variables)
    except (requests.exceptions.HTTPError, requests.exceptions.ReadTimeout,
            requests.exceptions.ConnectionError, tinify.errors.AccountError,
            tinify.errors.ClientError, KeyError) as implementation_error:
        return res.json({
            "success": False,
            str(type(implementation_error).__name__): str(implementation_error)
        })
    except Exception as error:
        return res.json({
            "success": False,
            "Error": str(error)
        })
    return res.json({
        "success:": True,
        "image": (optimized_image)
    })
