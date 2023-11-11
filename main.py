from image_classes import *



# def open_image():
#     global canvas, image_scaled_tk
#     image_path = filedialog.askopenfilename(
#         title='Please select a valid image',
#         filetypes=(('All files', '*.*'),
#                    ('PNG', '*.png'),
#                    ('JPG', '*.jpg'),
#                    ('JPEG', '*.jpeg'))
#     )
#     original_image = Image.open(image_path)
#     # Calculate ratio to fit image in canvas
#     canvas_width = canvas.winfo_width()
#     canvas_height = canvas.winfo_height()
#
#     aspect_ratio = original_image.width / original_image.height
#     if canvas_width / aspect_ratio <= canvas_height:
#         new_width = canvas_width
#         new_height = canvas_width / aspect_ratio
#     else:
#         new_height = canvas_height
#         new_width = canvas_height * aspect_ratio
#
#     scaled_image = original_image.resize((int(new_width), int(new_height)))
#
#     image_scaled_tk = ImageTk.PhotoImage(scaled_image)
#     # We resize the canvas to fit exactly the image
#     canvas.config(width=new_width, height=new_height)
#     # img_id = canvas.create_image((canvas_width - new_width) / 2,
#     #                              (canvas_height - new_height) / 2,
#     #                              anchor=NW,
#     #                              image=image_scaled_tk)
#     img_id = canvas.create_image(0,
#                                  0,
#                                  anchor=NW,
#                                  image=image_scaled_tk)
#
#     open_logo_button['state'] = NORMAL
#     set_text_button['state'] = NORMAL


# def open_logo():
#     global logo_scaled_tk, canvas, logo_id
#     logo_path = filedialog.askopenfilename(
#         title='Please select a valid logo',
#         filetypes=(('All files', '*.*'),
#                    ('PNG', '*.png'),
#                    ('JPEG', '*.jpeg'),
#                    ('JPG', '*.jpg'))
#     )
#     logo_img = Image.open(logo_path)
#     # Calculate ratio to fit image in canvas
#     canvas_width = canvas.winfo_width() - 200
#     canvas_height = canvas.winfo_height() - 200
#
#     aspect_ratio = logo_img.width / logo_img.height
#     if canvas_width / aspect_ratio <= canvas_height:
#         new_width = canvas_width
#         new_height = canvas_width / aspect_ratio
#     else:
#         new_height = canvas_height
#         new_width = canvas_height * aspect_ratio
#
#     scaled_image = logo_img.resize((int(new_width), int(new_height)))
#
#     logo_scaled_tk = ImageTk.PhotoImage(scaled_image)
#     logo_id = canvas.create_image((canvas_width - new_width) / 2,
#                                   (canvas_height - new_height) / 2,
#                                   anchor=NW,
#                                   image=logo_scaled_tk)
#
#     resize_logo_button['state'] = NORMAL
#     canvas.tag_bind(logo_id, "<ButtonPress-1>", start_drag)
#     canvas.tag_bind(logo_id, "<ButtonRelease-1>", stop_drag)
#     canvas.tag_bind(logo_id, "<B1-Motion>", drag)
#
#
# def resize_logo():
#     pass
#
#
# # Global variables to track the current drag information
# drag_data = {"item": None, "x": 0, "y": 0}
#
#
# def start_drag(event):
#     # Get the item being dragged
#     drag_data["item"] = canvas.find_closest(event.x, event.y)[0]
#     drag_data["x"] = event.x
#     drag_data["y"] = event.y
#
#
# def stop_drag(event):
#     drag_data["item"] = None
#
#
# def drag(event):
#     global canvas#, image_id
#     #img_coords = canvas.coords(str(image_id))
#     max_x_pos = canvas.winfo_width() - drag_data['item'].winfo_width()
#
#     max_y_pos = canvas.winfo_height() - event.height
#     if drag_data["item"] and event.x <= max_x_pos and event.y <= max_y_pos:
#         # Calculate the distance moved
#         delta_x = event.x - drag_data["x"]
#         delta_y = event.y - drag_data["y"]
#
#         # Move the item by the distance moved
#         canvas.move(drag_data["item"], delta_x, delta_y)
#
#         # Update the x and y for the next drag event
#         drag_data["x"] = event.x
#         drag_data["y"] = event.y

factor = 2.2
maingui = MainGUI(title='Add Watermark', geometry=[int(900*factor), int(600*factor)],
                  canvas_geometry=[int(600*factor), int(350*factor)])

if __name__ == '__main__':
    maingui.mainloop()


