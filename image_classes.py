from tkinter import *
# from tkinter.ttk import *
from tkinter import filedialog
import tkinter.messagebox
from PIL import ImageTk, Image, ImageDraw
import io

PLACEHOLDER_IMAGE = 'resources/images/placeholder.jpg'
FONT = ("Arial", 11)


class MainGUI(Tk):
    def __init__(self, title, geometry, canvas_geometry):
        super().__init__()
        self.title(title)
        self.maxsize(geometry[0], geometry[1])
        self.config(pady=20, padx=5, bg='skyblue')
        self.option_add('*Font', FONT)

        self.left_frame = Frame(self, width=200, height=400, bg='lightgrey')
        self.left_frame.grid(row=0, column=0, padx=5, pady=5)
        self.right_frame = Frame(self, width=650, height=400, bg='lightgrey')
        self.right_frame.grid(row=0, column=1, padx=5, pady=5)

        # We create the main canvas
        self.canvas = CanvasGui(self.right_frame, self, canvas_geometry)

        # Configure the left panel
        left_frame_title = Label(self.left_frame, text='Original Image',
                                 bg='lightgrey')
        left_frame_title.grid(row=0, column=0, padx=5, pady=5)
        self.original_image = Image.open(PLACEHOLDER_IMAGE)
        subsample_image = self.original_image.resize((self.original_image.width // 3,
                                                      self.original_image.height // 3))
        self.scaled_image_tk = ImageTk.PhotoImage(subsample_image)
        self.subsample_label = Label(self.left_frame, image=self.scaled_image_tk)
        self.subsample_label.grid(row=1, column=0, padx=5, pady=5)

        # Tools frame
        self.tool_frame = Frame(self.left_frame, width=180, height=185, bg='lightgrey')
        self.tool_frame.grid(row=2, column=0, padx=5, pady=5)

        (Label(self.tool_frame, text='Tools', background='lightgrey').
         grid(row=0, column=0, padx=5, pady=3, ipadx=10))
        (Label(self.tool_frame, text='Image', background='lightgrey').
         grid(row=0, column=1, padx=5, pady=3, ipadx=10))

        self.open_logo_button = Button(self.tool_frame, text='Open Logo',
                                       state=DISABLED, background='white',
                                       command=self.canvas.open_logo)
        self.open_logo_button.grid(row=1, column=0,
                                   pady=3, padx=3, sticky='w' + 'e' + 'n' + 's')

        self.resize_logo_button = Button(self.tool_frame, text='Resize Logo',
                                         state=DISABLED, background='white')
        self.resize_logo_button.grid(row=2, column=0,
                                     pady=3, padx=3, sticky='w' + 'e' + 'n' + 's')

        self.set_text_button = Button(self.tool_frame, text="Set text",
                                      state=DISABLED, background='white')
        self.set_text_button.grid(row=3, column=0,
                                  pady=3, padx=3, sticky='w' + 'e' + 'n' + 's')

        self.open_image_button = Button(self.tool_frame, text='Open image',
                                        background='white', command=self.canvas.open_image)
        self.open_image_button.grid(row=1, column=1,
                                    pady=3, padx=3, sticky='w' + 'e' + 'n' + 's')

        self.save_image_button = Button(self.tool_frame, text='Save Image',
                                        background='white', state=DISABLED,
                                        command=self.canvas.save_image)
        self.save_image_button.grid(row=2, column=1,
                                    pady=3, padx=3, sticky='w' + 'e' + 'n' + 's')

    def update_original_image(self, img: Image):
        subsample_image = img
        resize_factor = 2
        while subsample_image.width > self.left_frame.winfo_width():
            subsample_image = img.resize((img.width // resize_factor,
                                          img.height // resize_factor))
            resize_factor += 1
        self.scaled_image_tk = ImageTk.PhotoImage(subsample_image)
        self.subsample_label.config(image=self.scaled_image_tk)

    def image_opened_event(self):
        self.open_logo_button['state'] = NORMAL
        self.save_image_button['state'] = NORMAL
        self.set_text_button['state'] = NORMAL

    def logo_opened_event(self):
        self.resize_logo_button['state'] = NORMAL


class CanvasGui(Canvas):
    def __init__(self, parent, window: MainGUI, geometry):
        super().__init__(parent, width=geometry[0], height=geometry[1], bg='white')
        self.grid(row=0, column=0, columnspan=3, pady=10, padx=5)
        self.parent = parent
        self.window = window
        self.img_id = None
        self.logo_id = None
        self.image_tk = None
        self.logo_tk = None
        self.drag_data = {"item": None, "x": 0, "y": 0}

    def open_image(self):
        # TODO: manage cancel button
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

        self.image_tk = ImageTk.PhotoImage(scaled_image)
        # We resize the canvas to fit exactly the image
        self.config(width=new_width, height=new_height)

        self.img_id = self.create_image(0,
                                        0,
                                        anchor=NW,
                                        image=self.image_tk)
        self.window.update_original_image(original_image)
        self.window.image_opened_event()


    # TODO: add_text with popup window
    def add_text(self):
        pass

    # TODO: Decide whether or not delete the logo functionality
    def open_logo(self):
        logo_path = filedialog.askopenfilename(
            title='Please select a valid logo',
            filetypes=(('All files', '*.*'),
                       ('PNG', '*.png'),
                       ('JPEG', '*.jpeg'),
                       ('JPG', '*.jpg'))
        )
        logo_img = Image.open(logo_path)
        # Calculate ratio to fit image in canvas
        canvas_width = self.winfo_width() - 200
        canvas_height = self.winfo_height() - 200

        aspect_ratio = logo_img.width / logo_img.height
        if canvas_width / aspect_ratio <= canvas_height:
            new_width = canvas_width
            new_height = canvas_width / aspect_ratio
        else:
            new_height = canvas_height
            new_width = canvas_height * aspect_ratio

        scaled_image = logo_img.resize((int(new_width), int(new_height)))

        self.logo_tk = ImageTk.PhotoImage(scaled_image)
        self.logo_id = self.create_image((canvas_width - new_width) / 2,
                                         (canvas_height - new_height) / 2,
                                         anchor=NW,
                                         image=self.logo_tk)

        self.tag_bind(self.logo_id, "<ButtonPress-1>", self.start_drag)
        self.tag_bind(self.logo_id, "<ButtonRelease-1>", self.stop_drag)
        self.tag_bind(self.logo_id, "<B1-Motion>", self.drag)

    def start_drag(self, event):
        # Get the item being dragged
        self.drag_data["item"] = self.find_closest(event.x, event.y)[0]
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def stop_drag(self, event):
        self.drag_data["item"] = None

    def drag(self, event):
        #img_coords = canvas.coords(str(image_id))
        bbox = self.bbox(self.drag_data['item'])
        image_width = bbox[2] - bbox[0]
        image_height = bbox[3] - bbox[1]
        max_x_pos = self.winfo_width()
        max_y_pos = self.winfo_height()

        if self.drag_data["item"] and event.x <= max_x_pos and event.y <= max_y_pos:
            # Calculate the distance moved
            delta_x = event.x - self.drag_data["x"]
            delta_y = event.y - self.drag_data["y"]

            # Move the item by the distance moved
            self.move(self.drag_data["item"], delta_x, delta_y)

            # Update the x and y for the next drag event
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y

    def save_image(self):
        ps_data = self.postscript(colormode='color')
        img = Image.open(io.BytesIO(ps_data.encode("utf-8")))
        img.save('output/output.png', format='PNG')
        # TODO: Manage exceptions:
        # ValueError – If the output format could not be determined from the file name. Use the format option to solve this.
        # OSError – If the file could not be written. The file may have been created, and may contain partial data.
        tkinter.messagebox.showinfo("Successful", "Image was saved successfully")

