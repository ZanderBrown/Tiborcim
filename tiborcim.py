#! /usr/bin/env python3

from tkinter.ttk import Frame, Button, Notebook, Scrollbar, Style
from tkinter.filedialog import askopenfilename, asksaveasfile
from tkinter.messagebox import showerror, showinfo, askokcancel
from tkinter import Toplevel, Menu, Text, StringVar, IntVar, PhotoImage
from tkinter import DISABLED, NORMAL, END, RIGHT, Y, X, BOTTOM, HORIZONTAL, NONE
from os import sep, altsep
from os.path import join, abspath, dirname
import logging
logging.basicConfig(level=logging.DEBUG)

ICON_PNG = join(abspath(dirname(__file__)), "icon.png")
README_PATH = join(abspath(dirname(__file__)), "readme.md")

class CimReadme(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent)
        self.configure(borderwidth=0)
        self.geometry("+%d+%d" % (
                        parent.winfo_rootx()+30,
                        parent.winfo_rooty()+30))

        self.vbar = Scrollbar(self)
        self.text = Text(self, wrap='word', borderwidth='0p')
        self.vbar['command'] = self.text.yview
        self.vbar.pack(side=RIGHT, fill='y')
        self.text['yscrollcommand'] = self.vbar.set
        self.text.pack(expand=1, fill="both")
        try:
            f = open(README_PATH)
            self.text.delete(1.0)
            self.text.insert(1.0, f.read())
            self.text.delete('end - 1 chars')
        except:
            showerror("Error", "Cannot load README!")
        self.text.config(state='disabled')

        self.title('README')
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.parent = parent
        self.bind('<Escape>', self.close)

    def close(self, event=None):
        self.destroy()

    def show(parent):
        dlg = CimReadme(parent)
        dlg.lift()
        dlg.focus_set()

class CimAbout(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent)
        self.configure(borderwidth=0)
        self.transient(parent)
        self.geometry("+%d+%d" % (
                        parent.winfo_rootx()+30,
                        parent.winfo_rooty()+30))
        from tkinter import Frame, Label
        from sys import version
        from uflash import get_version as uflash_version
        from tibc import get_version as tibc_version

        self.bg = "#bbbbbb"
        self.fg = "#000000"
        
        release = version[:version.index(' ')]
        logofn = ICON_PNG
        self.picture = PhotoImage(master=self._root(), file=logofn)
        self.frameBg = frameBg = Frame(self, bg=self.bg, borderwidth=0)
        frameBg.grid(sticky='nsew')
        label_title = Label(frameBg, text='Cim', fg=self.fg, bg=self.bg,
                           font=('courier', 24, 'bold'))
        label_title.grid(row=0, column=1, sticky="w", padx=10, pady=[10,0])
        label_icon = Label(frameBg, image=self.picture, bg=self.bg)
        label_icon.grid(row=0, column=0, sticky="ne", rowspan=2,
                          padx=10, pady=10)
        byline = "Tiborcim Editor - Tkinter"
        label_info = Label(frameBg, text=byline, justify="left",
                          fg=self.fg, bg=self.bg)
        label_info.grid(row=1, column=1, sticky="w", columnspan=3, padx=10,
                       pady=[0,20])
        label_website = Label(frameBg, text='https://github.com/ZanderBrown/Tiborcim',
                         justify="left", fg=self.fg, bg=self.bg)
        label_website.grid(row=7, column=1, columnspan=2, sticky="w", padx=10, pady=0)
        tiborcim_version = 'Tiborcim ' + tibc_version() + ' (with uFlash ' + uflash_version() + ')' + ' on Python ' + release
        label_version = Label(frameBg, text=tiborcim_version,
                             fg=self.fg, bg=self.bg)
        label_version.grid(row=4, column=1, sticky="w", padx=10, pady=[0,5])

        self.resizable(height="false", width="false")
        self.title('About')
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.parent = parent
        self.bind('<Escape>', self.close)

    def close(self, event=None):
        self.destroy()

    def show(parent):
        dlg = CimAbout(parent)
        dlg.lift()
        dlg.focus_set()
        dlg.grab_set()

