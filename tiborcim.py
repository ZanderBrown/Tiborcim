from tkinter.ttk import Frame, Button, Notebook
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror, showinfo
from tkinter import Menu, DISABLED, NORMAL, END
from tkinter.scrolledtext import ScrolledText

class CimApp(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.file = None;
        self.master.title("Tiborcim")
        self.master.iconbitmap('icon.ico')
        
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

        self.nb = Notebook(self)

        self.page1 = Frame(self.nb)
        self.nonpython = ScrolledText(self.page1, state=DISABLED)
        self.nonpython.pack(expand=1, fill="both")
        
        self.page2 = Frame(self.nb)
        self.python = ScrolledText(self.page2, state=DISABLED)
        self.python.pack(expand=1, fill="both")

        self.nb.add(self.page1, text='Tiborcim')
        self.nb.add(self.page2, text='Python')

        self.nb.pack(expand=1, fill="both")

    def view_tiborcim(self):
        self.nb.select(self.page1)

    def view_python(self):
        self.nb.select(self.page2)

    def load_file(self):
        fname = askopenfilename(filetypes=(("Tiborcim", "*.tibas"),
                                           ("All files", "*.*") ))
        if fname:
            try:
                self.file = fname
                self.master.title(fname)
                f = open(self.file)
                self.nonpython.config(state=NORMAL)
                self.nonpython.delete(1.0, END)
                self.nonpython.insert(END, f.read())
                self.nonpython.config(state=DISABLED)
            except:
                showerror("Open Source File", "Failed to read file\n'%s'" % fname)
            return

    def load_file_keyb(self, event):
        self.load_file()

    def convert_file(self):
        from tibc import compiler as tibc
        tibc(self.file)
        try:
            f = open(self.file + '.py')
            self.python.config(state=NORMAL)
            self.python.delete(1.0, END)
            self.python.insert(END, f.read())
            self.python.config(state=DISABLED)
        except:
            print("That's Odd")

    def convert_file_keyb(self, event):
        self.convert_file()

    def flash_file(self):
        from tibc import flash
        from tibc import TibcStatus as status
        result = flash(self.file + '.py')
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
