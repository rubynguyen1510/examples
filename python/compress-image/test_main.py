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


        # Result data for 0b
        self.result_data_empty = b""
        
        # Decoded original image file 1kb
        image_file_1kb = open("python/compress-image/test/1kb/1kb.png", "rb")
        self.decoded_image_1kb = image_file_1kb.read()

        # Result data for 1kb tinypng
        encoded_result_1kb_tinypng = open("python/compress-image/test/1kb/1kb_result_encoded_tinypng.txt", "r")
        self.result_data_1kb_tinypng = base64.b64decode(encoded_result_1kb_tinypng.read())

        # Result data for 1kb krakenio
        encoded_result_1kb_krakenio = open("python/compress-image/test/1kb/1kb_result_encoded_krakenio.txt", "r")
        self.result_data_1kb_krakenio = base64.b64decode(encoded_result_1kb_krakenio.read())
        
        # Decoded original image file 3mb
        image_file_3mb = open("python/compress-image/test/3mb/3mb.jpg", "rb")
        self.decoded_image_3mb = image_file_3mb.read()

        # Result data for 3mb tinypng
        encoded_result_3mb_tinypng = open("python/compress-image/test/3mb/3mb_result_encoded_tinypng.txt", "r")
        self.result_data_3mb_tinypng = base64.b64decode(encoded_result_3mb_tinypng.read())

        # Result data for 3mb krakenio
        encoded_result_3mb_krakenio = open("python/compress-image/test/3mb/3mb_result_encoded_krakenio.txt", "r")
        self.result_data_3mb_krakenio = base64.b64decode(encoded_result_3mb_krakenio.read())

        self.variables_tinypng = [{
                #1 kb image
                "api_key": self.api_key_tinypng,
                "decoded_image": self.decoded_image_1kb,
            },

            {   
                #3kb image
                "api_key": self.api_key_tinypng,
                "decoded_image": self.decoded_image_3mb,
            },

            { #Wrong api key
                "api_key": "R4nM3B54NbHNcHblC0XXl0LZyVBgZ",
                "decoded_image": self.decoded_image_1kb,
            },

            { #If a person submits empty image
                "api_key": self.api_key_tinypng,
                "decoded_image": b"",
            }
        ]

        self.variables_krakenio = [{
            #1kb image
            "api_key": self.api_key_krakenio,
            "api_secret_key": self.secret_api_key_krakenio,
            "decoded_image": self.decoded_image_1kb
            },
            
            {
            "api_key": self.api_key_krakenio,
            "api_secret_key": self.secret_api_key_krakenio,
            "decoded_image": self.decoded_image_3mb
            },

            {
            "api_key": self.api_key_krakenio,
            "api_secret_key": self.secret_api_key_krakenio,
            "decoded_image": self.decoded_image_3mb
            },
                                   
            {
            "api_key": self.api_key_krakenio,
            "api_secret_key": self.secret_api_key_krakenio,
            "decoded_image": self.decoded_image_3mb
            },
                                   
        ]
        return None

    def test_tinypng(self):
        # Output validation 1KB
        result = main.tinypng_impl(self.variables_tinypng[0])
        self.assertTrue(result["success"])
        self.assertEqual(result["optimized_image"], self.result_data_1kb_tinypng)

        # Output validation 3MB
        result = main.tinypng_impl(self.variables_tinypng[1])
        self.assertTrue(result["success"])
        self.assertEqual(result["optimized_image"], self.result_data_3mb_tinypng)

        # If user inputs wrong credentials
        result = main.tinypng_impl(self.variables_tinypng[2])
        print(result)
        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Invalid_API_KEY")

    def test_krakenio(self):
        # Output validation 1KB
        result = main.krakenio_impl(self.variables_krakenio[1])

if __name__ == '__main__':
    unittest.main()