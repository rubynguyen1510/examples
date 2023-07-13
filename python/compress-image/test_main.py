import unittest
import base64
import pathlib
from unittest.mock import patch
import secret
import tinify
import requests
import requests.exceptions
import main


class TestTinypng(unittest.TestCase):
    def test_tinypng_small(self):
        want = (pathlib.Path(secret.RESULT_1KB_TINYPNG).
                read_text(encoding="utf-8"))
        got = main.tinypng_impl({"api_key": secret.API_KEY_TINYPNG,
                                 "decoded_image":
                                 pathlib.Path(secret.IMAGE_1KB).read_bytes()})
        self.assertEqual(got, want)

    def test_tinypng_big(self):
        want = (pathlib.Path(secret.RESULT_3MB_TINYPNG).
                read_text(encoding="utf-8"))
        got = main.tinypng_impl({"api_key": secret.API_KEY_TINYPNG,
                                 "decoded_image":
                                 pathlib.Path(secret.IMAGE_3MB).read_bytes()})
        self.assertEqual(got, want)

    def test_tinypng_credential(self):
        # Empty Credentials
        self.assertRaises(tinify.errors.AccountError, main.tinypng_impl,
                          {"api_key": "",
                           "decoded_image": pathlib.Path(secret.IMAGE_1KB).
                           read_bytes()})
        # # Incorrect Credentials
        self.assertRaises(tinify.errors.AccountError, main.tinypng_impl,
                          {"api_key": "1NCORRECT4CREDENT1ALS",
                           "decoded_image": pathlib.Path(secret.IMAGE_1KB).
                           read_bytes()})

    def test_tinypng_image(self):
        # Image is Empty
        self.assertRaises(tinify.errors.ClientError, main.tinypng_impl,
                          {"api_key": secret.API_KEY_TINYPNG,
                           "decoded_image": b""})
        # Corrupted Image
        self.assertRaises(tinify.errors.ClientError, main.tinypng_impl,
                          {"api_key": secret.API_KEY_TINYPNG,
                           "decoded_image":
                           b"ORw0KGgoAAAANSUhEUgAAABEAAAAOCAMAAAD+M"})

    def test_tinypng_keys(self):
        # Accessing wrong key
        self.assertRaises(KeyError, main.tinypng_impl,
                          {"a": secret.API_KEY_TINYPNG,
                           "decoded_image": pathlib.Path(secret.IMAGE_1KB).
                           read_bytes()})
        self.assertRaises(KeyError, main.tinypng_impl,
                          {"api_key": secret.API_KEY_TINYPNG,
                           "code_image": pathlib.Path(secret.IMAGE_1KB).
                           read_bytes()})

        # Empty Key
        self.assertRaises(KeyError, main.tinypng_impl,
                          {"": secret.API_KEY_TINYPNG,
                           "code_image": pathlib.Path(secret.IMAGE_1KB).
                           read_bytes()})
        self.assertRaises(KeyError, main.tinypng_impl,
                          {"api_key": secret.API_KEY_TINYPNG,
                           "": pathlib.Path(secret.IMAGE_1KB).read_bytes()})

    def test_tinypng_variables(self):
        # Empty variables
        self.assertRaises(KeyError, main.tinypng_impl, {})
        # Missing decoded_image variable
        self.assertRaises(KeyError, main.tinypng_impl,
                          {"api_key": secret.API_KEY_TINYPNG})
        # Missing api_key variable
        self.assertRaises(KeyError, main.tinypng_impl,
                          {"decoded_image": b"123"})

    def test_tinypng_impl_basic_functionality_3MB(self):
        with patch("main.tinify.from_buffer") as mock_from_buffer:
            # Strip the string. In our testcase we have b"Encoded Information"
            # so we would need to clean it.
            stripped_string = (pathlib.Path(
                secret.RESULT_3MB_TINYPNG).read_text(encoding="utf-8"))[2:-1]
            # Set up the mock return value.
            # To mock the return value we would give it the decoded result
            mock_from_buffer.return_value.to_buffer.return_value = (
                base64.b64decode(stripped_string))
            # Assert the expected result
            optimized_image = main.tinypng_impl({
                "api_key": secret.API_KEY_TINYPNG,
                "decoded_image": pathlib.Path(secret.IMAGE_3MB).read_bytes()})
            # Check if the return type is a string
            self.assertIsInstance(optimized_image, str)
            # Check if the assert equals and is correct
            self.assertEqual(optimized_image, str(base64.b64encode(
                mock_from_buffer.return_value.to_buffer.return_value)))

    def test_tinypng_impl_basic_functionality_1kb(self):
        with patch("main.tinify.from_buffer") as mock_from_buffer:
            # Strip the string. In our testcase we have b"Encoded Information"
            # so we would need to clean it.
            stripped_string = (pathlib.Path(
                secret.RESULT_1KB_TINYPNG).read_text(encoding="utf-8"))[2:-1]
            # Set up the mock return value.
            # To mock the return value we would give it the decoded result
            mock_from_buffer.return_value.to_buffer.return_value = (
                base64.b64decode(stripped_string))
            # Assert the expected result
            optimized_image = main.tinypng_impl({
                "api_key": secret.API_KEY_TINYPNG,
                "decoded_image": pathlib.Path(secret.IMAGE_1KB).read_bytes()})
            # Check if the return type is a string
            self.assertIsInstance(optimized_image, str)
            # Check if the assert equals and is correct
            self.assertEqual(optimized_image, str(base64.b64encode(
                mock_from_buffer.return_value.to_buffer.return_value)))

    def test_tinypng_impl_unexpected_exception_accountError(self):
        with patch("main.tinify.from_buffer") as mock_from_buffer:
            mock_from_buffer.side_effect = \
                tinify.errors.AccountError("API Key is wrong")
            self.assertRaises(tinify.errors.AccountError,
                              main.tinypng_impl,
                              {"api_key": secret.API_KEY_TINYPNG,
                               "decoded_image": pathlib.Path(secret.IMAGE_1KB).
                               read_bytes()})
            mock_from_buffer.assert_called_once()

    def test_tinypng_impl_unexpected_exception_clientError(self):
        with patch("main.tinify.from_buffer") as mock_from_buffer:
            mock_from_buffer.side_effect = \
                tinify.errors.ClientError("Image is incorrect")
            self.assertRaises(tinify.errors.ClientError,
                              main.tinypng_impl,
                              {"api_key": secret.API_KEY_TINYPNG,
                               "decoded_image": pathlib.Path(secret.IMAGE_1KB).
                               read_bytes()})
            mock_from_buffer.assert_called_once()


