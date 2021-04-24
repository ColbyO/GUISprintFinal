from tkinter import messagebox, StringVar, Entry, Label, LabelFrame, OptionMenu, Tk, Button, Listbox, Checkbutton, simpledialog, Frame, ANCHOR, IntVar, END, NORMAL, DISABLED, ACTIVE, NSEW, filedialog
import tkinter.ttk as ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import sys
#Setting up Tkinter window
window = Tk()
window.title("Medical GUI")
#Lists for bacterials and medicine .dat files and removing "\n" from the file.
bacterial = ["None"]
with open("bacterial.dat", "r") as bact:
    for line in bact:
        bact_stripped_line = line.strip()
        bact_line_list = bact_stripped_line.split()
        bacterial.append(bact_line_list)

medicine = ["None"]
with open("medicine.dat", "r") as med:
    for line2 in med:
        med_stripped_line = line2.strip()
        med_line_list = med_stripped_line.split()
        medicine.append(med_line_list)

#String/Int Vars
Bact_ID = StringVar()
culture_select = StringVar()
medicine_select = StringVar()
morning_count = StringVar()
evening_count = StringVar()

x_start = StringVar()
x_end = StringVar()

#commands
def exit():
    sys.exit(0)

def save():
    filename = simpledialog.askstring('Save File', 'What would you like to name this file?')
    # extra code that checks if user ends string with txt or dat so file will save, if they did code gets ignored.
    checkpng = []
    checkfile = ".txt" or ".dat"
    checkpng.append(filename)
    # If .txt or .dat isnt in the user entered file_name .dat gets append to it.
    try:
        if any([x in checkfile for x in checkpng]):
            filename = checkpng + ".dat"
    except TypeError as type_error:
        pass

    try:
        with open(filename, "w") as savefile:
            savefile.write("\n".join(listbox.get(0, END)))
            savefile.write("\n")
#If no file name is entered than a error window will pop up, after it will write a new file and space the contents out
    except FileNotFoundError as error:
        messagebox.showerror(title="ERROR", message="No Filename entered.")
    except TypeError as typeerror:
        pass
    else:
        with open(filename, "w") as savefile:
            savefile.write("\n".join(listbox.get(0, END)))
            savefile.write("\n")

def linear_projection():
#Writing a new tkinter window for users to enter info for graphs.
    while True:
        graph_window = Tk()
        graph_window.title("Linear Projection")
        x_start_value_label = Label(graph_window, text="Please enter a start x value for the plot:")
        x_start_value_label.grid(row=0, column=0)
        x_end_value_label = Label(graph_window, text="Please enter a end x value for the plot:")
        x_end_value_label.grid(row=1, column=0)
        x_start_entry = Entry(graph_window, textvariable=x_start)
        x_start_entry.grid(row=0, column=1)
        x_end_entry = Entry(graph_window, textvariable=x_end)
        x_end_entry.grid(row=1, column=1)
        #generates the graph, using matplotlib for a linear graph.
        def gen_graph():
            evening_int = int(evening_count.get())
            morning_int = int(morning_count.get())
            x = np.linspace(int(x_end_entry.get()), int(x_start_entry.get()), 100)
            try:
                b = morning_int
                a = (evening_int - morning_int) / 12
            except ValueError as e:
                messagebox.showerror(title="ERROR", message="Bacterials morning and evening count value's weren't inputted")
            else:
                y = a*x + b
                plt.plot(x, y, '-', label="Bacterial Growth/Decline")
                plt.grid()
                plt.title("Bacterial Growth/Decline")
                plt.xlabel("Growth Period")
                plt.ylabel("Bacterial Growth")
                #Graph wouldn't show line unless one number was negative, this fixes that.
                if int(x_end_entry.get()) > 0 and int(x_start_entry.get()) < 0:
                    plt.show()
                if int(x_start_entry.get()) > 0 and int(x_end_entry.get()) < 0:
                    plt.show()
                if int(x_end_entry.get()) < 0 and int(x_start_entry.get()) < 0:
                    messagebox.showerror(title="ERROR", message="One value must be negative.")
                if int(x_start_entry.get()) > 0 and int(x_end_entry.get()) > 0:
                    messagebox.showerror(title="ERROR", message="One value must be negative.")
        generate_graph_button = Button(graph_window, text="Generate Graph", command=gen_graph)
        generate_graph_button.grid(row=2, column=0, columnspan=2)
        graph_window.mainloop()
        break

def confirm():
    morning = int(morning_count.get())
    evening = int(evening_count.get())
    calc_rate_change = (((evening)/(morning)) -1)
    listbox.insert(END, "{} - {} - {} - {} - {} - {}".format(Bact_ID.get(), culture_select.get(), medicine_select.get(), morning_count.get(), evening_count.get(), calc_rate_change))

#Frames
user_input_frame = LabelFrame(window, text="Enter Information")
user_input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="NSEW")
listbox_frame = LabelFrame(window, text="Data List")
listbox_frame.grid(row=1, column=0, padx=10, pady=10, sticky="NSEW")
button_frame = Frame(window)
button_frame.grid(row=2, column=0, columnspan=1, padx=10, pady=10, sticky="NSEW")

#Dropdown Menus, Inputs, Buttons, Listboxes
#user input frame
bact_id_label = Label(user_input_frame, text="Bacterial ID:")
bact_id_label.grid(row=0, column=0, padx=6, pady=6, sticky="W")
culture_type = Label(user_input_frame, text="Type of Culture:")
culture_type.grid(row=1, column=0, padx=6, pady=6, sticky="W")
medicine_type = Label(user_input_frame, text="Type of Medicine:")
medicine_type.grid(row=2, column=0, padx=6, pady=6, sticky="W")
morn_bact_label = Label(user_input_frame, text="Morning Bacterial Count (6AM):")
morn_bact_label.grid(row=3, column=0, padx=6, pady=6, sticky="W")
even_bact_label = Label(user_input_frame, text="Evening Bacterial Count (6PM):")
even_bact_label.grid(row=4, column=0, padx=6, pady=6, sticky="W")
confirm_button = Button(user_input_frame, text="Confirm", command=confirm, height=2, width=10)
confirm_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

#user input entrys and lists
bact_id_entry = Entry(user_input_frame, textvariable=Bact_ID)
bact_id_entry.grid(row=0, column=1, padx=6, pady=6)
culture_list = ttk.OptionMenu(user_input_frame, culture_select,bacterial[0], *bacterial)
culture_list.grid(row=1, column=1, padx=6, pady=6)
medicine_list = ttk.OptionMenu(user_input_frame, medicine_select, medicine[0], *medicine)
medicine_list.grid(row=2, column=1, padx=6, pady=6)
morning_bact_entry = Entry(user_input_frame, textvariable=morning_count)
morning_bact_entry.grid(row=3, column=1, padx=6, pady=6)
evening_bact_entry = Entry(user_input_frame, textvariable=evening_count)
evening_bact_entry.grid(row=4, column=1, padx=6, pady=6)

#listbox
listbox = Listbox(listbox_frame, height=20, width=50)
listbox.grid(row=0, column=0, padx=6, pady=6)

#Buttons
save_button = Button(button_frame, text="Save", command=save, height=3, width=10)
save_button.grid(row=0, column=0, padx=15, pady=15)
linear_projection_button = Button(button_frame, text="Linear \n Projection", command=linear_projection, height=3, width=10)
linear_projection_button.grid(row=0, column=1, padx=15, pady=15)
exit_button = Button(button_frame, text="Exit", command=exit, height=3, width=10)
exit_button.grid(row=0, column=2, padx=15, pady=15)


window.mainloop()

