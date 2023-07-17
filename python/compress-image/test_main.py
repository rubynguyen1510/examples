# Standard librar
import base64
import pathlib
import unittest
from unittest.mock import patch

# Third party
import requests
import tinify
from parameterized import parameterized

# Local imports
import main
import secret

IMAGE_1KB = pathlib.Path(secret.IMAGE_1KB).read_bytes()
RESULT_1KB = (pathlib.Path(secret.RESULT_1KB_TINYPNG).
              read_text(encoding="utf-8"))


class TestTinypng(unittest.TestCase):
    """Class for testing the functionality of the 'tinypng_impl' function."""
    @unittest.skipUnless(secret.API_KEY_TINYPNG, "No Tinypng API Key set")
    def test_tinypng_small(self):
        """Test case optimizing 1kb image using 'tinypng_impl' function."""
        want = RESULT_1KB
        got = main.tinypng_impl({
            "api_key": secret.API_KEY_TINYPNG,
            "decoded_image": IMAGE_1KB,
        })
        self.assertEqual(base64.b64encode(got).decode(), want)

    def test_tinypng_credential(self):
        """Test case handling Account errors in the 'tinypng_impl' function."""
        # Incorrect Credentials
        self.assertRaises(tinify.errors.AccountError, main.tinypng_impl,
                          {"api_key": "1NCORRECT4CREDENT1ALS",
                           "decoded_image": IMAGE_1KB})

    @unittest.skipIf(not secret.API_KEY_TINYPNG, "No Tinypng API Key set")
    @parameterized([
        (b"",),
        (b"ORw0KGgoAAAANSUhEUgAAABEAAAAOCAMAAAD+M",),
    ])
    def test_tinypng_client(self, image):
        """Test case for Client errors in the 'tinypng_impl' function."""
        # Image is Empty
        data = {
            "api_key": secret.API_KEY_TINYPNG,
            "decoded_image": image,
        }

        with self.assertRaises(tinify.errors.ClientError):
            main.tinypng_impl(data)

    @unittest.skipIf(not secret.API_KEY_TINYPNG, "No Tinypng API Key set")
    def test_tinypng_keys(self):
        """Test case for handling Key errors in the 'tinypng_impl' function"""
        # Accessing wrong key
        self.assertRaises(KeyError, main.tinypng_impl,
                          {"a": secret.API_KEY_TINYPNG,
                           "decoded_image": IMAGE_1KB})
        self.assertRaises(KeyError, main.tinypng_impl,
                          {"api_key": secret.API_KEY_TINYPNG,
                           "code_image": IMAGE_1KB})
        # Empty Key
        self.assertRaises(KeyError, main.tinypng_impl,
                          {"": secret.API_KEY_TINYPNG,
                           "code_image": IMAGE_1KB})
        self.assertRaises(KeyError, main.tinypng_impl,
                          {"api_key": secret.API_KEY_TINYPNG,
                           "": IMAGE_1KB})

    @unittest.skipIf(not secret.API_KEY_TINYPNG, "No Tinypng API Key set")
    def test_tinypng_variables(self):
        """Test case handling variable errors in the 'tinypng_impl' function"""
        # Empty variables
        self.assertRaises(KeyError, main.tinypng_impl, {})
        # One key in variable
        self.assertRaises(KeyError, main.tinypng_impl,
                          {"api_key": secret.API_KEY_TINYPNG})

    @unittest.skipUnless(secret.API_KEY_TINYPNG, "No Tinypng API Key set")
    def test_tinypng_impl_basic_functionality_1kb(self):
        """basic functionality of 'tinypng_impl' with a 1kb image"""
        with patch("main.tinify.from_buffer") as mock_from_buffer:
            # Set up the mock return value as decoded result
            mock_from_buffer.return_value.to_buffer.return_value = (
                base64.b64decode(RESULT_1KB))
            # Assert the expected result
            optimized_image = main.tinypng_impl({
                "api_key": secret.API_KEY_TINYPNG,
                "decoded_image": IMAGE_1KB,
            })
            # Check if the return type is a string
            self.assertIsInstance(optimized_image, bytes)
            # Check if the assert equals and is correct
            self.assertEqual(
                optimized_image,
                mock_from_buffer.return_value.to_buffer.return_value)

    @unittest.skipIf(not secret.API_KEY_TINYPNG, "No Tinypng API Key set")
    def test_tinypng_impl_unexpected_exception_account_error(self):
        """Test case handling unexpected 'AccountError' in 'tinypng_impl'"""
        with patch.object(tinify, "from_buffer") as mock_from_buffer:
            # Set up the mock return value as account exception
            mock_from_buffer.side_effect = tinify.errors.AccountError(
                "API Key is wrong"
            )
            # Check the raise for Account error
            self.assertRaises(tinify.errors.AccountError,
                              main.tinypng_impl,
                              {"api_key": secret.API_KEY_TINYPNG,
                               "decoded_image": IMAGE_1KB})
            mock_from_buffer.assert_called_once()

    @unittest.skipIf(not secret.API_KEY_TINYPNG, "No Tinypng API Key set")
    def test_tinypng_impl_unexpected_exception_client_error(self):
        """Test case handling unexpected 'ClientError' in 'tinypng_impl'."""
        with patch("main.tinify.from_buffer") as mock_from_buffer:
            # Set up the mock return value as client exception
            mock_from_buffer.side_effect = \
                tinify.errors.ClientError("Image is incorrect")
            # Check the raise for client error
            self.assertRaises(tinify.errors.ClientError,
                              main.tinypng_impl,
                              {"api_key": secret.API_KEY_TINYPNG,
                               "decoded_image": IMAGE_1KB})
            mock_from_buffer.assert_called_once()


