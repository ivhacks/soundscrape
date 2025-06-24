import os

os.environ["TK_SILENCE_DEPRECATION"] = "1"

from PIL import Image, ImageTk
import tkinter as tk
import math


class WorkingCoverArtSelector:
    def __init__(self, images):
        self.images_pil = images
        self.image_index = -1

    def motion(self, event):
        x, y = event.x, event.y
        widget = event.widget

        try:
            image_index = int(widget._name)
        except:
            self.image_index = -1
            return

        if image_index < 0 or image_index >= len(self.images_pil):
            self.image_index = -1
            return

        if x < 0 or y < 0 or x > 200 or y > 200:
            self.image_index = -1
            return

        self.image_index = image_index

        # Map mouse coordinates to the resized image
        original_image = self.images_pil_resized[image_index]
        original_image_size = original_image.width
        coord_multiplier = original_image_size / 200

        mapped_x = x * coord_multiplier
        mapped_y = y * coord_multiplier

        # Calculate crop box for zoom
        left = max(0, mapped_x - self.zoom_box_width // 2)
        right = min(original_image_size, left + self.zoom_box_width)
        if right == original_image_size:
            left = right - self.zoom_box_width

        top = max(0, mapped_y - 150)  # ZOOM_BOX_HEIGHT // 2
        bottom = min(original_image_size, top + 300)
        if bottom == original_image_size:
            top = bottom - 300

        box_tuple = (left, top, right, bottom)
        zoom_box_image = original_image.crop(box_tuple)

        zoom_box_image_tk = ImageTk.PhotoImage(zoom_box_image)
        self.zoom_box_button.configure(image=zoom_box_image_tk)
        self.anti_garbage_collection_list[0] = zoom_box_image_tk

    def generate_thumbnail(self, image):
        orig_width = image.width
        orig_height = image.height
        res_label_string = str(orig_width) + " x " + str(orig_height)

        resized_image = image.resize((200, 200))

        res_label_height = math.floor(200 / 20)
        res_label_width = math.floor(200 / 30) * len(res_label_string) + 4

        from PIL import ImageDraw

        strip = Image.new("RGB", (res_label_width, res_label_height))
        draw = ImageDraw.Draw(strip)
        draw.text((2, 0), res_label_string, (255, 255, 255))

        offset = (0, 200 - res_label_height)
        resized_image.paste(strip, offset)
        return resized_image

    def show_selection_window(self):
        num_thumbnails = len(self.images_pil)

        self.root = tk.Tk()
        self.root.title("Cover Art Selector")

        self.zoom_box_width = num_thumbnails * 200 + (num_thumbnails - 1) * 10

        # Create zoom area as BUTTON (not Label)
        image_pil = Image.new(mode="RGB", size=(self.zoom_box_width, 300))
        zoom_box_image_tk = ImageTk.PhotoImage(image_pil)

        self.anti_garbage_collection_list = []
        self.anti_garbage_collection_list.append(zoom_box_image_tk)

        self.zoom_box_button = tk.Button(self.root, image=zoom_box_image_tk)
        self.zoom_box_button.grid(column=0, row=0, columnspan=num_thumbnails)

        # Create thumbnail buttons
        self.images_tk = []
        for i in range(len(self.images_pil)):
            image_pil = self.generate_thumbnail(self.images_pil[i])
            self.images_tk.append(ImageTk.PhotoImage(image_pil))

            button = tk.Button(
                self.root,
                image=self.images_tk[-1],
                command=self.root.destroy,
            )
            button._name = str(i)
            button.grid(column=i, row=1, padx=5)

        # Create resized images for zoom functionality
        self.images_pil_resized = []
        for i in range(num_thumbnails):
            width = self.images_pil[i].width
            if width < self.zoom_box_width:
                size_multiplier = math.floor(self.zoom_box_width / width) + 1
            else:
                size_multiplier = 2

            self.images_pil_resized.append(
                self.images_pil[i].resize(
                    (width * size_multiplier, width * size_multiplier),
                    resample=Image.Resampling.NEAREST,
                )
            )

        self.root.bind("<Motion>", self.motion)
        self.root.mainloop()
        return getattr(self, "image_index", -1)


# Load test images and run selector as originally requested
test_images = []
test_images.append(Image.open("test/images/1.png"))
test_images.append(Image.open("test/images/2.png"))

selector = WorkingCoverArtSelector(test_images)
selected_index = selector.show_selection_window()
print(f"Selected image index: {selected_index}")
