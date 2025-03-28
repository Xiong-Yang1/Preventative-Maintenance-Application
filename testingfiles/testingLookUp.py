import ttkbootstrap as tb
import tkinter as tk
import openpyxl
import pandas as pd
# Declare file path to the lookup table.
pm_query_path = r"\\mfad.mfroot.org\rchapp\Tox\Dept\ITTS Files\Projects\PM Project\PM_FORM_QUERY.xlsx"

def PM_QUERY():
    # Load the workbook in read-only mode
    my_pm_table = openpyxl.load_workbook(pm_query_path, read_only=True)
    sheets = my_pm_table['Daily']
    
    # Initialize lists to store all data
    task_type_list = []
    ui_type_list = []
    task_name_list = []
    operator_symbol_list = []
    cutoff_value_list = []
    margin_value_list = []
    unit_value_list = []

    # Dictionary to store grouped data
    task_dict = {}

    # Loop through rows in the sheet
    for row in sheets.iter_rows(min_row=2, min_col=1, max_col=7, values_only=True):
        task_type, ui_type, task_name, operator_symbol, cutoff_value, margin_value, unit_value = row

        # Append values to their respective lists
        task_type_list.append(task_type)
        ui_type_list.append(ui_type)
        task_name_list.append(task_name)
        operator_symbol_list.append(operator_symbol)
        cutoff_value_list.append(cutoff_value)
        margin_value_list.append(margin_value)
        unit_value_list.append(unit_value)

        # Organizing the grouped dictionary
        if task_type and ui_type and task_name:  # Ensure valid values
            if task_type not in task_dict:
                task_dict[task_type] = {}
            if ui_type not in task_dict[task_type]:
                task_dict[task_type][ui_type] = []
            
            # Store all data related to this entry
            task_dict[task_type][ui_type].append({
                "task_name": task_name,
                "operator_symbol": operator_symbol,
                "cutoff_value": cutoff_value,
                "margin_value": margin_value,
                "unit_value": unit_value
            })
    # Print the grouped data
    for task_type, ui_groups in task_dict.items():
        print(f"Task Type: {task_type}")
        for ui_type, tasks in ui_groups.items():
            print(f"  UI Type: {ui_type}")
            for task in tasks:
                print(f"    - {task['task_name']} (Operator: {task['operator_symbol']}, Cutoff: {task['cutoff_value']}, Margin: {task['margin_value']}, Unit: {task['unit_value']})")
        print() 

    # Return all extracted lists and the structured dictionary
    return (task_type_list, ui_type_list, task_name_list, 
            operator_symbol_list, cutoff_value_list, margin_value_list, unit_value_list, task_dict)

# Call the function
task_type_list, ui_type_list, task_name_list, operator_symbol_list, cutoff_value_list, margin_value_list, unit_value_list, task_dict = PM_QUERY()
