import tkinter as tk
from PIL import ImageTk, Image


class PhotoImageWrapper:
    def __init__(self, parent, image_path: str, is_logo: bool):
        self.parent = parent
        self.image_id = None
        self.image_tk = None
        self.scaled_image = None
        self.original_image = Image.open(image_path)

        # Calculate ratio to fit image in canvas
        canvas_width = parent.winfo_width()
        canvas_height = parent.winfo_height()

        new_width = 0
        new_height = 0
        if not is_logo:
            aspect_ratio = self.original_image.width / self.original_image.height
            if canvas_width / aspect_ratio <= canvas_height:
                new_width = canvas_width
                new_height = canvas_width / aspect_ratio
            else:
                new_height = canvas_height
                new_width = canvas_height * aspect_ratio

            self.scaled_image = self.original_image.resize((int(new_width), int(new_height)))

            self.image_tk = ImageTk.PhotoImage(self.scaled_image)
            # We resize the canvas to fit exactly the image
            self.parent.resize_canvas_event(new_width=new_width, new_height=new_height)

            self.image_id = self.parent.create_image(0,
                                                     0,
                                                     anchor=tk.NW,
                                                     image=self.image_tk)

            self.parent.update_original_image(self.original_image)
            self.parent.image_opened_event()
        else:
            resize_quantity = 200
            canvas_height -= resize_quantity
            canvas_height -= resize_quantity

            aspect_ratio = self.original_image.width / self.original_image.height
            if canvas_width / aspect_ratio <= canvas_height:
                new_width = canvas_width
                new_height = canvas_width / aspect_ratio
            else:
                new_height = canvas_height
                new_width = canvas_height * aspect_ratio

            self.scaled_image = self.original_image.resize((int(new_width), int(new_height)))

            self.image_tk = ImageTk.PhotoImage(self.scaled_image)
            self.image_id = self.parent.create_image((canvas_width - new_width) / 2,
                                                     (canvas_height - new_height) / 2,
                                                     anchor=tk.NW,
                                                     image=self.image_tk)

    def resize_image(self, delta):
        if self.scaled_image.width > 100:
            new_size = (self.scaled_image.width+delta, self.scaled_image.height+delta)
            self.scaled_image = self.original_image.resize(new_size, Image.LANCZOS)
            self.image_tk = ImageTk.PhotoImage(self.scaled_image)
            self.parent.itemconfig(self.image_id, image=self.image_tk)




