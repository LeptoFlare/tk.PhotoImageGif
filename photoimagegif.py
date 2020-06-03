"""Contains the PhotoImageGif Class."""
import tkinter as tk
from PIL import Image


class PhotoImageGif(tk.PhotoImage):
    """A tk.PhotoImage object that displays images, and plays them if they are gifs."""

    def __init__(self, root, file):
        """Initilize the PhotoImageGif."""
        super().__init__()

        self.root = root
        self.filepath = file

        self.loc = -1

        self.pil_image = Image.open(self.filepath)

        self.config(file=self.filepath, format=f"gif -index 0")

    def load(self):
        """Load the gif, cycling through the frames."""
        self.create_frames()
        if self.frames > 1:
            self.set_delay()
            self.next_frame()
            if self.next_frame is False:
                return False

    def create_frames(self):
        """Create the frames for the gif."""
        self.frames = 0
        last_frame = False
        while last_frame is False:
            try:
                tk.PhotoImage(file=self.filepath, format=f"gif -index {self.frames}")
                self.frames += 1
            except tk.TclError:
                last_frame = True

    def set_delay(self):
        """Set the delay/duration of the gif."""
        try:
            self.delay = self.pil_image.info["duration"]
        except KeyError:
            self.delay = 100

    def next_frame(self):
        """Go to the next frame."""
        try:
            self.loc = (self.loc + 1) % self.frames
        except TypeError:
            return False
        self.config(format=f"gif -index {self.loc}")
        self.root.after(self.delay, self.next_frame)

    def unload(self):
        """Stop the gif."""
        self.config(format=None)
        self.frames = None
