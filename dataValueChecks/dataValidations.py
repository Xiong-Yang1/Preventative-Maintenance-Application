


def validate_input(P):
    return P.replace('.', '', 1).isdigit() or P == ""  # Allow numbers, decimal point, and empty input

def move_focus(event, next_widget):
    """Move the focus to the next widget when 'Enter' or 'Tab' is pressed."""
    next_widget.focus_set()

def format_label(task_name):
    if task_name in ["Correct Reagent?", "How much?", "Expiration?", "Clear label?", "Keep the lines down?"]:
        return (task_name, 0)  # Underline first character
    return (task_name, -1)  # No underline

def toggle_action(toggle_var, manual_var, entry_widget):
    """Handles toggling of the entry field based on the checkbox."""
    print(toggle_var.get())
    if toggle_var.get():
        manual_var.set(0)  # Set value to 0
        entry_widget.config(state="disabled")  # Disable entry
        entry_widget.config(bootstyle = "warning")
    else:
        entry_widget.config(state="normal")  # Enable entry

