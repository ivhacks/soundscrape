import os
import tempfile
from unittest import TestCase
from unittest.mock import patch

from agentic_art_selector import pick_art_agentic


def read_test_image(name: str) -> bytes:
    with open(os.path.join("test", "images", name), "rb") as f:
        return f.read()


class AgenticArtSelectorTests(TestCase):
    def test_dumps_choices_named_by_index_and_resolution(self):
        art_dir = tempfile.mkdtemp()
        images = [read_test_image("1.png"), read_test_image("1_low_res_300x300.png")]
        with patch("agentic_art_selector.tempfile.mkdtemp", return_value=art_dir):
            with patch("builtins.input", return_value=f"{art_dir}/0_1024x1024.png"):
                pick_art_agentic(images)
        self.assertEqual(
            sorted(os.listdir(art_dir)), ["0_1024x1024.png", "1_300x300.png"]
        )
        with open(os.path.join(art_dir, "1_300x300.png"), "rb") as f:
            self.assertEqual(f.read(), images[1])

    def test_picks_second_choice(self):
        art_dir = tempfile.mkdtemp()
        images = [read_test_image("1.png"), read_test_image("2.png")]
        with patch("agentic_art_selector.tempfile.mkdtemp", return_value=art_dir):
            with patch("builtins.input", return_value=f"{art_dir}/1_1200x1200.png"):
                self.assertEqual(pick_art_agentic(images), 1)

    def test_reprompts_on_bad_path(self):
        art_dir = tempfile.mkdtemp()
        images = [read_test_image("1.png"), read_test_image("2.png")]
        answers = ["/tmp/not_a_choice.png", f"{art_dir}/1_1200x1200.png"]
        with patch("agentic_art_selector.tempfile.mkdtemp", return_value=art_dir):
            with patch("builtins.input", side_effect=answers) as fake_input:
                self.assertEqual(pick_art_agentic(images), 1)
        self.assertEqual(fake_input.call_count, 2)

    def test_crashes_when_stdin_closes(self):
        images = [read_test_image("1.png")]
        with patch("builtins.input", side_effect=EOFError):
            with self.assertRaises(EOFError):
                pick_art_agentic(images)
