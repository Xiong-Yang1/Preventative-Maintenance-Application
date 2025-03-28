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

from ttkbootstrap.scrolled import ScrolledFrame
# The functions will be kept in separate modules for organization and modularity.



# Create the main window
root = tb.Window(themename="superhero")
root.title("PM Entry Form")
root.iconbitmap(r'C:\WKSAdmin\Replicated Files\Local Icons\EXCEL.ico')
root.geometry('1500x800')

# Initialize dictionaries for specific dependencies.
# Please see the module 'dataLookUpTables.lookuptables' for specifics on file paths.
myAssays = lookuptbl.getMyAssays()
myInstruments = lookuptbl.getmyInstruments()
""" for assays in myAssays:
    print(f'Retrieved Assay {assays}')

for instruments in myInstruments:
    print(f'My instruments {instruments}') """
    
# Create the frame to contain labels
frame1 = tb.Frame(root)
frame1.pack(pady=20)

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

progress_Label = tb.Label(frame1,text="PM Progress Bar:")
progress_Label.grid(row = 1, column = 6, pady = 5, padx = 5)
# progress_Label maximum should be set to the total count of tasks on the entire form.
# with the current form, a total of 36 is set only to showcase the functionality.
progress_bar = tb.Progressbar(frame1, style = "Custom.Horizontal.TProgressbar",maximum=200, length=300)
progress_bar.grid(row = 1, column = 7, pady = 5, padx =15)   

# Create Notebook widget to hold tabs based on 'Date and Time' column
style_default_notebook = tb.Style()
style_default_notebook.configure("TNotebook")  # Set the notebook background to white
style_default_notebook.configure("TNotebook.Tab", padding=[10, 5], font=("Arial", 10))  # Default tab style

# Apply a bright green color to the selected tab
style_default_notebook.map("TNotebook.Tab",
          background=[("selected", "620080")],  # Bright green for the selected tab
          foreground=[("selected", "black")],    # Black text on the selected tab
          font=[("selected", ("Arial", 14, "bold"))])  # Bold font for the selected tab

entry_notebook = tb.Notebook(frame1, bootstyle = "warning")
entry_notebook.grid(row = 3, column = 0, columnspan = 10, pady = 20, padx = 20, sticky="ew")

#can be exported as a separate function
# assign the dictionary/lists from lookuptable functions.
# Retrieve data from PM_QUERY function
task_type, ui_type, task_name, operator_symbol, cutoffValue, margin_value, unit_value = PM_QUERY()

# Organize tasks into a dictionary by task type and UI type
task_dict = {}
for i in range(len(task_type)):
    t_type, u_type, t_name, op, cutoff, margin, unit = (
        task_type[i], ui_type[i], task_name[i], operator_symbol[i], cutoffValue[i], margin_value[i], unit_value[i]
    )

    # Initialize task type in dictionary if not exists
    if t_type not in task_dict:
        task_dict[t_type] = {"check": [], "entry": []}

    # Append task details into appropriate UI category
    task_dict[t_type][u_type].append({
        "task_name": t_name,
        "operator_symbol": op,
        "cutoff_value": cutoff,
        "margin_value": margin,
        "unit_value": unit
    })

# Dictionaries to store widget variables
chk_vars = {}
manual_vars = {}
meter_vars = {}