class TestKrakenIO(unittest.TestCase):
    def test_krakenio_small(self):
        # Output validation 1KB
        want = (pathlib.Path(
            secret.RESULT_1KB_KRAKENIO).read_text(encoding="utf-8"))
        got = main.krakenio_impl({"api_key": secret.API_KEY_KRAKENIO,
                                  "api_secret_key":
                                  secret.SECRET_API_KEY_KRAKENIO,
                                  "decoded_image":
                                  pathlib.Path(secret.IMAGE_1KB).
                                  read_bytes()})
        self.assertEqual(got, want)

    def test_krakenio_big(self):
        # Output validation 3MB
        want = (pathlib.Path(
            secret.RESULT_3MB_KRAKENIO).read_text(encoding="utf-8"))
        got = main.krakenio_impl({"api_key": secret.API_KEY_KRAKENIO,
                                  "api_secret_key":
                                  secret.SECRET_API_KEY_KRAKENIO,
                                  "decoded_image":
                                  pathlib.Path(secret.IMAGE_3MB).
                                  read_bytes()})
        self.assertEqual(got, want)

    def test_krakenio_wrong_api_key(self):
        self.assertRaises(requests.exceptions.HTTPError, main.krakenio_impl,
                          {"api_key": secret.API_KEY_KRAKENIO,
                           "api_secret_key": "1234",
                           "decoded_image": pathlib.Path(secret.IMAGE_1KB).
                           read_bytes()})

    def test_krakenio_wrong_api_secret_key(self):
        self.assertRaises(requests.exceptions.HTTPError, main.krakenio_impl,
                          {"api_key": "1234",
                           "api_secret_key": secret.SECRET_API_KEY_KRAKENIO,
                           "decoded_image": pathlib.Path(secret.IMAGE_1KB).
                           read_bytes()})

    def test_krakenio_corrupted_image(self):
        self.assertRaises(requests.exceptions.HTTPError, main.krakenio_impl,
                          {"api_key": secret.API_KEY_KRAKENIO,
                           "api_secret_key": secret.SECRET_API_KEY_KRAKENIO,
                           "decoded_image": "123"})

    def test_krakenio_time_out(self):
        with patch("main.requests.post") as mock_post:
            mock_post.side_effect = requests.exceptions.ReadTimeout
            with self.assertRaises(requests.exceptions.ReadTimeout):
                main.krakenio_impl({
                    "api_key": secret.API_KEY_KRAKENIO,
                    "api_secret_key": secret.SECRET_API_KEY_KRAKENIO,
                    "decoded_image":
                    pathlib.Path(secret.IMAGE_1KB).read_bytes()
                })
            mock_post.assert_called_once()

    def test_krakenio_connection_error(self):
        with patch("main.requests.post") as mock_post:
            mock_post.side_effect = requests.exceptions.ConnectionError
            with self.assertRaises(requests.exceptions.ConnectionError):
                main.krakenio_impl({
                    "api_key": secret.API_KEY_KRAKENIO,
                    "api_secret_key": secret.SECRET_API_KEY_KRAKENIO,
                    "decoded_image":
                    pathlib.Path(secret.IMAGE_1KB).read_bytes()
                })
            mock_post.assert_called_once()


