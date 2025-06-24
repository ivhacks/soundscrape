import os

os.environ["TK_SILENCE_DEPRECATION"] = "1"

from artwork import CoverArtSelector
from PIL import Image

test_images = []
test_images.append(Image.open("test/images/1.png"))
test_images.append(Image.open("test/images/2.png"))

selector = CoverArtSelector(test_images)
selected_index = selector.show_selection_window()
print(f"Selected image index: {selected_index}")
