import unittest
import base64
import pathlib
import secret
import main
import tinify
# from main import tinypng_impl


class TestMain(unittest.TestCase):
    # def test_tinypng_small(self):
    #     # Output validation 1KB
    #     want = base64.b64decode( pathlib.Path(secret.RESULT_1KB_TINYPNG).read_text() )
    #     got = main.tinypng_impl({"api_key": secret.API_KEY_TINYPNG, "decoded_image": pathlib.Path(secret.IMAGE_1KB).read_bytes()})
    #     self.assertIsNone(got[0])
    #     self.assertEqual(got[1], want)

    # def test_tinypng_large(self):
    #     # Output validation 1KB
    #     want = base64.b64decode( pathlib.Path(secret.RESULT_3MB_TINYPNG).read_text() )
    #     got = main.tinypng_impl({"api_key": secret.API_KEY_TINYPNG, "decoded_image": pathlib.Path(secret.IMAGE_3MB).read_bytes()})
    #     self.assertIsNone(got[0])
    #     self.assertEqual(got[1], want)

    def test_tinypng_credential(self):
        # Empty Credentials
        # got = main.tinypng_impl({"api_key": "", "decoded_image": pathlib.Path(secret.IMAGE_1KB).read_bytes()})
        # self.assertIsNotNone(got[0])
        # self.assertEqual(got[0], "Account Error: Provide an API key with tinify.key = ...")
        self.assertRaises(tinify.errors.AccountError, main.tinypng_impl, {"api_key": "", "decoded_image": pathlib.Path(secret.IMAGE_1KB).read_bytes()} )

        # # Incorrect Credentials
        # got = main.tinypng_impl({"api_key": "1NCORRECT4CREDENT1ALS", "decoded_image": pathlib.Path(secret.IMAGE_1KB).read_bytes()})
        # self.assertIsNotNone(got[0])
        # self.assertEqual(got[0], "Account Error: Credentials are invalid. (HTTP 401/Unauthorized)")

    def test_tinypng_corrupted_image(self):
        self.assertRaises(tinify.errors.ClientError, main.tinypng_impl, {"api_key": secret.API_KEY_TINYPNG, "decoded_image": b''} )
    #     # File is Empty
    #     got = main.tinypng_impl({"api_key": secret.API_KEY_TINYPNG, "decoded_image": b""})
    #     self.assertIsNotNone(got[0])
    #     self.assertEqual(got[0], "Client Error (File Empty or Corrupted): Input file is empty. (HTTP 400/InputMissing)")

    #     # Corrupted Image
    #     got = main.tinypng_impl({"api_key": secret.API_KEY_TINYPNG, "decoded_image": b"3YdB+NS6OqRWrdtHO+ZV9CFJOj/8pXSshPnDCpF"})
    #     self.assertIsNotNone(got[0])
    #     self.assertEqual(got[0], "Client Error (File Empty or Corrupted): File type is not supported. (HTTP 415/Unsupported media type)")
        self.assertRaises(tinify.errors.ClientError, main.tinypng_impl, {"api_key": secret.API_KEY_TINYPNG, "decoded_image": b'1233'} )

    # def test_tinypng_error(self):
    #     # Accessing wrong key
    #     # self.assertRaises(KeyError, main.tinypng_impl, {"a": secret.API_KEY_TINYPNG, "decoded_image": pathlib.Path(secret.IMAGE_1KB).read_bytes()})
    #     got = main.tinypng_impl({"api_key": secret.API_KEY_TINYPNG, "code": pathlib.Path(secret.IMAGE_1KB).read_bytes()})

if __name__ == '__main__':
    unittest.main()