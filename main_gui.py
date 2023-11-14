from canvas_gui import *

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

        # Tools configuration frame
        self.tool_config_frame = Frame(self.left_frame, width=180, height=20,
                                       bg='lightgrey')
        self.tool_config_frame.grid(row=3, column=0, padx=5, pady=5)

        # (Label(self.tool_config_frame, text='Configuration', background='lightgrey').
        # grid(row=0, column=0, padx=5, pady=3, ipadx=10))

        # Tools column
        self.open_logo_button = Button(self.tool_frame, text='Open Logo',
                                       state=DISABLED, background='white',
                                       command=self.canvas.open_logo)
        self.open_logo_button.grid(row=1, column=0,
                                   pady=3, padx=3, sticky='w' + 'e' + 'n' + 's')

        self.resize_logo_button = Button(self.tool_frame, text='Resize Logo',
                                         state=DISABLED, background='white',
                                         command=self.canvas.resize_logo)
        self.resize_logo_button.grid(row=2, column=0,
                                     pady=3, padx=3, sticky='w' + 'e' + 'n' + 's')

        self.delete_logo_button = Button(self.tool_frame, text='Delete Logo',
                                         state=DISABLED, background='white',
                                         command=self.canvas.delete_logo)
        self.delete_logo_button.grid(row=3, column=0,
                                     pady=3, padx=3, sticky='w' + 'e' + 'n' + 's')

        self.set_text_button = Button(self.tool_frame, text="Set text",
                                      state=DISABLED, background='white')
        self.set_text_button.grid(row=4, column=0,
                                  pady=3, padx=3, sticky='w' + 'e' + 'n' + 's')

        # Image column
        self.open_image_button = Button(self.tool_frame, text='Open image',
                                        background='white', command=self.canvas.open_image)
        self.open_image_button.grid(row=1, column=1,
                                    pady=3, padx=3, sticky='w' + 'e' + 'n' + 's')

        self.change_image_button = Button(self.tool_frame, text='Change image',
                                          background='white', state=DISABLED,
                                          command=self.canvas.open_image)
        self.change_image_button.grid(row=2, column=1,
                                      pady=3, padx=3, sticky='w' + 'e' + 'n' + 's')

        self.save_image_button = Button(self.tool_frame, text='Save Image',
                                        background='white', state=DISABLED,
                                        command=self.canvas.save_image)
        self.save_image_button.grid(row=3, column=1,
                                    pady=3, padx=3, sticky='w' + 'e' + 'n' + 's')

        # Configuration frame
        self.accept_resize = Button(self.tool_config_frame, text='Accept Resize',
                                    state=NORMAL, background='white',
                                    command=self.canvas.accept_resize)
        self.accept_resize.grid(row=0, column=0,
                                pady=3, padx=3, sticky='w' + 'e' + 'n' + 's')
        self.accept_resize.grid_forget()

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
        self.change_image_button['state'] = NORMAL
        # self.set_text_button['state'] = NORMAL

    def logo_opened_event(self):
        self.resize_logo_button['state'] = NORMAL
        self.delete_logo_button['state'] = NORMAL

    def logo_deleted_event(self):
        self.resize_logo_button['state'] = DISABLED
        self.delete_logo_button['state'] = DISABLED

    def resize_logo_event(self):
        self.resize_logo_button['state'] = DISABLED
        self.delete_logo_button['state'] = DISABLED
        self.open_logo_button['state'] = DISABLED
        self.save_image_button['state'] = DISABLED
        self.change_image_button['state'] = DISABLED
        self.open_image_button['state'] = DISABLED

        self.accept_resize.grid(row=0, column=0,
                                pady=3, padx=3, sticky='w' + 'e' + 'n' + 's')


