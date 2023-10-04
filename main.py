import datetime
import json
import tkinter as tk
from tkinter import ttk
from tkinter.simpledialog import askstring
from tkinter import messagebox
# Define the time intervals (in days) for spaced repetition
time_interval_z = 1
time_interval_a = 8
time_interval_b = 22
time_interval_c = 52
time_interval_d = 82
time_interval_e = 142
time_interval_f = 232


# Function to calculate the next repetition date
def calculate_next_repetition(current_date, time_interval):
    return current_date + datetime.timedelta(days=time_interval)

# Load the list of saved information and next repetition dates from a file, if available
try:
    with open("saved_data.json", "r") as file:
        saved_data = json.load(file)
except FileNotFoundError:
    saved_data = []

# Function to save data to JSON file
def save_json(data):
    with open('saved_data.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Create the main GUI window
root = tk.Tk()
root.title("Spaced Repetition App")

# Create a label for user input
input_label = ttk.Label(root, text="Enter new information:")
input_label.configure(padding=(30, 5))

input_label.pack()

# Create an entry widget for user input
input_entry = ttk.Entry(root)
input_entry.pack()

# Function to add new information
def add_information():
    new_information = input_entry.get().strip()
    if new_information:
        current_datetime = datetime.datetime.now()
        new_entry = {"information": new_information}
        for interval_name, time_interval in [('z', time_interval_z), ('a', time_interval_a), ('b', time_interval_b), ('c', time_interval_c), ('d', time_interval_d), ('e', time_interval_e), ('f', time_interval_f)]:
            next_repetition_date = calculate_next_repetition(current_datetime, time_interval)
            next_repetition_date_key = f"next_repetition_date_{interval_name}"
            new_entry[next_repetition_date_key] = next_repetition_date.isoformat()
        saved_data.append(new_entry)
        save_json(saved_data)
        update_reminders()
        input_entry.delete(0, 'end')

# Create a button to add new information
add_button = ttk.Button(root, text="Add Information", command=add_information)
add_button.pack()

# Create a label for reminders
reminders_label = ttk.Label(root, text="Reminders:")
reminders_label.pack()

# Create a text widget to display reminders
reminders_text = tk.Text(root, width=100, height=10)
reminders_text.pack()

def update_reminders():
    current_datetime = datetime.datetime.now()
    
    # Clear the existing reminders
    reminders_text.config(state=tk.NORMAL)
    reminders_text.delete("1.0", tk.END)
    reminders_text.config(state=tk.DISABLED)

    for entry in saved_data:
        entry_lines = []
        for interval_name in ['z','a', 'b', 'c', 'd','e','f']:
            next_repetition_date_key = f"next_repetition_date_{interval_name}"
            if next_repetition_date_key in entry:
                if "2" in entry[next_repetition_date_key]:
                    next_repetition_date = datetime.datetime.fromisoformat(entry[next_repetition_date_key])
                    if (next_repetition_date - current_datetime).days <= 15 and (next_repetition_date - current_datetime).days >= 0:
                        date_time_text = next_repetition_date.strftime('%Y-%m-%d %H:%M:%S')
                        entry_lines.append(f"Next repetition date '{interval_name}': {date_time_text}")
        if entry_lines:
            topic_lesson_text = entry['information']
            reminders_text.config(state=tk.NORMAL)  # Enable editing
            reminders_text.insert(tk.END, "Topic/lesson to review: ", "green")
            reminders_text.insert(tk.END, topic_lesson_text + "\n")
            for line in entry_lines:
                reminders_text.insert(tk.END, line + "\n", "blue")
            reminders_text.insert(tk.END, "\n\n")  # Two blank lines between entries
            reminders_text.config(state=tk.DISABLED)  # Disable editing

    # Optionally, you can update the GUI after clearing and adding new reminders
    root.update_idletasks()




reminders_text.tag_config("green", foreground="green")
reminders_text.tag_config("blue", foreground="blue")
reminders_text.tag_config("red", foreground="red")







# Create a button to remove completed items
def remove_done():
    user_information = askstring("Remove Completed", "Enter the information you completed exactly as it is:")
    information_code = askstring("Remove Completed", "Enter the repetition date code you have done(z,a,b,c,d,e,f):")
    print(information_code)
    next_repetition_date_key = "null"
    if user_information:
        user_information = user_information.strip()
        for entry in saved_data:
            if entry["information"] == user_information:
                next_repetition_date_key = f'next_repetition_date_{information_code}'
                print(next_repetition_date_key)
                if next_repetition_date_key in entry:
                    entry[next_repetition_date_key] = "done"
                """
                for interval_name in ['a', 'b', 'c', 'd']:
                    next_repetition_date_key = f"next_repetition_date_{interval_name}"
                    
                """
                save_json(saved_data)
                update_reminders()
                break
        else:
            messagebox.showwarning("Topic Not Found", f"Topic not found: {user_information}")


remove_button = ttk.Button(root, text="Remove Completed", command=remove_done)
remove_button.pack()

# Initialize GUI with existing reminders
update_reminders()

# Start the Tkinter main loop
root.mainloop()
