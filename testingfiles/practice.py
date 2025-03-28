import ttkbootstrap as tb
import tkinter as tk

def meterColoring(val):
    """Prints the current meter value when the Scale is adjusted."""
    # Access the meter widget's current amount used value
    print(f'Current Meter Widget Value: {meter_widget.amountusedvar.get()}')
    val = int(button_1.get())
    meter_widget.amountusedvar.set(val)
    if val > 450:
        meter_widget.configure(bootstyle = "danger")
        button_1.configure(bootstyle = "danger")
    elif val < 50:
        meter_widget.configure(bootstyle = "danger")
        button_1.configure(bootstyle = "danger")
    else:
        meter_widget.configure(bootstyle = "success")
        button_1.configure(bootstyle = "success")

root = tb.Window(themename="darkly")
root.geometry('210x250')

meter_widget = tb.Meter(root,
                        subtext="testing",
                        textright="barr",
                        bootstyle="success",
                        amounttotal=500,
                        amountused=50,
                        interactive=True
                        )
meter_widget.grid(row=0, column=1, pady=5, padx=5)

# Scale button to adjust meter value
button_1 = tb.Scale(root, bootstyle="success", from_=0, to=500, orient="horizontal", command=meterColoring, value = 50)
button_1.grid(row=1, column=1, pady=5, padx=5)

root.mainloop()
