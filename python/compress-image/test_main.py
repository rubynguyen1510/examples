import unittest
import base64
import pathlib
import secret
import main
# from main import tinypng_impl


class TestMain(unittest.TestCase):

    def setUp(self):
        # self.api_key_tinypng = YOUR API_KEY
        # self.api_key_krakenio = secret.API_KEY_KRAKENIO
        # self.secret_api_key_krakenio = secret.SECRET_API_KEY_KRAKENIO

        self.api_key_tinypng = secret.API_KEY_TINYPNG
        self.api_key_krakenio = secret.API_KEY_KRAKENIO
        self.secret_api_key_krakenio = secret.SECRET_API_KEY_KRAKENIO

    def test_tinypng_small(self):
        # Output validation 1KB
        want = base64.b64decode( pathlib.Path("python/compress-image/test/1kb/1kb_result_encoded_tinypng.txt").read_text() )
        got = main.tinypng_impl({"api_key": self.api_key_tinypng, "decoded_image": pathlib.Path("python/compress-image/test/1kb/1kb.png").read_bytes()})
        self.assertIsNone(got[0])
        self.assertEqual(got[1], want)


if __name__ == '__main__':
    unittest.main()