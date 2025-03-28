import ttkbootstrap as tb
from ttkbootstrap import *
import tkinter as tk
from PIL import Image, ImageTk

# initialize the global variables to track how many boxes are checked, and how many checkboxes there are total
global checkedBoxes
global totalBoxes

def update_notebook_tab(notebook_tab, tab_name, tab_index, chk_vars, *args):
    global checkedBoxes, totalBoxes

    checkedBoxes = 0
    totalBoxes = 0

    for ck, var in chk_vars.items():
        if tab_name in ck:
            totalBoxes += 1
            if var.get():
                checkedBoxes += 1

    # Check if all checkboxes are checked
    if checkedBoxes == totalBoxes:
        print(f'My tab Name: {tab_name}\nTab index: {tab_index}\nTab name: {tab_name}')
        print(f"You've completed PM by checking all {totalBoxes}!")

        # Append the ✅ emoji to the tab name
        new_tab_name = f"{tab_name} ✅"
         # Update the tab's name
        notebook_tab.tab(tab_index, text=new_tab_name)#, bootstyle = "success")        
        #newframe=notebook_tab(notebook_tab,Bootstyle="success")   
    else:
        # For tabs that are not completed, set the regular tab name
        new_tab_name = f"{tab_name}"

        # Update the tab's name
        notebook_tab.tab(tab_index, text=new_tab_name)#, bootstyle = "danger")
        #newframe=notebook_tab(notebook_tab,Bootstyle="danger")  