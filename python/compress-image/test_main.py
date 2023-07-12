import unittest
import base64
import pathlib
import secret
import main
import tinify
import requests
from unittest.mock import MagicMock, patch
import requests.exceptions
import json


class TestMain(unittest.TestCase):

    def test_krakenio_small(self):
        # Output validation 1KB
        want = base64.b64decode(pathlib.Path(
            secret.RESULT_1KB_KRAKENIO).read_text())
        got = main.krakenio_impl({"api_key": secret.API_KEY_KRAKENIO, 
                                  "api_secret_key": 
                                  secret.SECRET_API_KEY_KRAKENIO, 
                                  "decoded_image": pathlib.Path(
                                    secret.IMAGE_1KB).read_bytes()})
        self.assertEqual(got, want)

    def test_krakenio_big(self):
        # Output validation 3MB
        want = base64.b64decode(pathlib.Path(
            secret.RESULT_3MB_KRAKENIO).read_text())
        got = main.krakenio_impl({"api_key": secret.API_KEY_KRAKENIO,
                                  "api_secret_key":
                                  secret.SECRET_API_KEY_KRAKENIO,
                                  "decoded_image": pathlib.Path(
                                    secret.IMAGE_3MB).read_bytes()})
        self.assertEqual(got, want)

    def test_krakenio_wrong_api_key(self):
        self.assertRaises(requests.exceptions.HTTPError, main.krakenio_impl, 
                          {"api_key": secret.API_KEY_KRAKENIO,
                            "api_secret_key": "1234",
                            "decoded_image": pathlib.Path(
                            secret.IMAGE_1KB).read_bytes()})
        
    def test_krakenio_wrong_api_secret_key(self):
        self.assertRaises(requests.exceptions.HTTPError, main.krakenio_impl, 
                          {"api_key": "1234",
                            "api_secret_key": 
                            secret.SECRET_API_KEY_KRAKENIO,
                            "decoded_image": pathlib.Path(
                            secret.IMAGE_1KB).read_bytes()})

    def test_krakenio_corrupted_image(self):
        self.assertRaises(requests.exceptions.HTTPError, main.krakenio_impl, 
                          {"api_key": secret.API_KEY_KRAKENIO,
                            "api_secret_key": 
                            secret.SECRET_API_KEY_KRAKENIO,
                            "decoded_image": "123"})
    
    def test_krakenio_time_out(self):
        with patch("main.requests.post") as mock_post:
            mock_post.side_effect = requests.exceptions.ReadTimeout
            with self.assertRaises(requests.exceptions.ReadTimeout):
                main.krakenio_impl({
                    "api_key": secret.API_KEY_KRAKENIO,
                    "api_secret_key": secret.SECRET_API_KEY_KRAKENIO,
                    "decoded_image": pathlib.Path(secret.IMAGE_1KB).read_bytes()
                })
            mock_post.assert_called_once()
    
    def test_krakenio_connection_error(self):
        with patch("main.requests.post") as mock_post:
            mock_post.side_effect = requests.exceptions.ConnectionError
            with self.assertRaises(requests.exceptions.ConnectionError):
                main.krakenio_impl({
                    "api_key": secret.API_KEY_KRAKENIO,
                    "api_secret_key": secret.SECRET_API_KEY_KRAKENIO,
                    "decoded_image": pathlib.Path(secret.IMAGE_1KB).read_bytes()
                })
            mock_post.assert_called_once()

    def test_tinypng_small(self):
        want = base64.b64decode(pathlib.Path(secret.RESULT_1KB_TINYPNG).read_text())
        got = main.tinypng_impl({"api_key": secret.API_KEY_TINYPNG, "decoded_image": pathlib.Path(secret.IMAGE_1KB).read_bytes()})
        self.assertEqual(got, want)

    def test_tinypng_big(self):
        want = base64.b64decode(pathlib.Path(secret.RESULT_3MB_TINYPNG).read_text())
        got = main.tinypng_impl({"api_key": secret.API_KEY_TINYPNG, "decoded_image": pathlib.Path(secret.IMAGE_3MB).read_bytes()})
        self.assertEqual(got, want)

    def test_tinypng_credential(self):
        # Empty Credentials
        self.assertRaises(tinify.errors.AccountError, main.tinypng_impl, {"api_key": "", "decoded_image": pathlib.Path(secret.IMAGE_1KB).read_bytes()} )
        # # Incorrect Credentials
        self.assertRaises(tinify.errors.AccountError, main.tinypng_impl, {"api_key": "1NCORRECT4CREDENT1ALS", "decoded_image": pathlib.Path(secret.IMAGE_1KB).read_bytes()} )

    def test_tinypng_image(self):
        # Image is Empty
        self.assertRaises(tinify.errors.ClientError, main.tinypng_impl, {"api_key": secret.API_KEY_TINYPNG, "decoded_image": b''} )
        # Corrupted Image
        self.assertRaises(tinify.errors.ClientError, main.tinypng_impl, {"api_key": secret.API_KEY_TINYPNG, "decoded_image": b'ORw0KGgoAAAANSUhEUgAAABEAAAAOCAMAAAD+M'} )

    def test_tinypng_keys(self):
        # Accessing wrong key
        self.assertRaises(KeyError, main.tinypng_impl, {"a": secret.API_KEY_TINYPNG, "decoded_image": pathlib.Path(secret.IMAGE_1KB).read_bytes()})
        self.assertRaises(KeyError, main.tinypng_impl, {"api_key": secret.API_KEY_TINYPNG, "code_image": pathlib.Path(secret.IMAGE_1KB).read_bytes()})

        # Empty Key
        self.assertRaises(KeyError, main.tinypng_impl, {"": secret.API_KEY_TINYPNG, "code_image": pathlib.Path(secret.IMAGE_1KB).read_bytes()})
        self.assertRaises(KeyError, main.tinypng_impl, {"api_key": secret.API_KEY_TINYPNG, "": pathlib.Path(secret.IMAGE_1KB).read_bytes()})
        self.assertRaises(KeyError, main.tinypng_impl, {"": secret.API_KEY_TINYPNG, "": pathlib.Path(secret.IMAGE_1KB).read_bytes()})

    def test_tinypng_variables(self):
        self.assertRaises(KeyError, main.tinypng_impl, {})
        self.assertRaises(KeyError, main.tinypng_impl, {"api_key": "your_api_key"}) #Missing decoded_image variable

    def test_tinypng_return_type(self):
        with patch("main.tinify.from_buffer") as mock_from_buffer:
            mock_from_buffer.return_value.to_buffer.return_value = b''
            got = main.tinypng_impl({"api_key": secret.API_KEY_TINYPNG, "decoded_image": b''})
            self.assertIsInstance(got, bytes)

            mock_from_buffer.return_value.to_buffer.return_value = base64.b64decode( pathlib.Path(secret.RESULT_3MB_TINYPNG).read_text() )
            optimized_image = main.tinypng_impl({"api_key": secret.API_KEY_TINYPNG, "decoded_image": pathlib.Path(secret.IMAGE_3MB).read_bytes()})
            self.assertIsInstance(optimized_image, bytes)

    def test_tinypng_impl_basic_functionality(self):
        with patch("main.tinify.from_buffer") as mock_from_buffer:
            # Set up the mock return value
            mock_from_buffer.return_value.to_buffer.return_value = pathlib.Path(secret.RESULT_1KB_TINYPNG).read_text()
            # Assert the expected result
            self.assertEqual(main.tinypng_impl({"api_key": secret.API_KEY_TINYPNG, "decoded_image": pathlib.Path(secret.IMAGE_1KB).read_bytes()}), pathlib.Path(secret.RESULT_1KB_TINYPNG).read_text())
            # Assert that the mocked methods were called
            mock_from_buffer.assert_called_once_with(pathlib.Path(secret.IMAGE_1KB).read_bytes())
            mock_from_buffer.return_value.to_buffer.assert_called_once()

    def test_tinypng_impl_unexpected_exception(self):
        with patch("main.tinify.from_buffer") as mock_from_buffer:
            mock_from_buffer.side_effect = tinify.errors.AccountError("API Key is wrong")

            #Check assert raise 
            self.assertRaises(tinify.errors.AccountError, main.tinypng_impl, {"api_key": secret.API_KEY_TINYPNG, "decoded_image": pathlib.Path(secret.IMAGE_1KB).read_bytes()})
            
            #Check contents of raise error
            with self.assertRaises(tinify.errors.AccountError) as cm:
                main.tinypng_impl({"api_key": secret.API_KEY_TINYPNG, "decoded_image": pathlib.Path(secret.IMAGE_1KB).read_bytes()})
            self.assertEqual(str(cm.exception), "API Key is wrong")

    def test_main(self):
        # Output validation 1KB
        want = {
            "success:": True,
            "image": pathlib.Path(secret.RESULT_1KB_TINYPNG).read_text() 
        }

        req = MockRequest({
            "payload": {
                "provider": "tinypng",
                "image": str(base64.b64encode(pathlib.Path(secret.IMAGE_1KB).read_bytes()), 'utf-8')
            },
            "variables": {
                "API_KEY": secret.API_KEY_TINYPNG
            }
        })

        res = MockResponse()  # Create a mock response object
        main.main(req, res)
        
        # Check the response
        got = res.json()
        self.maxDiff = None
        self.assertEqual(got, want)

# Define a mock request class
class MockRequest:
    def __init__(self, data):
        self.payload = data.get("payload", {})
        self.variables = data.get("variables", {})

# Define a mock response class
class MockResponse:
    def __init__(self):
        self._json = None

    def json(self):
        return self._json

    def json(self, data=None):
        if data is not None:
            self._json = data
        return self._json
    
if __name__ == '__main__':
    unittest.main()