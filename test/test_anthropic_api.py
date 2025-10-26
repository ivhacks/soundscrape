from unittest import TestCase

import anthropic
from anthropic.types import TextBlock
import yaml


with open("secrets.yaml", "r") as f:
    config = yaml.safe_load(f)
    anthropic_api_key = config["anthropic_api_key"]


class AnthropicApiTests(TestCase):
    def test_basic(self):
        client = anthropic.Anthropic(api_key=anthropic_api_key)

        message = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": "do you love knock2? answer with only one word",
                }
            ],
        )
        self.assertEqual(type(message.content[0]), TextBlock)

    def test_image_comprehension(self):
        client = anthropic.Anthropic(api_key=anthropic_api_key)

        with open("test/cat.jpg", "rb") as f:
            file_upload = client.beta.files.upload(file=("cat.jpg", f, "image/jpeg"))

        message = client.beta.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            betas=["files-api-2025-04-14"],
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {"type": "file", "file_id": file_upload.id},
                        },
                        {
                            "type": "text",
                            "text": "Describe this image in one short sentance.",
                        },
                    ],
                }
            ],
        )

        print(message.content)
        self.assertTrue("cat" in message.content[0].text.lower())
