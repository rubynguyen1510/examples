import unittest
import base64
import pathlib
import secret
import main
import tinify
import requests
# from main import tinypng_impl

class TestMain(unittest.TestCase):

    def test_krakenio_small(self):
        # Output validation 1KB
        want = base64.b64decode(pathlib.Path(
            secret.RESULT_1KB_KRAKENIO).read_text())
        got = main.krakenio_impl({"api_key": secret.API_KEY_KRAKENIO, "api_secret_key": secret.SECRET_API_KEY_KRAKENIO, "decoded_image": pathlib.Path(secret.IMAGE_1KB).read_bytes()})
        self.assertIsNone(got[0])
        self.assertEqual(got[1], want)

    def test_krakenio_big(self):
        # Output validation 3MB
        want = base64.b64decode(pathlib.Path(secret.RESULT_3MB_KRAKENIO).read_text())
        got = main.krakenio_impl({"api_key": secret.API_KEY_KRAKENIO, "api_secret_key": secret.SECRET_API_KEY_KRAKENIO, "decoded_image": pathlib.Path(secret.IMAGE_3MB).read_bytes()})
        self.assertIsNone(got[0])
        self.assertEqual(got[1], want)


if __name__ == '__main__':
    unittest.main()