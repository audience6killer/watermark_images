from main_gui import *

factor = 2.2
maingui = MainGUI(title='Add Watermark', geometry=[int(900*factor), int(600*factor)],
                  canvas_geometry=[int(600*factor), int(350*factor)])

if __name__ == '__main__':
    maingui.mainloop()


