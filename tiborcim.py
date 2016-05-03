from tkinter.ttk import Frame, Button, Notebook
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror, showinfo
from tkinter import Menu, DISABLED, NORMAL, END, LEFT
from tkinter.scrolledtext import ScrolledText

class CimToolbar(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent)

        self.button = Button(self, text="Browse", command=parent.load_file, width=10)
        self.button.pack(side=LEFT)
        
        self.convert_button = Button(self, text="Convert", command=parent.convert_file, width=10)
        self.convert_button.pack(side=LEFT)
        
        self.flash_button = Button(self, text="Flash", command=parent.flash_file, width=10)
        self.flash_button.pack(side=LEFT)

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

        self.master.config(width=450, height=400, menu=menubar)
        
        self.bind_all("<Control-o>", self.load_file)

        self.toolbar = CimToolbar(self)  
        self.toolbar.pack(fill="both")

        self.nb = Notebook(self)

        page1 = Frame(self.nb)
        self.nonpython = ScrolledText(page1, state=DISABLED)
        self.nonpython.pack(expand=1, fill="both")
        
        page2 = Frame(self.nb)
        self.python = ScrolledText(page2, state=DISABLED)
        self.python.pack(expand=1, fill="both")

        self.nb.add(page1, text='Tiborcim')
        self.nb.add(page2, text='Python')

        self.nb.pack(expand=1, fill="both")

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

    def flash_file(self, event=None):
        from tibc import flash
        from tibc import TibcStatus as status
        result = flash(self.file + '.py')
        if result is status.SUCCESS:
            showinfo(title='Success', message='File Flashed', parent=self.master)
        else:
            showerror(title='Failure', message='An Error Occured. Code: %s' % result, parent=self.master)

    def file_quit(self, event=None):
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