class TestKrakenIO(unittest.TestCase):
    @unittest.skipIf(not (secret.API_KEY_KRAKENIO
                          and secret.SECRET_API_KEY_KRAKENIO),
                     "No KrakenIO API Key or Secret Key")
    def test_krakenio(self):
        """Output validation 1KB"""
        want = (pathlib.Path(
            secret.RESULT_1KB_KRAKENIO).read_text(encoding="utf-8"))
        got = main.krakenio_impl({
            "api_key": secret.API_KEY_KRAKENIO,
            "api_secret_key": secret.SECRET_API_KEY_KRAKENIO,
            "decoded_image": IMAGE_1KB
        })
        self.assertEqual(got, base64.b64decode(want))

    @unittest.skipIf(not (secret.API_KEY_KRAKENIO
                          and secret.SECRET_API_KEY_KRAKENIO),
                     "No KrakenIO API Key or Secret Key")
    def test_krakenio_time_out(self):
        with patch("main.requests.post") as mock_post:
            mock_post.side_effect = requests.exceptions.ReadTimeout
            with self.assertRaises(requests.exceptions.ReadTimeout):
                main.krakenio_impl({
                    "api_key": secret.API_KEY_KRAKENIO,
                    "api_secret_key": secret.SECRET_API_KEY_KRAKENIO,
                    "decoded_image": IMAGE_1KB
                })
            mock_post.assert_called_once()


