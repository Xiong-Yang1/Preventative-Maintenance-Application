import tkinter as tk
import ttkbootstrap as tb
import os
import subprocess
import notebookconfigurations.notebookstyle as nbStyle
import interactivefunctions.progressbar as prog
import interactivefunctions.meterwidgets as wig
import dataValueChecks.dataValidations as dv
import dataLookUpTables.lookuptables as lk

from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *


def assay_to_createnotebook(event, instrument_var, assay_drop_down_combo, instrument_assay_mapping, 
                            PM_log, root, entry_notebook, frame1):
    # add the assay path as an argument for the PM_QUERY function
    task_type, ui_type, task_name, operator_symbol, cutoffValue, margin_value, unit_value, optional_value = lk.PM_QUERY(assay_drop_down_combo.get(),instrument_var.get())

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

    # Create Progress Bar.
    total_tasks = sum(
        len(task_dict[t_type]['check'])  # Count entries under the 'entry' key
        for t_type in task_dict  # Iterate through each task type in task_dict
    )
    # Create progress label and progress bar.
    progress_Label = tb.Label(frame1,text="PM Progress Bar:")
    progress_Label.grid(row = 1, column = 6, pady = 5, padx = 5)
    progress_bar = tb.Progressbar(frame1, style = "primary",maximum=total_tasks, length=500)
    progress_bar.grid(row = 1, column = 7, pady = 5, padx =15) 

    selected_instrument = instrument_var.get()
    clear_all_notebooks(root)
    # Update the assay dropdown values based on the selected instrument
    if selected_instrument in instrument_assay_mapping:
        # Get the corresponding assays for the selected instrument
        assays_for_instrument = instrument_assay_mapping[selected_instrument]
        assay_drop_down_combo['values'] = assays_for_instrument
        
        # Keep the previous selection if available
        # If the current selection is no longer in the updated list, reset it
        current_selection = assay_drop_down_combo.get()
        if current_selection not in assays_for_instrument:
            assay_drop_down_combo.set("")  # Clear selection if no longer valid

    else:
        assay_drop_down_combo['values'] = []  # No assays available for selected instrument
        assay_drop_down_combo.set("")  # Clear selection

    # Check if the assay dropdown has a selected value (not empty)
    if assay_drop_down_combo.get() != "":
        # Run the functions if the assay value is selected
        clear_all_notebooks(root)
        createPMLog(PM_log, task_type, ui_type, task_name, operator_symbol, 
                    cutoffValue, margin_value, unit_value, optional_value)
        
        createNoteBook(root, frame1, entry_notebook, progress_bar, task_type, ui_type, 
                       task_name, operator_symbol, cutoffValue, margin_value, 
                       unit_value, optional_value)
    else:
        # Clear all created notebooks if assay is empty
        clear_all_notebooks(root)

def clear_all_notebooks(root):
    """Removes all tabs from notebooks without destroying frames, minimizing flicker."""
    root.update()  # Freeze updates to reduce flickering
    
    def remove_notebook_tabs(widget):
        for child in widget.winfo_children():
            if isinstance(child, tb.Notebook):
                for tab in child.tabs():
                    child.forget(tab)  # Remove each tab instead of destroying the notebook
            else:
                remove_notebook_tabs(child)  # Recursively check deeper widgets

    remove_notebook_tabs(root)
    root.update_idletasks()  # Update UI once after all operations

