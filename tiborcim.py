from tkinter.ttk import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from tkinter import messagebox, W, E, N, S, HORIZONTAL, DISABLED, NORMAL, END
from tkinter.scrolledtext import ScrolledText

class MyFrame(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.file = None;
        self.master.title("Tiborcim")
        self.master.minsize(width=450, height=400)
        self.master.config(width=450, height=400)
        self.master.rowconfigure(5, weight=1)
        self.master.columnconfigure(5, weight=1)

        self.grid(sticky=W)

        self.button = Button(self, text="Browse", command=self.load_file, width=10)
        self.button.grid(row=1, column=0, sticky=W+E+N+S)

        self.flash_button = Button(self, text="Convert", command=self.convert_file, width=10)
        self.flash_button.grid(row=1, column=1, sticky=W+E+N+S )

        self.flash_button = Button(self, text="Flash", command=self.flash_file, width=10)
        self.flash_button.grid(row=1, column=2, sticky=W+E+N+S )

        self.nb = Notebook(self)

        # adding Frames as pages for the ttk.Notebook 
        # first page, which would get widgets gridded into it
        page1 = Frame(self.nb)
        self.nonpython = ScrolledText(page1, state=DISABLED)
        self.nonpython.pack(expand=1, fill="both")
        
        # second page
        page2 = Frame(self.nb)
        self.python = ScrolledText(page2, state=DISABLED)
        self.python.pack(expand=1, fill="both")

        self.nb.add(page1, text='Tiborcim')
        self.nb.add(page2, text='Python')

        self.nb.grid(row=2, column=0, sticky=W, columnspan=3)

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

    def flash_file(self):
        from tibc import flash
        from tibc import TibcStatus as status
        result = flash(self.file + '.py')
        if result is status.SUCCESS:
            messagebox.showinfo(title='Success', message='File Flashed', parent=self.master)
        else:
            messagebox.showerror(title='Failure', message='An Error Occured. Code: %s' % result, parent=self.master)


if __name__ == "__main__":
    MyFrame().mainloop()
