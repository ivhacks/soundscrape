import base64
from unittest import TestCase

from openai import OpenAI
import pytest
import yaml


with open("secrets.yaml", "r") as f:
    config = yaml.safe_load(f)
    xai_api_key = config["xai_api_key"]


@pytest.mark.xdist_group(name="grok_api")
class GrokApiTests(TestCase):
    def test_basic(self):
        client = OpenAI(api_key=xai_api_key, base_url="https://api.x.ai/v1")

        response = client.responses.create(
            model="grok-4.5",
            input="do you love knock2? answer with only one word",
        )
        self.assertTrue(len(response.output_text) > 0)

    def test_image_comprehension(self):
        client = OpenAI(api_key=xai_api_key, base_url="https://api.x.ai/v1")

        with open("test/cat.jpg", "rb") as f:
            image_b64 = base64.b64encode(f.read()).decode("utf-8")

        response = client.responses.create(
            model="grok-4.5",
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_image",
                            "image_url": f"data:image/jpeg;base64,{image_b64}",
                        },
                        {
                            "type": "input_text",
                            "text": "Describe this image in one short sentance.",
                        },
                    ],
                }
            ],
        )

        print(response.output_text)
        self.assertTrue("cat" in response.output_text.lower())
