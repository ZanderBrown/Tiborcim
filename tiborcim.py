from tkinter.ttk import Frame, Button, Notebook
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror, showinfo
from tkinter import Menu, DISABLED, NORMAL, END
from tkinter.scrolledtext import ScrolledText

class CimFilePage(Notebook):
    def __init__(self, parent):
        Notebook.__init__(self, parent)
        self.page_tiborcim = Frame(self)
        self.page_python = Frame(self)
        self.add(self.page_tiborcim, text='Tiborcim')
        self.add(self.page_python, text='Python')
        self.text_tiborcim = ScrolledText(self.page_tiborcim)
        self.text_tiborcim.pack(expand=1, fill="both")
        self.text_python = ScrolledText(self.page_python, state=DISABLED)
        self.text_python.pack(expand=1, fill="both")

    def save_file(self):
        print('Save ' + self.filename)

    def convert_file(self):
        from tibc import compiler as tibc
        # Should warn if unsaved...
        self.save_file()
        tibc(self.filename)
        try:
            f = open(self.filename + '.py')
            self.text_python.config(state=NORMAL)
            self.text_python.delete(1.0, END)
            self.text_python.insert(END, f.read())
            self.text_python.config(state=DISABLED)
        except:
            print("That's Odd")

    def save_file_as(self, name):
        self.filename = name
        save_file()
        
    def load_file(self, name):
        self.filename = name
        print('Load ' + name)
        try:
            f = open(name)
            self.text_tiborcim.delete(1.0, END)
            self.text_tiborcim.insert(END, f.read())
        except:
            showerror("Open Source File", "Failed to read file\n'%s'" % fname)
        return

    def view_tiborcim(self):
        self.select(self.page_tiborcim)

    def view_python(self):
        self.select(self.page_python)
        
class CimApp(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.file = None;
        self.master.title("Tiborcim")
        self.master.iconbitmap('icon.ico')
        self.files = []
        self.pack(expand=1, fill="both")

        menubar = Menu(self.master)
        self.fileMenu = Menu(self.master, tearoff=0)
        self.fileMenu.add_command(label="Open...", command=self.load_file,
                                  underline=1, accelerator="Ctrl+O")
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Exit", command=self.file_quit, underline=1)
        menubar.add_cascade(label="File", menu=self.fileMenu, underline=1)

        self.menu_program = Menu(self.master, tearoff=0)
        self.menu_program.add_command(label="Convert", command=self.convert_file,
                                  underline=1, accelerator="Ctrl+T")
        self.menu_program.add_separator()
        self.menu_program.add_command(label="Flash", command=self.flash_file,
                                      underline=1, accelerator="Ctrl+B")
        menubar.add_cascade(label="Program", menu=self.menu_program, underline=1)
        self.master.config(width=450, height=400, menu=menubar)

        self.menu_view = Menu(self.master, tearoff=0)
        viewmode = "tiborcim"
        self.menu_view.add_radiobutton(label="Tiborcim", command=self.view_tiborcim,
                                       variable=viewmode, value="tiborcim")
        self.menu_view.add_radiobutton(label="Python", command=self.view_python,
                                       variable=viewmode, value="python")
        menubar.add_cascade(label="View", menu=self.menu_view, underline=1)

        self.bind_all("<Control-o>", self.load_file_keyb)
        self.bind_all("<Control-t>", self.convert_file_keyb)
        self.bind_all("<Control-b>", self.flash_file_keyb)

        self.file_tabs = Notebook(self)
        self.nb = CimFilePage(self.file_tabs)
        self.files.append(self.nb)

        self.file_tabs.add(self.nb, text='Unsaved Script')
        self.file_tabs.pack(expand=1, fill="both")

    def add_file(self, file):
        filepage = CimFilePage(self.file_tabs)
        self.file_tabs.add(filepage, text=file)
        filepage.load_file(file)
        self.files.append(filepage)

    def view_tiborcim(self):
        self.current_file().view_tiborcim()

    def view_python(self):
        self.current_file().view_python()

    def load_file(self):
        fname = askopenfilename(filetypes=(("Tiborcim", "*.tibas"),("All files", "*.*") ))
        if fname:
            self.add_file(fname)

    def load_file_keyb(self, event):
        self.load_file()

    def convert_file(self):
        self.current_file().convert_file()

    def convert_file_keyb(self, event):
        self.convert_file()

    def current_file(self):
        return self.files[int(self.file_tabs.index(self.file_tabs.select()))]

    def flash_file(self):
        from tibc import flash
        from tibc import TibcStatus as status
        self.current_file().convert_file()
        result = flash(self.current_file().filename + '.py')
        if result is status.SUCCESS:
            showinfo(title='Success', message='File Flashed', parent=self.master)
        else:
            showerror(title='Failure', message='An Error Occured. Code: %s' % result, parent=self.master)

    def flash_file_keyb(self, event):
        self.flash_file()

    def file_quit(self):
        self.quit()

_HELP_TEXT = """
Tiborcim - GUI for Tibc\n
 (C) Copyright Alexander Brown 2016\r\n
"""


if __name__ == "__main__":
    import argparse, sys
    argv = sys.argv[1:]
    try:
        parser = argparse.ArgumentParser(description=_HELP_TEXT)
        args = parser.parse_args(argv)
        CimApp().mainloop()
    except Exception as ex:
        print(ex)
