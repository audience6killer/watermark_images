from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from PIL import ImageTk, Image


class MainGUI(Tk):
    def __init__(self, title, geometry, canvas_geometry):
        super().__init__()
        self.title(title)
        self.geometry(geometry)
        self.config(pady=30)

        self.canvas = CanvasGui(canvas_geometry)

        self.open_image_button = Button(text='Open image', width=15, command=self.canvas.open_image)
        self.open_image_button.grid(row=2, column=0, columnspan=3, pady=10)

        self.open_logo_button = Button(text='Open Logo', width=15, state=DISABLED)
        self.open_logo_button.grid(row=1, column=0, columnspan=1, pady=10)

        self.resize_logo_button = Button(text='Resize Logo', width=15, state=DISABLED)
        self.resize_logo_button.grid(row=1, column=1, columnspan=1)

        self.set_text_button = Button(text="Set text", width=15, state=DISABLED)
        self.set_text_button.grid(row=1, column=2, columnspan=1)


class CanvasGui(Canvas):
    def __init__(self, geometry):
        super().__init__(width=geometry[0], height=geometry[1])
        self.grid(row=0, column=0, columnspan=3, pady=10)
        self.img_id = None
        self.logo_id = None

    def open_image(self):
        image_path = filedialog.askopenfilename(
            title='Please select a valid image',
            filetypes=(('All files', '*.*'),
                       ('PNG', '*.png'),
                       ('JPG', '*.jpg'),
                       ('JPEG', '*.jpeg'))
        )
        original_image = Image.open(image_path)
        # Calculate ratio to fit image in canvas
        canvas_width = self.winfo_width()
        canvas_height = self.winfo_height()

        aspect_ratio = original_image.width / original_image.height
        if canvas_width / aspect_ratio <= canvas_height:
            new_width = canvas_width
            new_height = canvas_width / aspect_ratio
        else:
            new_height = canvas_height
            new_width = canvas_height * aspect_ratio

        scaled_image = original_image.resize((int(new_width), int(new_height)))

        image_scaled_tk = ImageTk.PhotoImage(scaled_image)
        # We resize the canvas to fit exactly the image
        self.config(width=new_width, height=new_height)
        # img_id = canvas.create_image((canvas_width - new_width) / 2,
        #                              (canvas_height - new_height) / 2,
        #                              anchor=NW,
        #                              image=image_scaled_tk)
        self.img_id = self.create_image(0,
                                        0,
                                        anchor=NW,
                                        image=image_scaled_tk)
        self.update()
        #open_logo_button['state'] = NORMAL
        #set_text_button['state'] = NORMAL

    def open_logo(self):
        pass


# class Image(ImageTk.PhotoImage):
#     def __init__(self):
#         super().__init__()
