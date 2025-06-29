from io import BytesIO
import math
from tkinter import Button, Event, Label, Tk
from typing import List

from PIL import Image, ImageDraw, ImageTk


THUMBNAIL_SIZE = 200
ZOOM_BOX_HEIGHT = 600


class CoverArtSelector:
    def __init__(self, images_bytes: List[bytes]) -> None:
        # Convert bytes to PIL Images
        self.images_pil = []
        for image_bytes in images_bytes:
            image = Image.open(BytesIO(image_bytes))
            self.images_pil.append(image)

        self.image_index = -1

    def motion(self, event: Event) -> None:
        # Buttons have 5px padding, subtract to get exact coords relative to image
        x, y = event.x - 5, event.y - 5
        widget = event.widget

        try:
            self.image_index = int(widget._name)
        except (AttributeError, ValueError):
            # We're not on an image
            self.image_index = -1
            pass

        if self.image_index != -1:
            # Even if the mouse is on a button, it may still be outside the image.
            # If it's in the small padding area on the edge, we don't consider it to be on an image.
            if x < 0 or y < 0:
                self.image_index = -1

            if x > THUMBNAIL_SIZE or y > THUMBNAIL_SIZE:
                self.image_index = -1

        if self.image_index != -1:
            original_image = self.images_pil_resized[self.image_index]
            original_image_size = original_image.width
            coord_multiplier = original_image_size / THUMBNAIL_SIZE

            mapped_x = x * coord_multiplier
            mapped_y = y * coord_multiplier

            if mapped_x > self.zoom_box_width / 2:
                # Calc x based on right edge
                right = mapped_x + math.ceil(self.zoom_box_width / 2)
                if right > original_image_size:
                    right = original_image_size
                left = right - self.zoom_box_width
            else:
                # Calc x based on left edge
                left = mapped_x - math.floor(self.zoom_box_width / 2)
                if left < 0:
                    left = 0
                right = left + self.zoom_box_width

            if mapped_y > self.zoom_box_width / 2:
                # Calc y based on bottom edge
                bottom = mapped_y + math.ceil(ZOOM_BOX_HEIGHT / 2)
                if bottom > original_image_size:
                    bottom = original_image_size
                top = bottom - ZOOM_BOX_HEIGHT
            else:
                # Calc y based on top edge
                top = mapped_y - math.floor(ZOOM_BOX_HEIGHT / 2)
                if top < 0:
                    top = 0
                bottom = top + ZOOM_BOX_HEIGHT

            box_tuple = (left, top, right, bottom)
            zoom_box_image = original_image.crop(box_tuple)

            zoom_box_image_tk = ImageTk.PhotoImage(zoom_box_image)
            self.zoom_box_label.configure(image=zoom_box_image_tk)

            self.anti_garbage_collection_list[0] = zoom_box_image_tk

    def generate_thumbnail(self, image: Image.Image) -> Image.Image:
        orig_width = image.width
        orig_height = image.height
        res_label_string = str(orig_width) + " x " + str(orig_height)

        resized_image = image.resize((THUMBNAIL_SIZE, THUMBNAIL_SIZE))

        res_label_height = math.floor(THUMBNAIL_SIZE / 20)
        res_label_width = math.floor(THUMBNAIL_SIZE / 30) * len(res_label_string) + 4

        strip = Image.new("RGB", (res_label_width, res_label_height))
        draw = ImageDraw.Draw(strip)

        draw.text((2, 0), res_label_string, (255, 255, 255))
        offset = (0, THUMBNAIL_SIZE - res_label_height)
        resized_image.paste(strip, offset)
        return resized_image

    def show_selection_window(self) -> int:
        num_thumbnails = len(self.images_pil)

        self.root = Tk()
        self.root.title("covert artwork selector")

        self.zoom_box_width = (
            num_thumbnails * THUMBNAIL_SIZE + (num_thumbnails - 1) * 10
        )
        image_pil = Image.new(mode="RGB", size=(self.zoom_box_width, ZOOM_BOX_HEIGHT))
        zoom_box_image_tk = ImageTk.PhotoImage(image_pil)

        # Hack to prevent the zoomed image from getting garbage collected by TCL
        self.anti_garbage_collection_list = []
        self.anti_garbage_collection_list.append(zoom_box_image_tk)

        self.zoom_box_label = Label(self.root, image=zoom_box_image_tk)
        self.zoom_box_label.grid(column=0, row=0, columnspan=num_thumbnails + 1)

        # Create thumbnail buttons
        self.images_tk = []
        for i in range(len(self.images_pil)):
            image_pil = self.generate_thumbnail(self.images_pil[i])
            self.images_tk.append(ImageTk.PhotoImage(image_pil))
            Button(
                self.root,
                name=str(i),
                image=self.images_tk[-1],
                command=self.root.destroy,
            ).grid(column=i, row=1)

        # If any of the original images are smaller than the width of the zoomed area, scale them up
        self.images_pil_resized = []
        for i in range(num_thumbnails):
            width = self.images_pil[i].width
            if width < self.zoom_box_width:
                size_multiplier = math.floor(self.zoom_box_width / width) + 1
            else:
                # Double zoom of even high-res images just so we can get a better look at the details
                size_multiplier = 2

            self.images_pil_resized.append(
                self.images_pil[i].resize(
                    (width * size_multiplier, width * size_multiplier),
                    resample=Image.Resampling.NEAREST,
                )
            )

        self.root.bind("<Motion>", self.motion)
        self.root.mainloop()
        return self.image_index


if __name__ == "__main__":
    # Load test images as bytes
    test_images_bytes = []
    with open("test/images/1.png", "rb") as f:
        test_images_bytes.append(f.read())
    with open("test/images/2.png", "rb") as f:
        test_images_bytes.append(f.read())
    with open("test/images/1.png", "rb") as f:
        test_images_bytes.append(f.read())
    with open("test/images/2.png", "rb") as f:
        test_images_bytes.append(f.read())
    with open("test/images/1.png", "rb") as f:
        test_images_bytes.append(f.read())

    # Create and show the UI
    selector = CoverArtSelector(test_images_bytes)
    selected_index = selector.show_selection_window()

    if selected_index != -1:
        print(f"Selected image index: {selected_index}")
    else:
        print("No image was selected")
