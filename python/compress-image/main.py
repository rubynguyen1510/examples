""" Compress image function using Tinypng and Krakenio API """
import base64
import json
import tinify
import requests

KRAKEN_API_ENDPOINT = "https://api.kraken.io/v1/upload"
KRAKEN_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64)AppleWebKit/"
    "537.36(KHTML, like Gecko)Chrome/40.0.2214.85 Safari/537.36"
)


def krakenio_impl(variables):
    """
    Implements image optimization using the Kraken.io API.
    
    Input:
        variables (dict): A dictionary containing the
                          required variables for optimization.
    Returns:
        bytes: decoded optimized image.
    """
    optimized_image = None
    # Headers for post request
    headers = {"User-Agent": KRAKEN_USER_AGENT}
    # Image that we will pass in
    files = {"file": variables["decoded_image"]}
    # Parameters for post request
    params = {
        "auth": {
            "api_key": variables["api_key"],
            "api_secret": variables["api_secret_key"]
        },
        "wait": True,  # Optional: Wait for the optimization to complete
        "dev": False,  # Optional: Set to false to enter user mode.
    }
    response = requests.post(
        url=KRAKEN_API_ENDPOINT,
        headers=headers,
        files=files,
        json={"data": params},
        timeout=10,
    )
    # Check status code of response
    if response.ok:
        # Request successful, parse the response
        data = response.json()
        if data["success"]:
            optimized_url = data["kraked_url"]
            optimized_image = requests.get(optimized_url, timeout=10).content
    return optimized_image


def tinypng_impl(variables):
    """
    Implements image optimization using the Tinypng API.
    Input:
        variables (dict): A dictionary containing the required variables
        for optimization. Includes api_key and decoded_image.
    Returns:
        bytes: decoded optimized image.
    """
    tinify.key = variables["api_key"]
    optimized_image = (tinify.from_buffer(
        variables["decoded_image"]).to_buffer())
    return optimized_image


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
    # Check if payload is empty
    if not req.payload:
        raise ValueError("Missing payload")
    # Accessing provider from payload
    if not req.payload.get("provider"):
        raise ValueError("Missing provider")
    # Check if payload is not empty
    if not req.variables:
        raise ValueError("Missing variables.")
    # Accessing api_key from variables
    if not req.variables.get("API_KEY"):
        raise ValueError("Missing API_KEY")
    # Accessing encoded image from payload
    if not req.payload.get("image"):
        raise ValueError("Missing encoding image")
    result = {
        "provider": req.payload.get("provider").lower(),
        "api_key": req.variables.get("API_KEY"),
        "decoded_image": base64.b64decode(req.payload.get("image"))
    }
    # Get secret key
    if req.payload.get("provider") == "krakenio":
        if not req.variables.get("SECRET_API_KEY"):
            raise ValueError("Missing api secret key.")
        result["api_secret_key"] = req.variables.get("SECRET_API_KEY")
    return result


IMPLEMENTATIONS = {"krakenio": krakenio_impl, "tinypng": tinypng_impl}


def main(req, res):
    """
    The main function that runs Validate Payload and calls IMPLEMENTATIONS.

    Input:
        req: The request object.
        res: The response object.

    Returns:
        dict: A JSON response containing the optimization results.
    """
    try:
        variables = validate_request(req)
    except (ValueError) as payload_error:
        return res.json({"success": False, "Value Error": str(payload_error)})
    try:
        optimized_image = IMPLEMENTATIONS[variables["provider"]](variables)
    except Exception as error:
        return res.json({
            "success": False,
            "error": f"{str(type(error).__name__)} {str(error)}"
        })
    return res.json({
        "success": True,
        "image": base64.b64encode(optimized_image).decode()
    })
