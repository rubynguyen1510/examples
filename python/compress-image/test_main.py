import unittest
import base64
import main
# from main import tinypng_impl


class TestMain(unittest.TestCase):
    def setUp(self):
        # self.api_key = "YOUR_API_KEY"
        # self.encoded_image = b"YOUR_ENCODED_IMAGE"
        # self.result_data = b"YOUR_RESULT_DATA"

        # Gathering variables for 1kb image
        self.api_key_tinypng = "R4nM3B54NbHNcHblC0XXl0LZyV82PBgZ"
        self.api_key_krakenio = "f66cec6f44df73d3ba48d8dbce302738"
        self.secret_api_key_krakenio = "7bbd29dd53c00a068b7ebe20b074540a0d7cea9d"

        image_file_1kb = open("python/compress-image/test/1kb/1kb.png", "rb")
        self.decoded_image_1kb = image_file_1kb.read()

        encoded_result_1kb = open("python/compress-image/test/1kb/1kb_result_encoded", "r")
        self.result_data_1kb = base64.b64decode(encoded_result_1kb.read())

        # Gathering variables for 3MB image
        image_file_3mb = open("python/compress-image/test/3mb/3mb.jpg", "rb")
        self.decoded_image_3mb = image_file_3mb.read()

        encoded_result_3mb = open("python/compress-image/test/3mb/3mb_result_encoded", "r")
        self.result_data_3mb = base64.b64decode(encoded_result_3mb.read())

        self.variables_tinypng = [{
            "api_key": self.api_key_tinypng,
            "decoded_image": self.decoded_image_1kb
            },

            {
            "api_key": self.api_key_tinypng,
            "decoded_image": self.decoded_image_3mb
            }
        ]

        self.variables_krakenio = [{
            "api_key": self.api_key_krakenio,
            "secret_api_key": self.secret_api_key_krakenio,
            "decoded_image": self.decoded_image_1kb
            },
            
            {
            "api_key": self.api_key_krakenio,
            "secret_api_key": self.secret_api_key_krakenio,
            "decoded_image": self.decoded_image_3mb
            }
        ]

    def test_tinypng_1kb(self):
        # Output Validation 1KB
        for image in self.variables_tinypng:
            print(image)

if __name__ == '__main__':
    unittest.main()