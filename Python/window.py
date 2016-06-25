import tkinter


class Interface:
    def __init__(self):
        self.__window = tkinter.Tk()
        self.config_appearance()

    def config_appearance(self):
        self.config_window()
        self.config_widgets()

    def config_window(self):
        pass

    def config_widgets(self):
        pass

    def show_window(self):
        self.__window.mainloop()


interface = Interface()
interface.show_window()
