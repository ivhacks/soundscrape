from io import BytesIO

from PIL import Image
import requests


class TempHostError(Exception):
    pass


def scale_down_image(image_bytes: bytes) -> bytes:
    img = Image.open(BytesIO(image_bytes))
    if img.mode in ("RGBA", "LA", "P"):
        img = img.convert("RGB")
    img = img.resize((300, 300), Image.Resampling.LANCZOS)
    output = BytesIO()
    img.save(output, format="JPEG", quality=85)
    return output.getvalue()


def upload_litterbox(image_bytes: bytes) -> str:
    response = requests.post(
        "https://litterbox.catbox.moe/resources/internals/api.php",
        files={"fileToUpload": ("image.jpg", BytesIO(image_bytes), "image/jpeg")},
        data={"reqtype": "fileupload", "time": "1h"},
        timeout=30,
    )
    if response.status_code != 200:
        raise Exception(
            f"Failed to upload image: {response.status_code} - {response.text}"
        )
    url = response.text.strip()
    if not url.startswith("http"):
        raise Exception(f"Failed to upload image: {url}")
    return url


def upload_uguu(image_bytes: bytes) -> str:
    response = requests.post(
        "https://uguu.se/upload",
        files={"files[]": ("image.jpg", BytesIO(image_bytes), "image/jpeg")},
        timeout=30,
    )
    if response.status_code != 200:
        raise Exception(
            f"Failed to upload image: {response.status_code} - {response.text}"
        )
    data = response.json()
    if not data.get("success"):
        raise Exception(f"Failed to upload image: {data}")
    url = data["files"][0]["url"]
    if not url.startswith("http"):
        raise Exception(f"Failed to upload image: {url}")
    return url


UPLOADERS = [
    upload_litterbox,
    upload_uguu,
]


def upload_temp_image(image_path: str, uploaders=None) -> str:
    if uploaders is None:
        uploaders = UPLOADERS

    with open(image_path, "rb") as f:
        image_bytes = f.read()
    scaled_bytes = scale_down_image(image_bytes)

    errors = []
    for upload in uploaders:
        try:
            return upload(scaled_bytes)
        except Exception as e:
            errors.append(f"{upload.__name__}: {e}")

    raise TempHostError("all temp hosts failed: " + "; ".join(errors))
