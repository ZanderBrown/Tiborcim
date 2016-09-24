#! /usr/bin/env python3

from tkinter.ttk import Frame, Button, Notebook, Scrollbar
from tkinter.filedialog import askopenfilename, asksaveasfile
from tkinter.messagebox import showerror, showinfo, askokcancel
from tkinter import Menu, Text, DISABLED, NORMAL, END, RIGHT, Y, X, BOTTOM, HORIZONTAL, NONE

import logging
logging.basicConfig(level=logging.DEBUG)


def CimEditMenu(e):
    try:
        e.widget.focus()
        rmenu = Menu(None, tearoff=0, takefocus=0)
        rmenu.add_command(label='Cut', command=lambda e=e: e.widget.event_generate('<Control-x>'))
        rmenu.add_command(label='Copy', command=lambda e=e: e.widget.event_generate('<Control-c>'))
        rmenu.add_command(label='Paste', command=lambda e=e: e.widget.event_generate('<Control-v>'))
        rmenu.tk_popup(e.x_root+40, e.y_root+10,entry="0")
    except TclError:
        pass
    return "break"

class CimFilePage(Notebook):
    def __init__(self, parent):
        Notebook.__init__(self, parent)
        logger = logging.getLogger(__name__)
        self.page_tiborcim = Frame(self)
        self.page_python = Frame(self)
        self.add(self.page_tiborcim, text='Tiborcim')
        self.add(self.page_python, text='Python')

        self.vbar_tiborcim = Scrollbar(self.page_tiborcim, name='vbar_tiborcim')
        self.xbar_tiborcim = Scrollbar(self.page_tiborcim, name='xbar_tiborcim', orient=HORIZONTAL)
        self.text_tiborcim = Text(self.page_tiborcim, wrap=NONE)
        self.text_tiborcim.bind('<Button-3>',CimEditMenu, add='')
        self.vbar_tiborcim['command'] = self.text_tiborcim.yview
        self.vbar_tiborcim.pack(side=RIGHT, fill=Y)
        self.text_tiborcim['yscrollcommand'] = self.vbar_tiborcim.set
        self.xbar_tiborcim['command'] = self.text_tiborcim.xview
        self.xbar_tiborcim.pack(side=BOTTOM, fill=X)
        self.text_tiborcim['xscrollcommand'] = self.xbar_tiborcim.set
        self.text_tiborcim.pack(expand=1, fill="both")

        self.vbar_python = Scrollbar(self.page_python, name='vbar_python')
        self.xbar_python = Scrollbar(self.page_python, name='xbar_python', orient=HORIZONTAL)
        self.text_python = Text(self.page_python, wrap=NONE, state=DISABLED)
        self.vbar_python['command'] = self.text_python.yview
        self.vbar_python.pack(side=RIGHT, fill=Y)
        self.text_python['yscrollcommand'] = self.vbar_python.set
        self.xbar_python['command'] = self.text_python.xview
        self.xbar_python.pack(side=BOTTOM, fill=X)
        self.text_python['xscrollcommand'] = self.xbar_python.set
        self.text_python.pack(expand=1, fill="both")

        self.saved = True
        self.filename = None

    def save_file(self):
        if self.filename is None:
            self.save_file_as()
        else:
            self.saved = True;
            f = open(self.filename, "w")
            f.write(str(self.text_tiborcim.get(1.0, END)))
            f.close() 

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
            logging.warning("That's Odd")

    def save_file_as(self):
        f = asksaveasfile(mode='w', defaultextension=".tibas", filetypes=(("Tiborcim", "*.tibas"),("All files", "*.*") ))
        if f is not None:
            print(f.name)
            self.filename = f.name
            self.save_file()
        
    def load_file(self, name):
        self.saved = True;
        self.filename = name
        logging.debug('Load ' + name)
        try:
            f = open(name)
            self.text_tiborcim.delete(1.0, END)
            self.text_tiborcim.insert(END, f.read())
        except:
            showerror("Open Source File", "Failed to read file\n'%s'" % fname)
        return

    def view_tiborcim(self, event=None):
        self.select(self.page_tiborcim)

    def view_python(self, event=None):
        self.select(self.page_python)

    def get_file(self):
        import os
        filebit = self.filename.split(os.sep)
        if len(filebit) == 1:
            filebit = self.filename.split(os.altsep)
        return filebit[len(filebit) - 1];

    def close(self):
        if not self.saved:
            if askokcancel("Unsaved Changes", "Somefiles havent been saved!"):
                logging.debug("Close Anyway")
                return True
            else:
                self.save_file()
                return False
        else:
            return True

        