def createNoteBook(root,frame1,entry_notebook, progress_bar,task_type, ui_type, task_name, operator_symbol, cutoffValue, margin_value, unit_value, optional_value, *args):
    # Organize tasks into a dictionary by task type and UI type
    task_dict = {}
    for i in range(len(task_type)):
        t_type, u_type, t_name, op, cutoff, margin, unit, option = (
            task_type[i], ui_type[i], task_name[i], operator_symbol[i], cutoffValue[i], margin_value[i], unit_value[i], optional_value[i]
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
            "unit_value": unit,
            "optional_value": option
        })

    # Dictionaries to store widget variables
    chk_vars = {}
    chk_btn = {}
    manual_vars = {}
    meter_vars = {}
    toggle_var = {}

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
                task_text, underline_index = dv.format_label(task["task_name"])
                
                chk = tb.Checkbutton(
                    chk_frame, 
                    text=task_text, 
                    variable=chk_vars[f'{task_type}_chk{j}']
                )
                chk.config(underline=underline_index)
                chk.grid(row=j, column=0, sticky="ew", padx=20, pady=8)

                # Add trace for checkboxes
                chk_vars[f'{task_type}_chk{j}'].trace_add(
                    "write",
                    lambda *args, tab_name=tab_name, i=i, j=j: (
                        nbStyle.update_notebook_tab(entry_notebook, tab_name, i, chk_vars),
                        prog.progressBarScale(root, frame1, progress_bar, chk_vars[f'{tab_name}_chk{j}'],entry_notebook)
                    )
                )
                # Create a N/A toggle box for each entry that qualifies for turning off.
                if task["optional_value"] == "Yes":
                    toggle_var[f'{task_type}_entry{j}'] = tb.BooleanVar()

                    toggle = tb.Checkbutton(
                        chk_frame,
                        bootstyle="warning-round-toggle",
                        text="Not In Use",
                        variable=toggle_var[f'{task_type}_entry{j}']
                    )
                    toggle.grid(row=j, column=1, pady=5, padx=10, sticky="nsew")

                    # Add trace to track the button click event.
                    toggle_var[f'{task_type}_entry{j}'].trace_add(
                        "write", lambda *args, var=toggle_var[f'{task_type}_entry{j}'], 
                                        mv=chk_vars[f'{task_type}_chk{j}'], 
                                        ent=chk : dv.toggle_action(var, mv, ent)
                    )
                # Meter widget               

        # ---- ENTRY FRAME ----
        if ui_group["entry"]:
            manual_frame = tb.LabelFrame(notebook_frame, text="Manual Entries", bootstyle="info")
            manual_frame.grid(row=1, column=1, pady=10, padx=10, sticky="nsew")
            meter_frame = tb.LabelFrame(notebook_frame, text="Manual Entry Gauge", bootstyle="info")
            meter_frame.grid(row=1, column=2, pady=10, padx=10, sticky="nsew")
            # Create entry fields and meters for "entry" tasks
            for j, task in enumerate(ui_group["entry"]):
                lower_bound = task["cutoff_value"] - task["margin_value"]
                upper_bound = task["cutoff_value"] + task["margin_value"]
                operator = task["operator_symbol"]
                my_units = task["unit_value"]
                start_value =  lower_bound*.99

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
                    sub_text_label = f'{task["task_name"]} ({lower_bound}-{upper_bound})'
                elif operator == "<" or operator == "≤":
                    commenttext=f'{task["task_name"]} {task["operator_symbol"]} {task["cutoff_value"]} {my_units}'
                    sub_text_label = f'{task["task_name"]} ({lower_bound}-{upper_bound})'
                elif operator =="=":
                    commenttext=f'{task["task_name"]} {task["operator_symbol"]} {task["cutoff_value"]} {my_units}'
                    sub_text_label = f'{task["task_name"]} ({upper_bound})'

                # Label for entry field
                manual_entry_label = tb.Label(
                    manual_frame, 
                    text=commenttext
                )
                manual_entry_label.grid(row=j, column=0, pady=5, padx=10, sticky="nsew")

                # Entry field
                vcmd = root.register(dv.validate_input)
                manual_vars[f'{task_type}_entry{j}'] = tb.DoubleVar()
                manual_vars[f'{task_type}_entry{j}'].set(0)

                manual_entry = tb.Entry(
                    manual_frame, 
                    textvariable=manual_vars[f'{task_type}_entry{j}'],
                    validate="key", 
                    validatecommand=(vcmd, "%P")
                )
                manual_entry.grid(row=j, column=1, pady=5, padx=10, sticky="nsew")

                # Create a N/A toggle box for each entry that qualifies for turning off.
                if task["optional_value"] == "Yes":
                    toggle_var[f'{task_type}_entry{j}'] = tb.BooleanVar()

                    toggle = tb.Checkbutton(
                        manual_frame,
                        bootstyle="warning-round-toggle",
                        text="Not In Use",
                        variable=toggle_var[f'{task_type}_entry{j}']
                    )
                    toggle.grid(row=j, column=2, pady=5, padx=10, sticky="nsew")

                    # Add trace to track the button click event.
                    toggle_var[f'{task_type}_entry{j}'].trace_add(
                        "write", lambda *args, var=toggle_var[f'{task_type}_entry{j}'], 
                                        mv=manual_vars[f'{task_type}_entry{j}'], 
                                        ent=manual_entry: dv.toggle_action(var, mv, ent)
                    )
                # Meter widget
                meter_vars[f'{task_type}_meter{j}'] = manual_vars[f'{task_type}_entry{j}']

                meter_entry = tb.Meter(
                    meter_frame,
                    amountused=0,
                    amounttotal=round(upper_bound * 1.2),
                    subtext=sub_text_label,
                    bootstyle="danger",
                    textright=task["unit_value"],
                    meterthickness=20,
                    metertype="semi",
                    stripethickness=10
                )
                meter_entry.grid(row=1, column=4 + j, pady=5, padx=10)

                # Bind meter update function
                manual_vars[f'{task_type}_entry{j}'].trace_add(
                    "write",
                    lambda varname, index, mode, meter=meter_entry, manual = manual_entry, var=manual_vars[f'{task_type}_entry{j}'], 
                    lower=lower_bound, upper=upper_bound, operator = operator: 
                    wig.update_meter(varname, index, mode, meter, manual, var, lower, upper, operator),
                    #nbStyle.update_notebook_tab(entry_notebook, tab_name, i, chk_vars),
                    #prog.progressBarScaleManualEntry(progress_bar, chk_vars[f'{task_type}_chk{j}'], entry_notebook)
                )

                #manual_entry.bind("<FocusIn>", open_onscreen_keyboard)
def open_onscreen_keyboard(event):
    subprocess.Popen("osk", shell=True)

def createPMLog(PM_log,task_type, ui_type, task_name, operator_symbol, cutoffValue, margin_value, unit_value, optional_value, *args):
    #Assuming each variable returned by PM_QUERY() is a list (column-wise data)
    rowdata = list(zip(task_type, ui_type, task_name, operator_symbol, cutoffValue, margin_value, unit_value, optional_value))

    coldata = [
        {"text": "Task Type", "stretch": False},
        {"text": "UI Type", "stretch": True},
        {"text": "Task Name", "stretch": True},
        {"text": "Operator Symbol", "stretch": False},
        {"text": "Cutoff Value", "stretch": False},
        {"text": "Margin Value", "stretch": False},
        {"text": "Unit Value", "stretch": False},
        {"text": "Optional Value", "stretch": False},
    ]

    for i in range(1,6):
        my_notebookFrame = tb.Frame(PM_log,bootstyle = "darkly")
        PM_log.add(my_notebookFrame, text=f"Tab {i}")
        dt = Tableview(
            master=my_notebookFrame,
            coldata=coldata,
            rowdata=rowdata,
            paginated=True,
            searchable=True,
            bootstyle="primary",
            #editable=True,
            stripecolor=(None, "#B0C4DE"),
        )
        dt.pack(fill=BOTH, expand=YES, padx=10, pady=10)   