class TestValidateRequest(unittest.TestCase):
    @parameterized.expand([
        [
            {
                "payload": {
                    "provider": "tinypng",
                    "image": str(base64.b64encode(pathlib.Path(
                        secret.IMAGE_1KB).read_bytes()), "utf-8")
                },
                "variables": {"API_KEY": secret.API_KEY_TINYPNG},
            },
            {
                "provider": "tinypng",
                "api_key": secret.API_KEY_TINYPNG,
                "decoded_image": IMAGE_1KB
            }
        ],
        [
            {
                "payload": {
                    "provider": "krakenio",
                    "image": str(base64.b64encode(pathlib.Path(
                        secret.IMAGE_1KB).read_bytes()), "utf-8")
                },
                "variables": {
                    "API_KEY": secret.API_KEY_KRAKENIO,
                    "SECRET_API_KEY": secret.SECRET_API_KEY_KRAKENIO
                }
            },
            {
                "provider": "krakenio",
                "api_key": secret.API_KEY_KRAKENIO,
                "api_secret_key": secret.SECRET_API_KEY_KRAKENIO,
                "decoded_image": IMAGE_1KB
            }
        ]
    ])
    @unittest.skipIf(not (secret.API_KEY_KRAKENIO
                          and secret.SECRET_API_KEY_KRAKENIO
                          and secret.API_KEY_TINYPNG),
                     "No Tinypng Key and KrakenIO Key")
    def test_validate_request(self, got, expected):
        req = MyRequest({
            "payload": got["payload"],
            "variables": got["variables"]
            })
        self.assertEqual(main.validate_request(req), expected)

    @parameterized.expand([
        [
            {
                "payload": {},
                "variables": {},
            },
            ("Missing payload")
        ],
        [
            {
                "payload": {"provider": "IMNOTAPROVIDER", "image": ""},
                "variables": {"API_KEY": "1234567"},
            },
            ("Invalid provider.")
        ],
        [
            {
                "payload": {"provider": "krakenio", "image": ""},
                "variables": {},
            },
            ("Missing variables.")
        ],
        [
            {
                # Missing api key tiny
                "payload": {"provider": "tinypng", "image": "12345"},
                "variables": {"API_KEY": ""},
            },
            ("Missing API key.")
        ],
        [
            {
                # Missing api key
                "payload": {"provider": "krakenio", "image": "12345"},
                "variables": {"API_KEY": "", "SECRET_API_KEY": ""},
            },
            ("Missing API key.")
        ],
        [
            {
                # Missing secret api key
                "payload": {"provider": "krakenio", "image": "12345"},
                "variables": {"API_KEY": "123", "SECRET_API_KEY": ""},
            },
            ("Missing api secret key.")
        ]
    ])
    def test_validate_request_ValueError(self, got, want):
        req = MyRequest({
            "payload": got["payload"],
            "variables": got["variables"]
        })
        with self.assertRaises(ValueError) as context:
            main.validate_request(req)
            self.assertEqual(str(context.exception), want)

    @parameterized.expand([
        [
            {
                # accessing wrong provider
                "payload": {"WRONG_PROVIDER": "krakenio", "image": "12345"},
                "variables": {"API_KEY": "123", "SECRET_API_KEY": ""},
            }
        ],
        [
            {
                # accessing wrong image
                "payload": {"provider": "krakenio", "1Mage": "12345"},
                "variables": {"API_KEY": "123", "SECRET_API_KEY": ""},
            }
        ],
        [
            {
                # accessing wrong api key
                "payload": {"provider": "krakenio", "1Mage": "12345"},
                "variables": {"NOT AN API": "123", "SECRET_API_KEY": ""},
            }
        ],
        [
            {
                # accessing wrong api keys and secret keys
                "payload": {"provider": "krakenio", "1Mage": "12345"},
                "variables": {"API": "123", "SecretKey": ""},
            }
        ]

    ])
    def test_validate_request_KeyError(self, got):
        req = MyRequest({
            "payload": got["payload"],
            "variables": got["variables"]
            })
        self.assertRaises(ValueError, main.validate_request, req)


class TestMain(unittest.TestCase):
    @unittest.skipIf(not secret.API_KEY_TINYPNG, "No Tinypng API Key set")
    def test_main_success(self):
        # Output validation 1KB
        want = {
            "success": True,
            "image":
            pathlib.Path(secret.RESULT_1KB_TINYPNG).read_text(encoding="utf-8")
        }

        req = MyRequest({
            "payload": {
                "provider": "tinypng",
                "image": base64.b64encode(IMAGE_1KB).decode()
            },
            "variables": {
                "API_KEY": secret.API_KEY_TINYPNG
            }
        })

        res = MyResponse()  # Create a response object
        main.main(req, res)

        # Check the response
        got = res.json()
        self.maxDiff = None
        self.assertEqual(got, want)

    def test_main_value_error(self):
        want = {"success": False, "Value Error": "Missing payload"}
        req = MyRequest({"payload": {}, "variables": {}})
        res = MyResponse()  # Create a response object
        main.main(req, res)

        # Check the response
        got = res.json()
        self.maxDiff = None
        self.assertEqual(got, want)

    def test_main_exception(self):
        req = MyRequest({
            "payload": {
                "provider": "tinypng",
                "image": base64.b64encode(IMAGE_1KB).decode()
            },
            "variables": {
                "API_KEY": "wrong_api_key"
            }
        })
        res = MyResponse()  # Create a response object
        main.main(req, res)

        # Check the response
        got = res.json()
        self.maxDiff = None
        self.assertFalse(got["success"])
        self.assertIn("AccountError", got["error"])


# Define a mock request class
class MyRequest:
    def __init__(self, data):
        self.payload = data.get("payload", {})
        self.variables = data.get("variables", {})


# Define a mock response class
class MyResponse:
    def __init__(self):
        self._json = None

    def json(self, data=None):
        if data is not None:
            self._json = data
        return self._json


if __name__ == "__main__":
    unittest.main()
