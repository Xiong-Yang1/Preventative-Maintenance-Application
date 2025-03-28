import tkinter as tk
import ttkbootstrap as tb
import datetime as dt
import dataframefunctions.dataframeFunct1 as df1

from dataLookUpTables.lookuptables import get_Assay_and_Instrument
from dataLookUpTables.lookuptables import update_instruments
from notebookconfigurations.createnotebook import assay_to_createnotebook
from notebookconfigurations.createnotebook import clear_all_notebooks
#from dataValueChecks.login_module import login_window
from canvas.canvasframe import my_canvas
from ttkbootstrap.constants import *

# The functions will be kept in separate modules for organization and modularity.

#user_name = login_window()

# Create the main window
root = tb.Window(themename="superhero")
root.title("PM Entry Form")
root.iconbitmap(r'C:\WKSAdmin\Replicated Files\Local Icons\EXCEL.ico')
#root.withdraw()
root.geometry('1700x700')
#root.state('zoomed')
# Initialize dictionaries for specific dependencies.
# Please see the module 'dataLookUpTables.lookuptables' for specifics on file paths.
myAssays, myInstruments, instrument_assay_mapping = get_Assay_and_Instrument()

# function to generate the frame within a scrollable canvas.
frame1 = my_canvas(root)

# Creating Title Label for form.
title_Label = tb.Label(frame1, text = "CFTL PM Entry Form", font=("Arial", 20))
title_Label.grid(row = 0, column = 1, columnspan = 10, pady=20, padx= 20, sticky="ew")

# Creating First entry row.
first_entry_Label = tb.Label(frame1, text="Please Enter Your Name")
first_entry_Label.grid(row = 1, column = 0, pady = 5, padx = 20, sticky = "ew")
first_entry_Box = tb.DateEntry(frame1, startdate=dt.date.today())
first_entry_Box.grid(row = 1, column = 1, pady = 20, padx = 20, sticky = "nsew")

# Creating second entry row.
second_entry_Label = tb.Label(frame1, text="Staff Name")
second_entry_Label.grid(row = 2, column = 0, pady = 5, padx = 20, sticky = "ew")
second_entry_Box = tb.Entry(frame1, textvariable=". . .")
second_entry_Box.grid(row = 2, column = 1, pady = 20, padx =20, sticky = "nsew")

# Creating the N/A button.
chk_togg_var = tk.BooleanVar()
toggle_button = tb.Checkbutton(frame1,bootstyle = "danger-round-toggle",text="Instrument Not in Use", variable=chk_togg_var)
toggle_button.grid(row = 2,column=3,pady=5,padx=20, sticky="ew")

# Create Assay Drop-down first so that the instrument combobox has something to attach to.
assay_drop_down_label = tb.Label(frame1,text = "Assay/Method")
assay_drop_down_label.grid(row= 2, column = 6, pady=5, padx=20, sticky="e")
assay_var = tb.StringVar()
assay_drop_down_combo = tb.Combobox(frame1, text= assay_var, state="readonly", width=20)
assay_drop_down_combo.grid(row = 2, column = 7, pady=5, padx=20, sticky = "w")
assay_drop_down_combo.bind(  "<<ComboboxSelected>>", 
                            lambda event: (assay_to_createnotebook(event,instrument_var, 
                                                                    assay_drop_down_combo, 
                                                                    instrument_assay_mapping, 
                                                                    PM_log, 
                                                                    root,
                                                                    entry_notebook,
                                                                    frame1
                                                                    )
                                            )
)
# Create Instrument Drop-down.
instrument_drop_down_label = tb.Label(frame1,text = "Instrument")
instrument_drop_down_label.grid(row= 2, column = 4, pady=5, padx=20, sticky="e")
instrument_var = tb.StringVar()
instrument_drop_down_combo = tb.Combobox(frame1, textvariable=instrument_var, values=myInstruments, state="readonly", width=20)
instrument_drop_down_combo.grid(row = 2, column = 5, pady=5, padx=20, sticky = "w")
instrument_drop_down_combo.bind("<<ComboboxSelected>>", lambda event: 
                                update_instruments(event, 
                                                    root, 
                                                    instrument_var,
                                                    assay_drop_down_combo,
                                                    instrument_assay_mapping
                                                    )
                                )
# progress bar and notebooks are generated in separate functions because they are assay/instrument dependent items.
# Initialize the style object
style_default_notebook = tb.Style()
# Configure the tab style with padding and font
style_default_notebook.configure("TNotebook.Tab", 
                                  padding=[10, 5], 
                                  font=("Arial", 10)
                                  )
# Apply the changes for the selected tab
style_default_notebook.map("TNotebook.Tab",
                           background=[("selected", "purple")],  # Purple for the selected tab
                           foreground=[("selected", "black")],   # Black text on the selected tab
                           font=[("selected", ("Arial", 14, "bold"))]
                           )  # Bold font for the selected tab
# create the notebook object, assign a theme and apply it via the grid method
entry_notebook = tb.Notebook(frame1, bootstyle = "darkly")
entry_notebook.grid(row = 3, column = 0, columnspan = 10, pady = 20, padx = 20, sticky="ew")

# Creating first button.
entry_Btn = tb.Button(frame1, 
                      text = "Submit", 
                      bootstyle = "success, outline", 
                      command = lambda: (df1.myFirstFunction(root, 
                                                            frame1,
                                                            first_entry_Box.entry.get(),
                                                            second_entry_Box.get(), 
                                                            chk_togg_var, 
                                                            instrument_drop_down_combo.get(),
                                                            assay_drop_down_combo.get()
                                                            )
                                        )
)
entry_Btn.grid(row = 4, column=0,pady=20, padx=20, sticky = "nsew")

# Creating Second button.
entry_Btn = tb.Button(frame1, 
                      text = "Clear", 
                      bootstyle = "danger, outline", 
                      command = lambda: (clear_all_notebooks(root)
                                        )
)
entry_Btn.grid(row = 4, column=1, pady=20, padx=20, sticky = "nsew")

# Create Notebook for PM entries
PM_log = tb.Notebook(frame1, bootstyle = "primary")
PM_log.grid(row = 5, column = 0, columnspan = 10, pady = 10, padx=5, sticky="ew")

# create the PM log table. Will update this function to generate and update the notebook upon PM entry.
# as of 3/26/25, the PM log only displays the reference ranges to generate the form.

root.mainloop()

