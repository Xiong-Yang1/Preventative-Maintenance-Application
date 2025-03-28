import ttkbootstrap as tb
import tkinter as tk

def update_meter(varname, index, mode, meter, manual_entry,var, lower_bound, upper_bound, operator):
    #Update the Meter widget whenever the associated entry field changes.
    #Also updates meter color based on thresholds.
    try:
        val = var.get()  # Get the value from the variable
        operator = operator  # Get the operator symbol
                
        # If the value is empty, reset to 0
        if val == "":
            val = 0
        if val > (upper_bound * 1.2):
            var.set(round(upper_bound * 1.2))

        #print(f'Entered Value = {val}, LowerBound = {lower_bound}, UpperBound = {upper_bound}, operator = {operator}')
        
        # Apply conditions based on the operator
        if operator == "<":
            if val > lower_bound and val < upper_bound:
                meter.configure(bootstyle="success")
                manual_entry.configure(bootstyle = "success")
            else:
                meter.configure(bootstyle="danger")
                manual_entry.configure(bootstyle = "danger")
        elif operator == "≤":
            if val > lower_bound and val <= upper_bound:
                meter.configure(bootstyle="success")
                manual_entry.configure(bootstyle = "success")
            else:
                meter.configure(bootstyle="danger") 
                manual_entry.configure(bootstyle = "danger")
        elif operator == "±":        
            # Apply color based on thresholds
            if val < lower_bound or val > upper_bound:
                meter.configure(bootstyle="danger")
                manual_entry.configure(bootstyle = "danger")
            else:
                meter.configure(bootstyle="success")
                manual_entry.configure(bootstyle = "success")
        elif operator == "=":        
            # Apply color based on thresholds
            if val == upper_bound:
                meter.configure(bootstyle="success")
                manual_entry.configure(bootstyle = "success")
            else:
                meter.configure(bootstyle="danger")
                manual_entry.configure(bootstyle = "danger")


        # Update the meter widget value
        meter.amountusedvar.set(var.get())
        
    except ValueError:
        # Handle cases where entry is empty or invalid
        print("Invalid input detected, setting meter to 0.")
        meter.amountusedvar.set(0)
        meter.configure(bootstyle="danger")