class CimApp(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.file = None;
        self.master.title("Tiborcim")
        self.master.iconbitmap('icon.ico')
        self.files = []
        self.pack(expand=1, fill="both")
        self.master.minsize(300,300)
        self.master.geometry("500x500")

        menubar = Menu(self.master)
        self.fileMenu = Menu(self.master, tearoff=0)
        self.fileMenu.add_command(label="New", command=self.new_file,
                                  underline=1, accelerator="Ctrl+N")
        self.fileMenu.add_command(label="Open...", command=self.load_file,
                                  underline=1, accelerator="Ctrl+O")
        self.fileMenu.add_command(label="Save", command=self.file_save,
                                  underline=1, accelerator="Ctrl+S")
        self.fileMenu.add_command(label="Save As...", command=self.file_save_as,
                                  underline=1, accelerator="Ctrl+Alt+S")
        self.fileMenu.add_command(label="Close", command=self.close_file,
                                  underline=1, accelerator="Ctrl+W")
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Exit", command=self.file_quit, underline=1)
        menubar.add_cascade(label="File", menu=self.fileMenu, underline=1)

        self.edit_program = Menu(self.master, tearoff=0)
        self.edit_program.add_command(label="Undo", command=self.edit_undo,
                                  underline=1, accelerator="Ctrl+Z")
        self.edit_program.add_separator()
        self.edit_program.add_command(label="Redo", command=self.edit_redo,
                                      underline=1, accelerator="Ctrl+Y")
        menubar.add_cascade(label="Edit", menu=self.edit_program, underline=1)

        self.menu_program = Menu(self.master, tearoff=0)
        self.menu_program.add_command(label="Convert", command=self.convert_file,
                                  underline=1, accelerator="Ctrl+T")
        self.menu_program.add_separator()
        self.menu_program.add_command(label="Flash", command=self.flash_file,
                                      underline=1, accelerator="Ctrl+B")
        menubar.add_cascade(label="Program", menu=self.menu_program, underline=1)

        self.menu_view = Menu(self.master, tearoff=0)
        viewmode = "tiborcim"
        self.menu_view.add_radiobutton(label="Tiborcim", command=self.view_tiborcim,
                                       variable=viewmode, value="tiborcim")
        self.menu_view.add_radiobutton(label="Python", command=self.view_python,
                                       variable=viewmode, value="python")
        menubar.add_cascade(label="View", menu=self.menu_view, underline=1)

        self.master.config(width=450, height=400, menu=menubar)

        self.bind_all("<Control-o>", self.load_file)
        self.bind_all("<Control-s>", self.file_save)
        self.bind_all("<Control-Alt-s>", self.file_save_as)
        self.bind_all("<Control-t>", self.convert_file)
        self.bind_all("<Control-b>", self.flash_file)
        self.bind_all("<Control-w>", self.close_file)
        self.master.protocol("WM_DELETE_WINDOW", self.file_quit)

        self.file_tabs = Notebook(self)
        self.file_tabs.bind_all("<<NotebookTabChanged>>", self.file_changed)
        self.file_tabs.pack(expand=1, fill="both")

        self.add_file()

    def file_changed(self, event):
        title = str(event.widget.tab(event.widget.index("current"),"text")).upper().strip()
        if title != "PYTHON" or title != "TIBORCIM":
            if self.current_file().filename is not None:
                self.master.title(self.current_file().get_file() + " - Tiborcim")
            else:
                self.master.title("Tiborcim")

    def add_file(self, file=None):
        filepage = CimFilePage(self.file_tabs)
        if file is None:
            self.file_tabs.add(filepage, text="Unsaved Program")
            filepage.saved = False
            filepage.filename = None
        else:
            filepage.load_file(file)
            self.file_tabs.add(filepage, text=filepage.get_file())
        self.files.append(filepage)

    def view_tiborcim(self, event=None):
        self.current_file().view_tiborcim()

    def view_python(self, event=None):
        self.current_file().view_python()

    def new_file(self, event=None):
        filepage = CimFilePage(self.file_tabs)
        self.file_tabs.add(filepage, text="Unsaved Program")
        self.files.append(filepage)

    def load_file(self, event=None):
        fname = askopenfilename(filetypes=(("Tiborcim", "*.tibas"),("All files", "*.*") ), parent=self.master)
        if fname:
            self.add_file(fname)

    def file_save(self, event=None):
        self.file_tabs.tab(self.current_file(), text=self.current_file().get_file())
        self.current_file().save_file()

    def file_save_as(self, event=None):
        self.current_file().save_file_as()

    def convert_file(self, event=None):
        self.current_file().convert_file()

    def current_file(self, event=None):
        return self.files[int(self.file_tabs.index(self.file_tabs.select()))]

    def flash_file(self, event=None):
        from tibc import flash
        from tibc import TibcStatus as status
        self.current_file().convert_file()
        result = flash(self.current_file().filename + '.py')
        if result is status.SUCCESS:
            showinfo(title='Success', message='File Flashed', parent=self.master)
        else:
            showerror(title='Failure', message='An Error Occured. Code: %s' % result, parent=self.master)

    def close_file(self, event=None):
        logging.debug("Close File")
        file = self.current_file()
        if file.close():
            self.file_tabs.forget(file)
            self.files.remove(file)

    def edit_redo(self, event=None):
        self.current_file().text_tiborcim.edit_redo()
        
    def edit_undo(self, event=None):
        self.current_file().text_tiborcim.edit_undo()

    def file_quit(self, event=None):
        for ndx, member in enumerate(self.files):
            logging.debug(self.files[ndx].saved)
            if not self.files[ndx].close():
                return

        self.quit()

_HELP_TEXT = """
Tiborcim - GUI for Tibc the TIBORCIM compiler\n
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
        logging.debug(ex)
