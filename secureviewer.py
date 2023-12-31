import tkinter as tk
from tkinter import messagebox
# importing everything from tkinter
from tkinter import *
# importing ttk for styling widgets from tkinter
from tkinter import ttk
# importing filedialog from tkinter
from tkinter import filedialog as fd
# importing os module
import os
# importing the PDF_Functions class from the functions file and other functions
from functions import PDF_Functions
from opendoc import open_doc
import keyboard
import signal

# creating a class called PDFViewer
class PDFViewer:
    # initializing the __init__ / special method
    def __init__(self, master):
        # path for the pdf doc
        self.path = None
        ###############SRC###################
        self.src = None
        # state of the pdf doc, open or closed
        self.fileisopen = None
        # author of the pdf doc
        self.author = None
        # name for the pdf doc
        self.name = None
        # the current page for the pdf
        self.current_page = 0
        # total number of pages for the pdf doc
        self.numPages = None    
        # creating the window
        self.master = master
        # gives title to the main window
        self.master.title('SecureViewer')
        # gives dimensions to main window
        self.master.geometry('1080x720+440+180')
        # this disables the minimize/maximize button on the main window
        self.master.resizable(width = 0, height = 0)
        # loads the icon and adds it to the main window
        self.master.iconbitmap(self.master, 'UVA.ico')
        # creating the menu
        self.menu = Menu(self.master)
        # adding it to the main window
        self.master.config(menu=self.menu)
        # creating a sub menu
        self.filemenu = Menu(self.menu)
        # giving the sub menu a label
        self.menu.add_cascade(label="Archivo", menu=self.filemenu)
        # adding a two buttons to the sub menus
        self.filemenu.add_command(label="Abrir Archivo", command=self.open_file)
        #self.filemenu.add_command(label="Exit", command=self.master.destroy)
        # creating the top frame
        self.top_frame = ttk.Frame(self.master, width=780, height=950)
        # placing the frame using inside main window using grid()
        self.top_frame.grid(row=1, column=0)
        # the frame will not propagate
        self.top_frame.grid_propagate(True)
        # creating the bottom frame
        self.bottom_frame = ttk.Frame(self.master, width=1080, height=50)
        # placing the frame using inside main window using grid()
        self.bottom_frame.grid(row=0, column=0)
        # the frame will not propagate
        self.bottom_frame.grid_propagate(False)
        
        # creating a vertical scrollbar
        self.scrolly = Scrollbar(self.top_frame, orient=VERTICAL)
        # adding the scrollbar
        self.scrolly.grid(row=0, column=1, sticky=(N,S))
        # creating a horizontal scrollbar
        self.scrollx = Scrollbar(self.top_frame, orient=HORIZONTAL)
        # adding the scrollbar
        self.scrollx.grid(row=1, column=0, sticky=(W, E))


        # creating the canvas for display the PDF pages
        self.output = Canvas(self.top_frame, bg='#ECE8F3', width=1360, height=750)
        self.output.scale
        # inserting both vertical and horizontal scrollbars to the canvas
        self.output.configure(yscrollcommand=self.scrolly.set, xscrollcommand=self.scrollx.set)
        # adding the canvas
        self.output.grid(row=0, column=0, padx=(80, 5), pady=2)
        # configuring the horizontal scrollbar to the canvas
        self.scrolly.configure(command=self.output.yview)
        # configuring the vertical scrollbar to the canvas
        self.scrollx.configure(command=self.output.xview)


        # loading the button icons
        self.uparrow_icon = PhotoImage(file='uparrow.png')
        self.downarrow_icon = PhotoImage(file='downarrow.png')
        # resizing the icons to fit on buttons
        self.uparrow = self.uparrow_icon.subsample(3, 3)
        self.downarrow = self.downarrow_icon.subsample(3, 3)
        # creating an up button with an icon
        self.upbutton = ttk.Button(self.bottom_frame, image=self.uparrow, command=self.previous_page)
        # adding the button
        self.upbutton.grid(row=0, column=1, padx=(470, 5), pady=2)
        # creating a down button with an icon
        self.downbutton = ttk.Button(self.bottom_frame, image=self.downarrow, command=self.next_page)
        # adding the button
        self.downbutton.grid(row=0, column=2, pady=2)
        # label for displaying page numbers
        self.page_label = ttk.Label(self.bottom_frame, text='página')
        # adding the label
        self.page_label.grid(row=0, column=5, pady=2)
       

        # label_1 for introduction page number
        self.label1=tk.Label(self.bottom_frame,text="Ir a la página:")
        # adding the label_1
        self.label1.grid(row=0, column=10, padx=(100, 5), pady=2)
        # creating box for introduction page number
        self.dato=tk.StringVar()
        self.entry1=tk.Entry(self.bottom_frame, width=10, textvariable=self.dato)
        self.entry1.grid(row=0, column=12, pady=2)
        self.boton1=tk.Button(self.bottom_frame, text="IR", command=self.browse)
        self.boton1.grid(row=0, column=16,padx=(20, 5), pady=2)
        
    

    # function for opening uva files
    def open_file(self):
        # open the file dialog
        filepath = fd.askopenfilename(title='Seleccione un archivo .uva', initialdir=os.getcwd(), filetypes=(('UVA', '*.uva'), ))
        # checking if the file exists
        if filepath:
            # declaring the path
            self.path = filepath
            # extracting the uva file from the path
            filename = os.path.basename(self.path)

            try:       
                self.src = open_doc(filepath)
                # passing the path to PDF_Functions
                self.functions = PDF_Functions(self.path,self.src)
                # getting data and numPages
                data, numPages = self.functions.get_metadata()
                # setting the current page to 0
                self.current_page = 0
                # checking if numPages exists
                if numPages:
                    # getting the title
                    self.name = data.get('title', filename[:-4])
                    # getting the author
                    self.author = data.get('author', None)
                    self.numPages = numPages
                    # setting fileopen to True
                    self.fileisopen = True
                    # calling the display_page() function
                    self.display_page()
                    # replacing the window title with the PDF document name
                    self.master.title(self.name)
            
            except:
                messagebox.showinfo(message="La información obtenida no genera un PDF válido", title="Formato incorrecto")
    
    # the function to display the page  
    def display_page(self):
        # checking if numPages is less than current_page and if current_page is less than
        # or equal to 0
        if 0 <= self.current_page < self.numPages:
            # getting the page using get_page() function from functions
            self.img_file = self.functions.get_page(self.current_page)
            # inserting the page image inside the Canvas
            self.output.create_image(0, 0, anchor='nw', image=self.img_file)
            # the variable to be stringified
            self.stringified_current_page = self.current_page + 1
            # updating the page label with number of pages 
            self.page_label['text'] = str(self.stringified_current_page) + ' de ' + str(self.numPages)
            # creating a region for inserting the page inside the Canvas
            region = self.output.bbox(ALL)
            # making the region to be scrollable
            self.output.configure(scrollregion=region)         

    # function for displaying next page
    def next_page(self):
        # checking if file is open
        if self.fileisopen:
            # checking if current_page is less than or equal to numPages-1
            if self.current_page < self.numPages - 1:
                # updating the page with value 1
                self.current_page += 1
                
                # displaying the new page
                self.display_page()
                            
    # function for displaying the previous page        
    def previous_page(self):
        # checking if fileisopen
        if self.fileisopen:
            # checking if current_page is greater than 0
            if self.current_page > 0:
                # decrementing the current_page by 1
                self.current_page -= 1
                
                # displaying the previous page
                self.display_page()

    # function for displaying the page        
    def browse(self):
        
        # checking if fileisopen
        if self.fileisopen:

            # checking if current_page is greater than 0
                        
            try:
                int(self.dato.get())
                value=int(self.dato.get())
                
                if 0 < value <= self.numPages:
                    # updating the page 
                    self.current_page = value-1
                    
                    # displaying the new page
                    self.display_page()
                else:
                    self.entry1.delete(0,'end')
                    messagebox.showinfo(message="La página " + str(value) + " no existe en el documento", title="Número de página incorrecto")
               

            except ValueError:
                
                self.entry1.delete(0,'end')
                messagebox.showinfo(message="Debe introducir un número de página", title="Número de página incorrecto")
                

class KeyBlocker:
    def __init__(self, v):
        self.locked = False
        v.bind("<FocusIn>", self.on_focus_in)
        v.bind("<FocusOut>", self.on_focus_out)
        v.bind("<Destroy>", self.on_focus_out)
        v.bind_class("Toplevel", "<FocusIn>", self.on_focus_in)
        v.bind_class("Toplevel", "<FocusOut>", self.on_focus_out)
        v.bind_class("Toplevel", "<Destroy>", self.on_focus_out)

        signal.signal(signal.SIGTERM, self.on_focus_out)

    def on_focus_in(self, event):
        self.lock()
    
    def on_focus_out(self, event):
        self.unlock()

    def lock(self):
        if(not self.locked):
            for i in range(65):
                keyboard.block_key(i)
            self.locked = True

    def unlock(self):
        if(self.locked):
            for i in range(65):
                keyboard.unblock_key(i)
            self.locked = False


  
# creating the root winding using Tk() class
root = Tk()
root.state('zoomed')
# disabling part of keyboard to avoid screenshots
kb = KeyBlocker(root)
# instantiating/creating object app for class PDFViewer
app = PDFViewer(root)
# calling the mainloop to run the app infinitely until user closes it
root.mainloop()

