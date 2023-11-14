from tkinter import *
from tkinter import filedialog
import tkinter.messagebox
from PIL import ImageTk, Image
import io
from photo import *


class CanvasGui(Canvas):
    def __init__(self, parent, window, geometry):
        super().__init__(parent, width=geometry[0], height=geometry[1], bg='white')
        self.original_geometry = geometry
        self.grid(row=0, column=0, columnspan=3, pady=10, padx=5)
        self.parent = parent
        self.window = window
        self.base_image = None
        self.logo_image = None
        self.drag_data = {"item": None, "x": 0, "y": 0}
        self.upper_corner_coords = ()
        self.lower_corner_coords = ()
        self.upper_corner = None
        self.lower_corner = None

    def open_image(self):
        image_path = filedialog.askopenfilename(
            title='Please select a valid image',
            filetypes=(('All files', '*.*'),
                       ('PNG', '*.png'),
                       ('JPG', '*.jpg'),
                       ('JPEG', '*.jpeg'))
        )

        # We check if a file was selected
        if not image_path:
            return

        # We first check whether an image has already been opened, if so
        # we reset the canvas original geometry
        if self.base_image:
            self.config(width=self.original_geometry[0], height=self.original_geometry[1])
            self.update()

        self.base_image = PhotoImageWrapper(self, image_path, False)


    # TODO: add_text with popup window
    def add_text(self):
        pass

    def open_logo(self):
        logo_path = filedialog.askopenfilename(
            title='Please select a valid logo',
            filetypes=(('All files', '*.*'),
                       ('PNG', '*.png'),
                       ('JPEG', '*.jpeg'),
                       ('JPG', '*.jpg'))
        )

        if not logo_path:
            return

        self.logo_image = PhotoImageWrapper(self, logo_path, True)

        self.enable_drag_logo()
        self.window.logo_opened_event()


    def start_drag(self, event):
        # Get the item being dragged
        self.drag_data["item"] = self.find_closest(event.x, event.y)[0]
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def stop_drag(self, event):
        self.drag_data["item"] = None

    def drag(self, event):
        # img_coords = canvas.coords(str(image_id))
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

    def start_resize(self, event):
        # Get the item being dragged
        self.drag_data["item"] = self.find_closest(event.x, event.y)[0]
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        print(f'initial pos: ({event.x}, {event.y})')

    def stop_resize(self, event):
        self.drag_data["item"] = None

    def resize(self, event):
        halo = 50
        delta = 0
        if (self.drag_data["item"] and
                halo < event.x <= self.winfo_width() - halo and
                halo < event.y <= self.winfo_height() - halo):
            if event.x != self.drag_data['x']:
                # Calculate the distance moved
                delta_x = event.x - self.drag_data["x"]

                # Move the item by the distance moved
                self.move(self.drag_data["item"], delta_x, delta_x)
                delta = delta_x
            elif event.y != self.drag_data['y']:
                delta_y = event.y - self.drag_data["y"]

                # Move the item by the distance moved
                self.move(self.drag_data["item"], delta_y, delta_y)
                delta = delta_y

            # if self.drag_data['item'] == self.upper_corner:
            self.logo_image.resize_image(delta)

            self.update()

            # Update the x and y for the next drag event
            self.drag_data["y"] = event.y
            self.drag_data["x"] = event.x

    def save_image(self):
        ps_data = self.postscript(colormode='color')
        img = Image.open(io.BytesIO(ps_data.encode("utf-8")))
        try:
            img.save('output/output.png', format='PNG')
        except ValueError or OSError:
            tkinter.messagebox.showerror(title='Error', message='There was an error saving the image')
        else:
            tkinter.messagebox.showinfo("Successful", "Image was saved successfully")

    def delete_logo(self):
        self.delete(self.logo_image.image_id)
        self.update()
        self.window.logo_deleted_event()

    def resize_logo(self):
        bbox = self.bbox(self.logo_image.image_id)
        print(bbox)

        point_radius = 9

        # We create a point in each corner of the image
        self.upper_corner_coords = (bbox[0], bbox[1])
        self.lower_corner_coords = (bbox[2], bbox[3])

        self.upper_corner = self.create_oval(bbox[0] - point_radius, bbox[1] - point_radius,
                                             bbox[0] + point_radius, bbox[1] + point_radius,
                                             fill='blue')
        self.lower_corner = self.create_oval(bbox[2] - point_radius, bbox[3] - point_radius,
                                             bbox[2] + point_radius, bbox[3] + point_radius,
                                             fill='red')

        self.disable_drag_logo()
        self.enable_corners_drag()

        self.window.resize_logo_event()
        # (center_x - radius, center_y - radius, center_x + radius, center_y + radius,

    def accept_resize(self):
        self.delete(self.upper_corner)
        self.delete(self.lower_corner)

        self.enable_drag_logo()
        self.disable_corners_drag()
        self.window.accept_resize_changes_event()

    def disable_drag_logo(self):
        self.tag_unbind(self.logo_image.image_id, "<ButtonPress-1>")
        self.tag_unbind(self.logo_image.image_id, "<ButtonRelease-1>")
        self.tag_unbind(self.logo_image.image_id, "<B1-Motion>")

    def disable_corners_drag(self):
        pass

    def enable_drag_logo(self):
        self.tag_bind(self.logo_image.image_id, "<ButtonPress-1>", self.start_drag)
        self.tag_bind(self.logo_image.image_id, "<ButtonRelease-1>", self.stop_drag)
        self.tag_bind(self.logo_image.image_id, "<B1-Motion>", self.drag)

    def enable_corners_drag(self):
        # self.tag_bind(self.upper_corner, "<ButtonPress-1>", self.start_resize)
        # self.tag_bind(self.upper_corner, "<ButtonRelease-1>", self.stop_resize)
        # self.tag_bind(self.upper_corner, "<B1-Motion>", self.resize)

        self.tag_bind(self.lower_corner, "<ButtonPress-1>", self.start_resize)
        self.tag_bind(self.lower_corner, "<ButtonRelease-1>", self.stop_resize)
        self.tag_bind(self.lower_corner, "<B1-Motion>", self.resize)

    def resize_canvas_event(self, new_width, new_height):
        self.config(width=new_width, height=new_height)

    def update_original_image(self, original_image: Image):
        self.window.update_original_image(original_image)

    def image_opened_event(self):
        self.window.image_opened_event()


