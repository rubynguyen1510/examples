import json
import base64
import requests


def upload():
    # Provide your Kraken.io API credentials
    api_key = "f66cec6f44df73d3ba48d8dbce302738"
    api_secret = "7bbd29dd53c00a068b7ebe20b074540a0d7cea9d"
    url = 'https://api.kraken.io/v1/'
    api_endpoint = url + 'upload'
    file_path = '10mb.jpg'
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.85 Safari/537.36'
    }

    files = {
            'file': open(file_path, 'rb')
    }

    params = {
        "auth": {
            "api_key": api_key,
            "api_secret": api_secret
        },
        "wait": True,  # Optional: Wait for the optimization to complete
        "dev": True
    }
    # response = requests.get(api_endpoint)
    response = requests.post(url=api_endpoint, headers=headers, files=files, data={'data': json.dumps(params)}, timeout=10)
    print(response.json())

    # Check the response status code
    if response.status_code == 200:
        # Request successful, parse the response
        data = response.json()
        if data["success"]:
            optimized_url = data["kraked_url"]
            # Process the optimized image URL as needed
            print("Optimized URL:", optimized_url)
            value = requests.get(optimized_url).content
            file = open("output/output.txt", "w")
            file.write(str(value))
        else:
            # Request unsuccessful, handle the error
            error_message = data["error"]
            print("Kraken.io API error:", error_message)
    else:
        # Request unsuccessful, handle the error
        print("Request failed with status code:", response.status_code)


# upload()


def upload_string(encoded):
    api_key = "f66cec6f44df73d3ba48d8dbce302738"
    api_secret = "7bbd29dd53c00a068b7ebe20b074540a0d7cea9d"

    url = 'https://api.kraken.io/v1/'
    api_endpoint = url + 'upload'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.85 Safari/537.36'
    }
    value = base64.b64decode(encoded.read())
    # print(value)

    files = {
            'file': value
    }

    params = {
        "auth": {
            "api_key": api_key,
            "api_secret": api_secret
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


file = open('200_kb.txt')
upload_string(file)


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
