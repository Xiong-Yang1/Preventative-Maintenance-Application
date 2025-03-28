import tkinter as tk
import ttkbootstrap as tb
import pandas as pd
import datetime as dt

import dataframefunctions.dataframeFunct1 as df1
import dataLookUpTables.lookuptables as lookuptbl
import notebookconfigurations.notebookstyle as nbStyle
import interactivefunctions.progressbar as prog
import interactivefunctions.meterwidgets as wig
import dataValueChecks.dataValidations as dv

from dataLookUpTables.lookuptables import PM_QUERY
from notebookconfigurations.createnotebook import createNoteBook
from notebookconfigurations.createnotebook import createPMLog
from notebookconfigurations.createnotebook import defineNumberofTasks
from notebookconfigurations.createnotebook import assay_to_createnotebook
from notebookconfigurations.createnotebook import clear_all_notebooks
from canvas.canvasframe import my_canvas
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *

# The functions will be kept in separate modules for organization and modularity.



# Create the main window
root = tb.Window(themename="superhero")
root.title("PM Entry Form")
root.iconbitmap(r'C:\WKSAdmin\Replicated Files\Local Icons\EXCEL.ico')
root.withdraw()
root.geometry('1550x800')
root.state('zoomed')
# Initialize dictionaries for specific dependencies.
# Please see the module 'dataLookUpTables.lookuptables' for specifics on file paths.
myAssays, myInstruments, instrument_assay_mapping = lookuptbl.get_Assay_and_Instrument()
""" for assays in myAssays:
    print(f'Retrieved Assay {assays}')

for instruments in myInstruments:
    print(f'My instruments {instruments}') """
# assign the dictionary/lists from lookuptable functions.


""" # Retrieve dictionary/lists from PM_QUERY function this function sets the parameters for generating the form widgets.
task_type, ui_type, task_name, operator_symbol, cutoffValue, margin_value, unit_value, optional_value = PM_QUERY() """    

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
toggle_button = tb.Checkbutton(frame1,bootstyle = "danger-round-toggle",text="Not In Use", variable=chk_togg_var)
toggle_button.grid(row = 2,column=3,pady=5,padx=20, sticky="ew")

# Create Assay Drop-down first so that the instrument combobox has something to attach to.
assay_drop_down_label = tb.Label(frame1,text = "Assay/Method")
assay_drop_down_label.grid(row= 2, column = 6, pady=5, padx=20, sticky="e")
assay_var = tb.StringVar()
assay_drop_down_combo = tb.Combobox(frame1, text= assay_var, state="readonly", width=20)
assay_drop_down_combo.grid(row = 2, column = 7, pady=5, padx=20, sticky = "w")
#assay_drop_down_combo.bind("<<ComboboxSelected>>", update_form_with_new_ranges)
assay_drop_down_combo.bind(  "<<ComboboxSelected>>", 
            lambda event: (assay_to_createnotebook(event,instrument_var, assay_drop_down_combo, instrument_assay_mapping, 
                                                    PM_log, task_type, ui_type, task_name, operator_symbol, 
                                                    cutoffValue, margin_value, unit_value, optional_value, 
                                                    root, entry_notebook, progress_bar),task_type, ui_type, task_name)
)
# Create Instrument Drop-down.
instrument_drop_down_label = tb.Label(frame1,text = "Instrument")
instrument_drop_down_label.grid(row= 2, column = 4, pady=5, padx=20, sticky="e")
instrument_var = tb.StringVar()
instrument_drop_down_combo = tb.Combobox(frame1, textvariable=instrument_var, values=myInstruments, state="readonly", width=20)
instrument_drop_down_combo.grid(row = 2, column = 5, pady=5, padx=20, sticky = "w")
instrument_drop_down_combo.bind("<<ComboboxSelected>>", lambda event: 
                                lookuptbl.update_instruments(event, 
                                                            root, 
                                                            instrument_var,
                                                            assay_drop_down_combo,
                                                            instrument_assay_mapping
                                                            )
                                )

# Retrieve dictionary/lists from PM_QUERY function this function sets the parameters for generating the form widgets.
# This function is ran AFTER the drop-downs are created because the assay value will be used in the path to construct the directory to the reference file.
task_type, ui_type, task_name, operator_symbol, cutoffValue, margin_value, unit_value, optional_value = PM_QUERY()

# progress_Label maximum should be set to the total count of tasks on the entire form.
# utilize this function to determine the number of checkbox/tasks to set the progress bar maximum.
total_tasks = defineNumberofTasks(task_type, ui_type, 
                                    task_name, 
                                    operator_symbol, 
                                    cutoffValue, 
                                    margin_value, 
                                    unit_value
                                    )
total_entries = defineNumberofTasks(task_type, ui_type, 
                                    task_name, 
                                    operator_symbol, 
                                    cutoffValue, 
                                    margin_value, 
                                    unit_value
                                    )

# Create progress label and progress bar.
progress_Label = tb.Label(frame1,text="PM Progress Bar:")
progress_Label.grid(row = 1, column = 6, pady = 5, padx = 5)
progress_bar = tb.Progressbar(frame1, style = "primary",maximum=total_tasks, length=500)
progress_bar.grid(row = 1, column = 7, pady = 5, padx =15)

# Initialize the style object
style_default_notebook = tb.Style()
# Configure the tab style with padding and font
style_default_notebook.configure("TNotebook.Tab", 
                                  padding=[10, 5], 
                                  font=("Arial", 10))
# Apply the changes for the selected tab
style_default_notebook.map("TNotebook.Tab",
                           background=[("selected", "purple")],  # Purple for the selected tab
                           foreground=[("selected", "black")],   # Black text on the selected tab
                           font=[("selected", ("Arial", 14, "bold"))])  # Bold font for the selected tab
# create the notebook object, assign a theme and apply it via the grid method
entry_notebook = tb.Notebook(frame1, bootstyle = "darkly")
entry_notebook.grid(row = 3, column = 0, columnspan = 10, pady = 20, padx = 20, sticky="ew")

# Function to create notebook tabs.
""" createNoteBook(root,entry_notebook, 
                progress_bar, 
                task_type, ui_type, 
                task_name, 
                operator_symbol, 
                cutoffValue, 
                margin_value, 
                unit_value,
                optional_value) """

# Creating first button.
entry_Btn = tb.Button(frame1, 
                      text = "Submit", 
                      bootstyle = "success, outline", 
                      command = lambda: (df1.myFirstFunction(first_entry_Box.entry.get(),
                                                            second_entry_Box.get(), 
                                                            progress_bar,
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
                      command = lambda: (clear_all_notebooks(root))
)
entry_Btn.grid(row = 4, column=1, pady=20, padx=20, sticky = "nsew")

# Create Notebook for PM entries
notebookHeaders = ['Date',
                        'Staff Name',
                        'Task 1',
                        'Task 2', 
                        'Task 3',
                        'Task 4',
                        'Task 5']
PM_log = tb.Notebook(frame1, bootstyle = "primary")
PM_log.grid(row = 5, column = 0, columnspan = 10, pady = 10, padx=5, sticky="ew")

# create the PM log table. Will update this function to generate and update the notebook upon PM entry.
# as of 3/26/25, the PM log only displays the reference ranges to generate the form.
""" createPMLog(PM_log, 
            task_type, 
            ui_type, 
            task_name, 
            operator_symbol, 
            cutoffValue, 
            margin_value, 
            unit_value,
            optional_value) """


root.mainloop()
