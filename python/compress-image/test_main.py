import unittest
import base64
import pathlib
import secret
import main
import tinify

from unittest import mock
# from main import tinypng_impl

class TestMain(unittest.TestCase):
    # def test_tinypng_small(self):
    #     # Output validation 1KB
    #     want = base64.b64decode( pathlib.Path(secret.RESULT_1KB_TINYPNG).read_text() )
    #     got = main.tinypng_impl({"api_key": secret.API_KEY_TINYPNG, "decoded_image": pathlib.Path(secret.IMAGE_1KB).read_bytes()})
    #     self.assertEqual(got, want)

    # def test_tinypng_large(self):
    #     # Output validation 1KB
    #     want = base64.b64decode( pathlib.Path(secret.RESULT_3MB_TINYPNG).read_text() )
    #     got = main.tinypng_impl({"api_key": secret.API_KEY_TINYPNG, "decoded_image": pathlib.Path(secret.IMAGE_3MB).read_bytes()})
    #     self.assertEqual(got, want)

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

    @mock.patch('main.tinify.from_buffer')
    def test_tinypng_return_type(self, mock_from_buffer):
        mock_from_buffer.return_value.to_buffer.return_value = b''
        got = main.tinypng_impl({"api_key": secret.API_KEY_TINYPNG, "decoded_image": b''})
        self.assertIsInstance(got, bytes)

        mock_from_buffer.return_value.to_buffer.return_value = base64.b64decode( pathlib.Path(secret.RESULT_3MB_TINYPNG).read_text() )
        optimized_image = main.tinypng_impl({"api_key": secret.API_KEY_TINYPNG, "decoded_image": pathlib.Path(secret.IMAGE_3MB).read_bytes()})
        self.assertIsInstance(optimized_image, bytes)

    def test_tinypng_impl_basic_functionality(self):
        with mock.patch("tinify.from_buffer") as mock_from_buffer:
            # Set up the mock return value
            mock_from_buffer.return_value.to_buffer.return_value = pathlib.Path(secret.RESULT_1KB_TINYPNG).read_text()
            # Assert the expected result
            self.assertEqual(main.tinypng_impl({"api_key": secret.API_KEY_TINYPNG, "decoded_image": pathlib.Path(secret.IMAGE_1KB).read_bytes()}), pathlib.Path(secret.RESULT_1KB_TINYPNG).read_text())
            # Assert that the mocked methods were called
            mock_from_buffer.assert_called_once_with(pathlib.Path(secret.IMAGE_1KB).read_bytes())
            mock_from_buffer.return_value.to_buffer.assert_called_once()
        
    # def test_krakenio_small(self):
    #     want = base64.b64decode( pathlib.Path(secret.RESULT_1KB_KRAKENIO).read_text() )
    #     got = main.krakenio_impl({"api_key": secret.API_KEY_KRAKENIO, "api_secret_key": secret.SECRET_API_KEY_KRAKENIO, "decoded_image": pathlib.Path(secret.IMAGE_1KB).read_bytes()})
    #     self.assertEqual(got, want)

if __name__ == '__main__':
    unittest.main()