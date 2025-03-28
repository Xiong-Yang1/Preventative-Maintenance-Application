import ttkbootstrap as tb

# this function will retrieve the root window and generate a scroll bars.
# this function was written by AI, chatGPT.
def my_canvas(root):    # Create a Canvas for scrolling -------------------------------------------------------------------- AI GENERATED
    # Create a custom style for the scrollbars
    style = tb.Style()

    # Configure the scrollbar appearance
    style.configure("Custom.Vertical.TScrollbar",
                    troughcolor="#d4f4d7",  # Light green track
                    background="#98df99",  # Default handle color
                    bordercolor="#98df99",  # Border color
                    arrowcolor="#6cbf6c")   # Arrows color
    
    style.configure("Custom.Horizontal.TScrollbar",
                    troughcolor="#d4f4d7",
                    background="#98df99",
                    bordercolor="#98df99",
                    arrowcolor="#6cbf6c")

    # Force the scrollbar thumb (slider) to match the intended color
    style.map("Custom.Vertical.TScrollbar",
              background=[("active", "#82e082"),  # Hover effect
                          ("pressed", "#6cbf6c")])  # Click effect

    style.map("Custom.Horizontal.TScrollbar",
              background=[("active", "#82e082"),
                          ("pressed", "#6cbf6c")])

    # Create a container frame
    container = tb.Frame(root)
    container.pack(fill="both", expand=True, padx=5, pady=5)

    # Create a Canvas
    canvas = tb.Canvas(container)
    
    # Apply the custom style to the scrollbars
    scrollbar_y = tb.Scrollbar(container, orient="vertical", command=canvas.yview, style="Custom.Vertical.TScrollbar")
    scrollbar_x = tb.Scrollbar(root, orient="horizontal", command=canvas.xview, style="Custom.Horizontal.TScrollbar")  

    # Create a Scrollable Frame inside the Canvas
    frame1 = tb.Frame(canvas)

    # Ensure scrolling updates when frame size changes
    frame1.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    frame1.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1*(e.delta//120), "units"))

    # Embed the frame inside the Canvas
    canvas.create_window((0, 0), window=frame1, anchor="nw")

    # Configure Canvas scrolling
    canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

    # Pack the Canvas and Scrollbars
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar_y.pack(side="right", fill="y")
    scrollbar_x.pack(side="bottom", fill="x")
    # Create a Canvas for scrolling -------------------------------------------------------------------- AI GENERATED
    return frame1
