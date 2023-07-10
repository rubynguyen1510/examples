import unittest
import base64
import main
# from main import tinypng_impl


class TestMain(unittest.TestCase):
    def set_up(self):
        # self.api_key = "YOUR_API_KEY"
        # self.encoded_image = b"YOUR_ENCODED_IMAGE"
        # self.result_data = b"YOUR_RESULT_DATA"

        # Gathering variables for 1kb image
        self.api_key = "R4nM3B54NbHNcHblC0XXl0LZyV82PBgZ"

        image_file_1kb = open("python/compress-image/test/1kb/1kb.png", "rb")
        self.decoded_image_1kb = image_file_1kb.read()

        encoded_result_1kb = open("python/compress-image/test/1kb/1kb_result_encoded", "r")
        self.result_data_1kb = base64.b64decode(encoded_result_1kb.read())

        self.variables_1kb = {
            "api_key": self.api_key,
            "decoded_image": self.decoded_image_1kb
        }
        # Gathering variables for 3MB image
        image_file_3mb = open("python/compress-image/test/3mb/3mb.jpg", "rb")
        self.decoded_image_3mb = image_file_3mb.read()

        encoded_result_3mb = open("python/compress-image/test/3mb/3mb_result_encoded", "r")
        self.result_data_3mb = base64.b64decode(encoded_result_3mb.read())

        self.variables_1kb = {
            "api_key": self.api_key,
            "decoded_image": self.decoded_image_1kb
        }


    def test_tinypng_1kb(self):
        # Output Validation 1KB
        result = main.tinypng_impl(self.variables_1kb)
        self.assertTrue(result["success"])
        self.assertEqual(result["optimized_image"], self.result_data_1kb)

        result = main.tinypng_impl(self.variables_1kb)
        self.assertTrue(result["success"])
        self.assertEqual(result["optimized_image"], self.result_data_1kb)
if __name__ == '__main__':
    unittest.main()