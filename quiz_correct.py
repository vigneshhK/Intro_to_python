import tkinter as tk
from tkinter import scrolledtext, filedialog
from tkinter import simpledialog
import subprocess
import threading
import re
import os

# Function to run the DepotDownloader command
def run_command(pubfileid, account_name, account_password):
    printlog(f"----------Downloading {pubfileid}--------\n")
    if 'save_location' not in globals():
        printlog("Error: Save location is not set correctly.\n")
        return
    if not os.path.isdir(save_location):
        printlog("Error: Save location is not exist.\n")
        return
    target_directory = os.path.join(save_location, "projects", "myprojects")
    if not os.path.isdir(target_directory):
        printlog("Invaild save location: Selected directory does not contain \\projects\\myprojects\n")
        return
    downloader_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "DepotdownloaderMod", "DepotDownloadermod.exe")
    if not os.path.isfile(downloader_path):
        printlog(f"Error: Downloader executable not found: {downloader_path}\n")
        return
    command = [
        downloader_path,
        "-app", "431960",
        "-pubfile", pubfileid,
        "-verify-all",
        "-username", account_name,
        "-password", account_password,
        "-dir", os.path.join(target_directory, pubfileid),
    ]
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
    output_buffer = ""
    auth_prompted = False
    while True:
        character = process.stdout.read(1)
        if not character:
            break
        output_buffer += character
        if character == "\n":
            printlog(output_buffer)
            output_buffer = ""
        elif not auth_prompted:
            upper_output = output_buffer.upper()
            guard_position = upper_output.find("STEAM GUARD")
            code_position = upper_output.find("AUTH CODE", guard_position)
            if guard_position >= 0 and code_position >= 0 and upper_output.rfind(":") > code_position:
                printlog(output_buffer)
                output_buffer = ""
                auth_event = threading.Event()
                root.after(0, prompt_steam_guard, process, auth_event)
                auth_event.wait()
                auth_prompted = True
    if output_buffer:
        printlog(output_buffer)
    process.stdout.close()
    process.stdin.close()
    process.wait()
    printlog(f"-------------Download finished-----------\n")

def printlog(log):
    if threading.current_thread() is not threading.main_thread():
        root.after(0, printlog, log)
        return
    console.config(state=tk.NORMAL)
    console.insert(tk.END, log)
    console.yview(tk.END)
    console.config(state=tk.DISABLED)

def prompt_steam_guard(process, auth_event):
    code = simpledialog.askstring("Steam Guard", "Enter the code sent to your email:", parent=root)
    if code:
        process.stdin.write(code.strip() + "\n")
        process.stdin.flush()
    else:
        process.terminate()
        printlog("Steam Guard code entry cancelled.\n")
    auth_event.set()

# Function to handle running commands in sequence
def run_commands(account_name, account_password):
    run_button.config(state=tk.DISABLED)
    links = link_text.get("1.0", tk.END).splitlines()
    for link in links:
        if link:
            match = re.search(r'\b\d{8,10}\b', link.strip())
            if match:
                run_command(match.group(0), account_name, account_password)
            else:
                printlog(f"Invalid link: {link}\n")
    run_button.config(state=tk.NORMAL)
    root.after(0, lambda: password_entry.delete(0, tk.END))
            
# Function to run commands in a separate thread
def start_thread():
    account_name = username_entry.get().strip()
    account_password = password_entry.get()
    if not account_name or not account_password:
        printlog("Enter your Steam username and password before downloading.\n")
        return
    threading.Thread(target=run_commands, args=(account_name, account_password), daemon=True).start()

def on_closing():
    subprocess.Popen("taskkill /f /im DepotDownloadermod.exe", creationflags=subprocess.CREATE_NO_WINDOW)
    os._exit(0)

# Function to select save location
def select_save_location():
    selected_directory = filedialog.askdirectory()
    target_directory = os.path.join(selected_directory, "projects", "myprojects")
    if not os.path.isdir(target_directory):
        printlog("Invaild save location: Selected directory does not contain \\projects\\myprojects\n")
    else:
        printlog(f"Path set to {selected_directory}\n")
        global save_location
        save_location = selected_directory
        save_location_label.config(text=f"Save Location: {selected_directory}")
        with open('lastsavelocation.cfg', 'w') as file:
            file.write(selected_directory)

def load_save_location():
    try:
        with open('lastsavelocation.cfg', 'r') as file:
            target_directory = file.read().strip()
            if os.path.isdir(target_directory):
                global save_location
                save_location = target_directory
            else:
                save_location = "Not set"
    except FileNotFoundError:
        save_location = "Not set"

load_save_location()

# GUI setup
root = tk.Tk()
root.title("Wallpaper Engine Workshop Downloader")

title_label = tk.Label(root, text="Wallpaper Engine Workshop Downloader", font=("Arial", 21))
title_label.grid(row=0, column=0)

# Steam credentials
username_label = tk.Label(root, text="Steam username:")
username_label.grid(row=1, column=0, sticky='e', padx=(0, 8))
username_entry = tk.Entry(root, width=32)
username_entry.grid(row=1, column=1, sticky='w')
password_label = tk.Label(root, text="Steam password:")
password_label.grid(row=2, column=0, sticky='e', padx=(0, 8))
password_entry = tk.Entry(root, width=32, show="*")
password_entry.grid(row=2, column=1, sticky='w')

# Save location button
save_location_button = tk.Button(root, text="Select wallpaper engine path", command=select_save_location)
save_location_button.grid(row=3, column=0, columnspan=2)

save_location_label = tk.Label(root, text=f"Wallpaper engine path: {save_location}")
save_location_label.grid(row=4, column=0, columnspan=2)

# Link input
link_label = tk.Label(root, text="Enter workshop items (one per line, support link and file id):")
link_text = scrolledtext.ScrolledText(root, height=10)
link_label.grid(row=5, column=0, columnspan=2)
link_text.grid(row=6, column=0, columnspan=2)

# Console output
console_label = tk.Label(root, text="Console Output:")
console = scrolledtext.ScrolledText(root, height=10)
console_label.grid(row=7, column=0, columnspan=2)
console.grid(row=8, column=0, columnspan=2)
console.config(state=tk.DISABLED)

# Run button
run_button = tk.Button(root, text="Download", command=start_thread)
run_button.grid(row=9, column=0, columnspan=2)

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()