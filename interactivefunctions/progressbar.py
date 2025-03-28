import ttkbootstrap as tb

def progressBarScale(root, frame1, progressBar, chk_var, notebook, *args) :
    # Get the checkbox state (True if checked, False if unchecked)
    checkBox_state = chk_var.get()
    maxprogress = progressBar['maximum']

    """     for parent in (root, frame1):
        widgets_to_check = [parent]  # Start with root and frame1
        
        while widgets_to_check:
            widget = widgets_to_check.pop(0)  # Process the first widget in the list
            widget_type = type(widget).__name__  # Get widget type
            available_keys = widget.keys()  # List all available options for the widget
            #print(f"Available properties for the widget: {available_keys}")
            # Check if the widget is a tb.Meter
            if isinstance(widget, tb.Checkbutton):

                check_value = widget.cget("value")
                if not check_value:
                    print(f"I've removed one checkbox from the total. {check_value}")
                    maxprogress = maxprogress - 1  """
    # Update the progress bar value based on the checkbox state
    if checkBox_state:
        progressBar['value'] += 1  # Increment the progress bar value
        print(f"Progress is currently at: {progressBar['value']}\nMaximum {progressBar['maximum']}")
    else:
        progressBar['value'] -= 1  # Decrement the progress bar value
        
    if progressBar['value'] == progressBar['maximum']:
        # Set the progress bar style to 'success' when full
        progressBar.configure(bootstyle ="success")
        notebook.configure(bootstyle ="success")
    else:
        # Reset the color if the progress bar is not full
        progressBar.configure(bootstyle="primary")
        notebook.configure(bootstyle ="darkly")

""" def progressBarScaleManualEntry(progressBar, notebook, value) :

    progressBar['value'] += value  # Increment the progress bar value
    print(f"Progress is currently at: {progressBar['value']}")

    # actual configuration for widget style    
    if progressBar['value'] == progressBar['maximum']:
        # Set the progress bar style to 'success' when full
        progressBar.configure(bootstyle ="success")
        notebook.configure(bootstyle ="success")
    else:
        # Reset the color if the progress bar is not full
        progressBar.configure(bootstyle="warning")
        notebook.configure(bootstyle ="darkly") """