class CimTiborcimText(Text):
    def __init__(self, parent):
        Text.__init__(self, parent, wrap=NONE, undo=True, maxundo=-1, borderwidth='0p')
        self.vbar = Scrollbar(parent, name='vbar_tiborcim')
        self.xbar = Scrollbar(parent, name='xbar_tiborcim', orient="horizontal")
        self.bind('<Button-3>',CimEditMenu, add='')
        self.vbar['command'] = self.yview
        self.vbar.pack(side="right", fill=Y)
        self['yscrollcommand'] = self.vbar.set
        self.xbar['command'] = self.xview
        self.xbar.pack(side="bottom", fill=X)
        self['xscrollcommand'] = self.xbar.set
        self.pack(expand=1, fill="both")
        self.tag_configure("keyword", foreground="#ff0000")
        self.tag_configure("string", foreground="#28a030")
        self.tag_configure("block", foreground="#0000ff")
        self.tag_configure("builtin", foreground="#9228a0")

        def text_changed(evt):
            line, col = self.index('insert').split('.')
            txt = self.get('%s.0' % line, '%s.end' % line)
            blocks = [
                "WHILE ", "WEND",                       # WHILE loop
                "SUB ", "END SUB",                      # SUBs
                "IF ", "ELSEIF ", "ELSE", "END IF",     # IF control
                "FOR ", "NEXT",                         # FOR loop
                "PYTHON", "END PYTHON"                  # PYTHON block
            ]
            builtins = [
                "INKEY\$",
                "STR\$", "\bINT",                         # Data casting
                "RND",
                "RECEIVE\$"
            ]
            keywords = [
                "SCREEN ", "PSET ",                     # Leds
                "RADIO ON", "RADIO OFF", "BROADCAST ",  # Radio communications
                "PRINT ",
                "SHOW ",
                "IMAGE ",
                "SLEEP "
            ]
            strings = [
                "\"(.*?)\"",
                "'(.*?)'"
            ]
            self.tag_remove('builtin', '1.0', 'end')
            self.tag_remove('keyword', '1.0', 'end')
            self.tag_remove('string', '1.0', 'end')
            self.tag_remove('block', '1.0', 'end')
            for builtin in builtins:
                self.highlight_pattern(builtin + "(?=([^\"]*\"[^\"]*\")*[^\"]*$)", "builtin", '1.0', 'end', True)
            for keyword in keywords:
                self.highlight_pattern(keyword + "(?=([^\"]*\"[^\"]*\")*[^\"]*$)", "keyword", '1.0', 'end', True)
            for string in strings:
                self.highlight_pattern(string + "(?=([^\"]*\"[^\"]*\")*[^\"]*$)", "string", '1.0', 'end', True)
            for block in blocks:
                self.highlight_pattern(block + "(?=([^\"]*\"[^\"]*\")*[^\"]*$)", "block", '1.0', 'end', True)
            self.edit_modified(False)

        self.bind('<<Modified>>', text_changed)

    def highlight_pattern(self, pattern, tag, start="1.0", end="end",
                          regexp=False):
        start = self.index(start)
        end = self.index(end)
        self.mark_set("matchStart", start)
        self.mark_set("matchEnd", start)
        self.mark_set("searchLimit", end)

        count = IntVar()
        while True:
            index = self.search(pattern, "matchEnd","searchLimit",
                                count=count, regexp=regexp)
            if index == "": break
            if count.get() == 0: break
            self.mark_set("matchStart", index)
            self.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            self.tag_add(tag, "matchStart", "matchEnd")

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
        Notebook.__init__(self, parent, style='Type.TNotebook')
        logger = logging.getLogger(__name__)

        s = Style()
        s.configure('Type.TNotebook', tabposition="se")
        
        self.page_tiborcim = Frame(self)
        self.page_python = Frame(self)
        self.add(self.page_tiborcim, text='Tiborcim')
        self.add(self.page_python, text='Python')

        self.text_tiborcim = CimTiborcimText(self.page_tiborcim)

        self.vbar_python = Scrollbar(self.page_python, name='vbar_python')
        self.xbar_python = Scrollbar(self.page_python, name='xbar_python', orient="horizontal")
        self.text_python = Text(self.page_python, wrap="none", state="disabled", borderwidth='0p')
        self.vbar_python['command'] = self.text_python.yview
        self.vbar_python.pack(side="right", fill="y")
        self.text_python['yscrollcommand'] = self.vbar_python.set
        self.xbar_python['command'] = self.text_python.xview
        self.xbar_python.pack(side="bottom", fill="x")
        self.text_python['xscrollcommand'] = self.xbar_python.set
        self.text_python.pack(expand=1, fill="both")

        self.viewmode = "tiborcim"
        self.saved = True
        self.filename = None

    def save_file(self):
        if self.filename is None:
            self.save_file_as()
        else:
            self.saved = True;
            f = open(self.filename, "w")
            f.write(self.text_tiborcim.get("1.0", "end"))
            f.close() 

    def convert_file(self):
        from tibc import compiler as tibc
        # Should warn if unsaved...
        self.save_file()
        tibc(self.filename)
        try:
            f = open(self.filename + '.py')
            self.text_python.config(state="normal")
            self.text_python.delete("1.0", "end")
            self.text_python.insert("end", f.read())
            self.text_python.config(state="disabled")
        except:
            logging.warning("That's Odd")

    def save_file_as(self):
        f = asksaveasfile(mode='w', defaultextension=".tibas", filetypes=(("Tiborcim", "*.tibas"),("All files", "*.*") ))
        if f is not None:
            self.filename = f.name
            self.save_file()
        
    def load_file(self, name):
        self.saved = True;
        self.filename = name
        logging.debug('Load ' + name)
        try:
            f = open(name)
            self.text_tiborcim.delete("1.0")
            self.text_tiborcim.insert("1.0", f.read())
            self.text_tiborcim.delete('end - 1 chars')
            f.close()
        except:
            showerror("Open Source File", "Failed to read file\n'%s'" % name)
        return

    def view_tiborcim(self, event=None):
        self.select(self.page_tiborcim)
        self.viewmode = "tiborcim"

    def view_python(self, event=None):
        self.select(self.page_python)
        self.viewmode = "python"

    def get_file(self):
        filebit = self.filename.split(sep)
        if len(filebit) == 1:
            filebit = self.filename.split(altsep)
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
        self.master.iconphoto(True, PhotoImage(file=ICON_PNG))
        self.files = []
        self.current_tab = StringVar()
        self.pack(expand=1, fill="both")
        self.master.minsize(300,300)
        self.master.geometry("500x500")

        self.menubar = Menu(self.master)
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
        self.menubar.add_cascade(label="File", menu=self.fileMenu, underline=1)

        self.edit_program = Menu(self.master, tearoff=0)
        self.edit_program.add_command(label="Undo", command=self.edit_undo,
                                  underline=1, accelerator="Ctrl+Z")
        self.edit_program.add_command(label="Redo", command=self.edit_redo,
                                      underline=1, accelerator="Ctrl+Y")
        self.edit_program.add_separator()
        self.edit_program.add_command(label="Cut", command=self.edit_cut,
                                      underline=1, accelerator="Ctrl+X")
        self.edit_program.add_command(label="Copy", command=self.edit_copy,
                                      underline=1, accelerator="Ctrl+C")
        self.edit_program.add_command(label="Paste", command=self.edit_paste,
                                      underline=1, accelerator="Ctrl+V")
        self.menubar.add_cascade(label="Edit", menu=self.edit_program, underline=1)

        self.menu_program = Menu(self.master, tearoff=0)
        self.menu_program.add_command(label="Convert", command=self.convert_file,
                                  underline=1, accelerator="Ctrl+T")
        self.menu_program.add_command(label="Flash", command=self.flash_file,
                                      underline=1, accelerator="Ctrl+B")
        self.menu_program.add_separator()
        self.menubar.add_cascade(label="Program", menu=self.menu_program, underline=1)

        self.menu_view = Menu(self.master, tearoff=0)
        self.viewmode = StringVar()
        self.viewmode.set("tiborcim")
        self.menu_view.add_radiobutton(label="Tiborcim", command=self.view_tiborcim,
                                       variable=self.viewmode, value="tiborcim")
        self.menu_view.add_radiobutton(label="Python", command=self.view_python,
                                       variable=self.viewmode, value="python")
        self.menubar.add_cascade(label="View", menu=self.menu_view, underline=1)

        self.menu_help = Menu(self.master, tearoff=0)
        self.menu_help.add_command(label="README", command=self.help_readme,
                                  underline=1)
        self.menu_help.add_command(label="About", command=self.help_about,
                                  underline=1)
        self.menubar.add_cascade(label="Help", menu=self.menu_help, underline=1)

        self.master.config(width=450, height=400, menu=self.menubar)

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
        self.menu_program.delete(3, END)
        for tab in self.file_tabs.tabs():
            tabtext = self.file_tabs.tab(self.file_tabs.index(tab),"text")
            if tabtext.upper().strip() == title:
                self.current_tab.set(tab)        
            self.menu_program.add_radiobutton(label=tabtext, command=self.program_switch,
                                  underline=1, value=tab, variable=self.current_tab)
        if title != "PYTHON" or title != "TIBORCIM":
            if self.current_file().filename is not None:
                self.master.title(self.current_file().get_file() + " - Tiborcim")
            else:
                self.master.title("Tiborcim")
            if str(self.current_file().tab(self.current_file().index("current"),"text")).upper().strip() == "TIBORCIM":
                self.menubar.entryconfig("Edit", state=NORMAL)
            else:
                self.menubar.entryconfig("Edit", state=DISABLED)
            self.viewmode.set(self.current_file().viewmode)
        if title == "PYTHON":
            self.menubar.entryconfig("Edit", state=DISABLED)
            self.current_file().viewmode = "python";
            self.viewmode.set("python");
        if title == "TIBORCIM":
            self.menubar.entryconfig("Edit", state=NORMAL)
            self.current_file().viewmode = "tiborcim";
            self.viewmode.set("tiborcim");

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

    def program_switch(self):
        self.file_tabs.select(self.current_tab.get())

    def new_file(self, event=None):
        filepage = CimFilePage(self.file_tabs)
        self.file_tabs.add(filepage, text="Unsaved Program")
        self.files.append(filepage)

    def load_file(self, event=None):
        fname = askopenfilename(filetypes=(("Tiborcim", "*.tibas"),("All files", "*.*") ), parent=self.master)
        if fname:
            self.add_file(fname)

    def file_save(self, event=None):
        self.current_file().save_file()
        self.file_tabs.tab(self.current_file(), text=self.current_file().get_file())

    def file_save_as(self, event=None):
        self.current_file().save_file_as()
        self.file_tabs.tab(self.current_file(), text=self.current_file().get_file())

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

    def edit_cut(self, event=None):
        self.current_file().text_tiborcim.event_generate('<Control-x>')

    def edit_copy(self, event=None):
        self.current_file().text_tiborcim.event_generate('<Control-c>')

    def edit_paste(self, event=None):
        self.current_file().text_tiborcim.event_generate('<Control-v>')

    def edit_redo(self, event=None):
        self.current_file().text_tiborcim.edit_redo()
        
    def edit_undo(self, event=None):
        self.current_file().text_tiborcim.edit_undo()

    def help_about(self, event=None):
        CimAbout.show(self)

    def help_readme(self, event=None):
        CimReadme.show(self)

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
