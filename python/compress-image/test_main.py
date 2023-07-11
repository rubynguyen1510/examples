import unittest
import base64
import pathlib
import secret
import main
import tinify
import requests
from unittest.mock import MagicMock, patch
import requests.exceptions

# from main import tinypng_impl

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



if __name__ == '__main__':
    unittest.main()