class TestValidatePayload(unittest.TestCase):
    def test_validate_request(self):
        test_cases = [
            {
                "payload": {
                    "provider": "tinypng",
                    "image": str(base64.b64encode(pathlib.Path(
                                secret.IMAGE_1KB).read_bytes()), "utf-8")},
                "variables": {"API_KEY": secret.API_KEY_TINYPNG},
                "expected_result": {
                    "provider": "tinypng",
                    "api_key": secret.API_KEY_TINYPNG,
                    "decoded_image":
                    pathlib.Path(secret.IMAGE_1KB).read_bytes()}
            },
            {
                "payload": {
                    "provider": "krakenio",
                    "image": str(base64.b64encode(pathlib.Path(
                        secret.IMAGE_1KB).read_bytes()), "utf-8")},
                "variables": {
                    "API_KEY": secret.API_KEY_KRAKENIO,
                    "SECRET_API_KEY": secret.SECRET_API_KEY_KRAKENIO},
                "expected_result": {
                    "provider": "krakenio",
                    "api_key": secret.API_KEY_KRAKENIO,
                    "api_secret_key": secret.SECRET_API_KEY_KRAKENIO,
                    "decoded_image":
                    pathlib.Path(secret.IMAGE_1KB).read_bytes()}
            }
        ]

        for test_case in test_cases:
            req = MockRequest({
                "payload": test_case["payload"],
                "variables": test_case["variables"]
                })
            got = main.validate_request(req)
            self.assertEqual(got, test_case["expected_result"])

    def test_validate_request_ValueError(self):
        test_cases = [
            # Empty payload
            {
                "payload": {},
                "variables": {},
                "expected_error": "Missing payload"
            },
            # Invalid Provider and Image is Empty
            {
                "payload": {"provider": "IMNOTAPROVIDER", "image": ""},
                "variables": {"API_KEY": "1234567"},
                "expected_error": "Invalid provider."
            },
            # Missing variables
            {
                "payload": {"provider": "krakenio", "image": ""},
                "variables": {},
                "expected_error": "Missing variables."
            },
            {
                # Missing api key tiny
                "payload": {"provider": "tinypng", "image": "12345"},
                "variables": {"API_KEY": ""},
                "expected_error": "Missing API key."
            },
            {
                # Missing api key
                "payload": {"provider": "krakenio", "image": "12345"},
                "variables": {"API_KEY": "", "SECRET_API_KEY": ""},
                "expected_error": "Missing API key."
            },
            {
                # Missing secret api key
                "payload": {"provider": "krakenio", "image": "12345"},
                "variables": {"API_KEY": "123", "SECRET_API_KEY": ""},
                "expected_error": "Missing api secret key."
            },
        ]

        for test_case in test_cases:
            req = MockRequest({
                "payload": test_case["payload"],
                "variables": test_case["variables"]
                })
            with self.assertRaises(ValueError) as context:
                main.validate_request(req)
                self.assertEqual(str(context.exception),
                                 test_case["expected_error"])

    def test_validate_request_KeyError(self):
        test_cases = [
            {
                # accessing wrong provider
                "payload": {"WRONG_PROVIDER": "krakenio", "image": "12345"},
                "variables": {"API_KEY": "123", "SECRET_API_KEY": ""},
            },
            {
                # accessing wrong image
                "payload": {"provider": "krakenio", "1Mage": "12345"},
                "variables": {"API_KEY": "123", "SECRET_API_KEY": ""},
            },
            {
                # accessing wrong api key
                "payload": {"provider": "krakenio", "1Mage": "12345"},
                "variables": {"NOT AN API": "123", "SECRET_API_KEY": ""},
            },
            {
                # accessing wrong api keys and secret keys
                "payload": {"provider": "krakenio", "1Mage": "12345"},
                "variables": {"API": "123", "SecretKey": ""},
            },
        ]
        for test_case in test_cases:
            req = MockRequest({
                "payload": test_case["payload"],
                "variables": test_case["variables"]
                })
            self.assertRaises(KeyError, main.validate_request, req)


class TestMain(unittest.TestCase):
    def test_main_tinypng(self):
        # Output validation 1KB
        want = {
            "success:": True,
            "image": pathlib.Path(
                secret.RESULT_1KB_TINYPNG).read_text(encoding="utf-8")
        }

        req = MockRequest({
            "payload": {
                "provider": "tinypng",
                "image": str(base64.b64encode(pathlib.Path(
                        secret.IMAGE_1KB).read_bytes()), "utf-8")
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

    def test_main_krakenio(self):
        # Output validation 1KB
        want = {
            "success:": True,
            "image": pathlib.Path(
                    secret.RESULT_1KB_KRAKENIO).read_text(encoding="utf-8")
        }

        req = MockRequest({
            "payload": {
                "provider": "krakenio",
                "image": str(base64.b64encode(pathlib.Path(
                    secret.IMAGE_1KB).read_bytes()), "utf-8")
            },
            "variables": {
                "API_KEY": secret.API_KEY_KRAKENIO,
                "SECRET_API_KEY": secret.SECRET_API_KEY_KRAKENIO
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

    # def json(self, data=None):
    #     if data is not None:
    #         self._json = data
    #     return self._json


if __name__ == "__main__":
    unittest.main()