# Iterate through unique task types to create tabs
for i, (task_type, ui_group) in enumerate(task_dict.items()):
    # Create a new notebook tab for each task type
    notebook_frame = tb.Frame(entry_notebook)
    tab_name = task_type
    entry_notebook.add(notebook_frame, text=tab_name)

    # Configure grid layout
    notebook_frame.rowconfigure(0, weight=0)
    notebook_frame.rowconfigure(1, weight=0)

    # ---- CHECKBOX FRAME ----
    if ui_group["check"]:
        chk_frame = tb.LabelFrame(notebook_frame, text="Check Tasks", bootstyle="info")
        chk_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")

        # Create checkboxes for "check" tasks
        for j, task in enumerate(ui_group["check"]):
            chk_vars[f'{task_type}_chk{j}'] = tb.BooleanVar()
            chk = tb.Checkbutton(
                chk_frame, 
                text=task["task_name"], 
                variable=chk_vars[f'{task_type}_chk{j}']
            )
            chk.grid(row=j, column=0, sticky="ew", padx=20, pady=8)

            # Add trace for checkboxes
            chk_vars[f'{task_type}_chk{j}'].trace_add(
                "write",
                lambda *args, tab_name=tab_name, i=i, j=j: (
                    nbStyle.update_notebook_tab(entry_notebook, tab_name, i, chk_vars),
                    prog.progressBarScale(progress_bar, chk_vars[f'{tab_name}_chk{j}'],entry_notebook)
                )
            )

    # ---- ENTRY FRAME ----
    if ui_group["entry"]:
        manual_frame = tb.LabelFrame(notebook_frame, text="Manual Entries", bootstyle="info")
        manual_frame.grid(row=1, column=1, pady=10, padx=10, sticky="nsew")

        # Create entry fields and meters for "entry" tasks
        for j, task in enumerate(ui_group["entry"]):
            lower_bound = task["cutoff_value"] - task["margin_value"]
            upper_bound = task["cutoff_value"] + task["margin_value"]
            operator = task["operator_symbol"]
            my_units = task["unit_value"]
            median_value = (upper_bound + lower_bound) / 2

            if lower_bound == upper_bound:
                lower_bound = 0
            # convert empty units to blank.
            if my_units == "N/A":
                my_units = ""
            else:
                my_units =f"({my_units})"
            # create custom labels for each field type.
            if operator == "±":
                commenttext=f'{task["task_name"]} {lower_bound}-{upper_bound} {my_units}'
            elif operator == "<" or operator == "≤":
                commenttext=f'{task["task_name"]} {task["operator_symbol"]} {task["cutoff_value"]} {my_units}'


            # Label for entry field
            manual_entry_label = tb.Label(
                manual_frame, 
                text=commenttext
            )
            manual_entry_label.grid(row=j, column=0, pady=5, padx=10, sticky="nsew")

            # Entry field
            vcmd = root.register(dv.validate_input)
            manual_vars[f'{task_type}_entry{j}'] = tb.DoubleVar()
            manual_vars[f'{task_type}_entry{j}'].set(lower_bound)
            
            manual_entry = tb.Entry(
                manual_frame, 
                textvariable=manual_vars[f'{task_type}_entry{j}'],
                validate="key", 
                validatecommand=(vcmd, "%P")
            )
            manual_entry.grid(row=j, column=1, pady=5, padx=10, sticky="nsew")

            # Meter widget
            meter_vars[f'{task_type}_meter{j}'] = manual_vars[f'{task_type}_entry{j}']
            meter_entry = tb.Meter(
                notebook_frame,
                amountused=lower_bound,
                amounttotal=round(upper_bound * 1.2),
                subtext=f'{task["task_name"]} ({lower_bound}-{upper_bound})',
                bootstyle="success",
                textright=task["unit_value"],
                meterthickness=20,
                metertype="semi",
                stripethickness=10
            )
            meter_entry.grid(row=1, column=4 + j, pady=5, padx=10)

            # Bind meter update function
            manual_vars[f'{task_type}_entry{j}'].trace_add(
                "write",
                lambda varname, index, mode, meter=meter_entry, var=manual_vars[f'{task_type}_entry{j}'], 
                lower=lower_bound, upper=upper_bound, operator = operator: 
                wig.update_meter(varname, index, mode, meter, var, lower, upper, operator),
                #nbStyle.update_notebook_tab(entry_notebook, tab_name, i, chk_vars),
                #prog.progressBarScale(progress_bar, chk_vars[f'{task_type}_chk{j}'], entry_notebook)
            )


# Creating first button.
entry_Btn = tb.Button(frame1, 
                      text = "Submit", 
                      bootstyle = "success, outline", 
                      command = lambda: (
                                        df1.myFirstFunction(first_entry_Box.entry.get(),
                                                            second_entry_Box.get(), 
                                                            progress_bar,
                                                            chk_togg_var
                                                            )
                                        )
)
entry_Btn.grid(row = 4, column=0,pady=20, padx=20, sticky = "nsew")

# Creating Second button.
entry_Btn = tb.Button(frame1, 
                      text = "Clear", 
                      bootstyle = "danger, outline", 
                      command = lambda: (
                                        df1.mysecondFunction(first_entry_Box.entry.get(),
                                                            second_entry_Box.get(), 
                                                            progress_bar,
                                                            chk_togg_var
                                                            )
                      )
)

entry_Btn.grid(row = 4, column=1, pady=20, padx=20, sticky = "nsew")

# Create Progress Bar.
total_entries = sum(
    len(task_dict[t_type]['check'])  # Count entries under the 'check' key
    for t_type in task_dict  # Iterate through each task type in task_dict
)

progress_Label = tb.Label(frame1,text="PM Progress Bar:")
progress_Label.grid(row = 1, column = 6, pady = 5, padx = 5)
# progress_Label maximum should be set to the total count of tasks on the entire form.
# with the current form, a total of 36 is set only to showcase the functionality.
progress_bar = tb.Progressbar(frame1, style = "Custom.Horizontal.TProgressbar",maximum=total_entries, length=300)
progress_bar.grid(row = 1, column = 7, pady = 5, padx =15)   
# Create Notebook for PM entries
""" notebookHeaders = ['Date',
                   'Staff Name',
                   'Task 1',
                   'Task 2', 
                   'Task 3',
                   'Task 4',
                   'Task 5']
PM_log = tb.Notebook(frame1)
PM_log.grid(row = 5, column = 0, columnspan = 10, pady = 10, padx=5, sticky="ew")
PM_log.add(tb.Frame(PM_log),text="tab1")
PM_log.add(tb.Frame(PM_log),text="tab2")
PM_log.add(tb.Frame(PM_log),text="tab3")
PM_log.add(tb.Frame(PM_log),text="tab4") """

frame1.columnconfigure(9, weight=1)
frame1.rowconfigure(10,weight=2)
frame1.columnconfigure(0,weight=0)
frame1.columnconfigure(1,weight=0)

root.mainloop()
