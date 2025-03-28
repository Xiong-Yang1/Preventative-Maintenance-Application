import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *

app = ttk.Window()
colors = app.style.colors

my_notebook = ttk.Notebook(app,bootstyle = "primary")
my_notebook.grid(row = 0, column = 0, pady = 10, padx = 10)

coldata = [
    {"text": "LicenseNumber", "stretch": False},
    "CompanyName",
    {"text": "UserCount", "stretch": False},
]

rowdata = [
    ('A123', 'IzzyCo', 12),
    ('A136', 'Kimdee Inc.', 45),
    ('A158', 'Farmadding Co.', 36)
]

for i in range(6):
    my_notebookFrame = ttk.Frame(my_notebook,bootstyle = "secondary")
    my_notebook.add(my_notebookFrame, text="Tab {i}")
    dt = Tableview(
        master=my_notebookFrame,
        coldata=coldata,
        rowdata=rowdata,
        paginated=True,
        searchable=True,
        bootstyle="primary",
        stripecolor=(colors.light, None),
    )
    dt.pack(fill=BOTH, expand=YES, padx=10, pady=10)

app.mainloop()
