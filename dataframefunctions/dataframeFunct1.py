import tkinter as tk    
import ttkbootstrap as tb
import datetime as dt
from ttkbootstrap.toast import ToastNotification

def myFirstFunction(root, frame1, myDate, myStaff, toggleButtonStatus, instrumentName, Assay):
    progressBar = None

    # Loop through widgets in root and frame1 to find a progress bar
    for widget in root.winfo_children() + frame1.winfo_children():
        
        if isinstance(widget, tb.Progressbar):  # Check if the widget is a progress bar
            progressBar = widget
            break  # Stop at the first found progress bar
    
    # If no progress bar is found, return or handle accordingly
    if not progressBar:
        print("No progress bar found!")
        return
    # check for meters outside of parameters.
    # Loop through all widgets, including nested ones inside notebooks, frames, etc.
    styles_list = []
    for parent in (root, frame1):
        widgets_to_check = [parent]  # Start with root and frame1
        
        while widgets_to_check:
            widget = widgets_to_check.pop(0)  # Process the first widget in the list
            widget_type = type(widget).__name__  # Get widget type
            available_keys = widget.keys()  # List all available options for the widget
            #print(f"Available properties for the widget: {available_keys}")
            # Check if the widget is a tb.Meter
            if isinstance(widget, tb.Meter):
                widget_class = widget.winfo_class()  # Class of the widget
                widget_name = widget.winfo_name()  # Widget name
                #eter_value = widget.cget("text")
                print(f"Widget: {widget_type}, Class: {widget_class}, Name: {widget_name}")
                
                # Attempt to fetch the widget style, including background and foreground
                try:
                    actual_bg = widget.cget(widget["bootstyle"])  # Returns tuple (R, G, B)
                    actual_fg = widget.cget(widget["bootstyle"])
                except Exception as e:
                    print(f"This is the style i actually want -: {e}")
                    styles_list.append((widget_name,e))
            
            # Add child widgets to the list if they can contain other widgets
            if isinstance(widget, (tk.Frame, tb.Frame, tb.Notebook, tb.Labelframe, tb.PanedWindow)):
                widgets_to_check.extend(widget.winfo_children())  # Add all child widgets

    for style in styles_list:
        print(f'Values are: {style}')

    progressBarCurrent = progressBar['value']
    progressMaxValue = progressBar['maximum']
    toast = None

    if toggleButtonStatus.get():
        toast = ToastNotification(title="Instrument Not in Use",
                                  message="Please advise. . . ",
                                  duration=5000,
                                  bootstyle="warning")
        # Call function for data entry
    elif progressBarCurrent == progressMaxValue:
        toast = ToastNotification(title=f"APPROVED PM - {Assay}",
                                  message=f'Completed by: {myStaff} \nOn: {myDate}\nFor instrument: {instrumentName}!',
                                  duration=6000,
                                  bootstyle="success",
                                  alert=True)
    else:
        toast = ToastNotification(title="PM NOT COMPLETE",
                                  message="PLEASE COMPLETE PM",
                                  duration=5000,
                                  bootstyle="danger")

    toast.show_toast()

    # call function for data entry.
def mysecondFunction(myDate, myStaff, progressBar, toggleButtonStatus):
    progressBarCurrent = progressBar['value']
    progressMaxValue = progressBar['maximum']
    toast = None

    toast = ToastNotification(title = "Function in progress. . .",
                            message = "Please advise. . . ",
                            duration = 3000,
                            bootstyle= "danger"
                            )    
   
    toast.show_toast()
    