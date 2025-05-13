import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime

file_types = {
    "Images": [".png", ".jpg", ".jpeg", ".gif", ".bmp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv"],
    "Music": [".mp3", ".wav", ".aac"],
    "Archives": [".zip", ".rar", ".tar", ".gz"],
}

LOG_FILE = "organizer_log.txt"

def get_file_category(extension):
    for category, extensions in file_types.items():
        if extension.lower() in extensions:
            return category
    return "Others"

def get_file_info(path):
    size = os.path.getsize(path)
    created = datetime.fromtimestamp(os.path.getctime(path)).strftime("%Y-%m-%d %H:%M:%S")
    modified = datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y-%m-%d %H:%M:%S")
    return size, created, modified

def write_log(file_structure):
    with open(LOG_FILE, "a") as log:
        log.write(f"\n===== Organized on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} =====\n")
        for category, files in file_structure.items():
            log.write(f"{category}/\n")
            for file in files:
                log.write(f"  └── {file['name']} ({file['size']}, Created: {file['created']}, Modified: {file['modified']})\n")

def organize_files(folder_path):
    if not folder_path:
        return

    count = 0
    file_structure = {}

    for filename in os.listdir(folder_path):
        src_path = os.path.join(folder_path, filename)
        if os.path.isfile(src_path):
            _, ext = os.path.splitext(filename)
            size, created, modified = get_file_info(src_path)

            proceed = messagebox.askyesno(
                "Confirm Organization",
                f"Do you want to organize this file?\n\n"
                f"File: {filename}\n"
                f"Size: {size} bytes\n"
                f"Created: {created}\n"
                f"Modified: {modified}"
            )

            if not proceed:
                continue

            category = get_file_category(ext)
            category_path = os.path.join(folder_path, category)
            os.makedirs(category_path, exist_ok=True)
            dest_path = os.path.join(category_path, filename)
            shutil.move(src_path, dest_path)

            file_structure.setdefault(category, []).append({
                "name": filename,
                "size": f"{size} bytes",
                "created": created,
                "modified": modified
            })
            count += 1

    if count > 0:
        write_log(file_structure)

    return count, file_structure

def display_structure(file_structure):
    lines = []
    for category, files in file_structure.items():
        lines.append(f"{category}/")
        for file in files:
            lines.append(f"  └── {file['name']} ({file['size']}, Created: {file['created']}, Modified: {file['modified']})")
    return "\n".join(lines)

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        count, structure = organize_files(folder_path)
        messagebox.showinfo("Success", f"Organized {count} files successfully!")

        result_window = tk.Toplevel(root)
        result_window.title("Organized Folder Structure")
        result_window.geometry("700x500")
        result_window.configure(bg="#f0f0f0")

        result_text = tk.Text(result_window, wrap=tk.WORD, font=("Courier New", 10), padx=10, pady=10, bg="#ffffff")
        result_text.insert(tk.END, display_structure(structure))
        result_text.configure(state="disabled")
        result_text.pack(expand=True, fill="both", padx=20, pady=20)

        close_btn = tk.Button(result_window, text="Close", command=result_window.destroy,
                              font=("Segoe UI", 11), bg="#ddd", relief="flat", padx=10, pady=5)
        close_btn.pack(pady=10)

        exit_btn_output = tk.Button(result_window, text="Exit", font=("Segoe UI", 12),
                                    bg="#757575", fg="white", relief="flat", padx=20, pady=10, bd=0)
        exit_btn_output.pack(pady=5)
        exit_btn_output.bind("<Enter>", on_enter_exit_output)
        exit_btn_output.bind("<Leave>", on_leave_exit_output)
        exit_btn_output.configure(command=root.quit)

def clear_log(log_window):
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as log:
            log.write("")
        messagebox.showinfo("Log Cleared", "All log entries have been deleted.")
    log_window.destroy()

def view_log():
    if not os.path.exists(LOG_FILE) or os.path.getsize(LOG_FILE) == 0:
        messagebox.showinfo("No Logs", "No file organization log is available yet.")
        return

    with open(LOG_FILE, "r") as log:
        content = log.read()

    log_window = tk.Toplevel(root)
    log_window.title("Organization Log")
    log_window.geometry("700x500")
    log_window.configure(bg="#f8f8f8")

    log_text = tk.Text(log_window, wrap=tk.WORD, font=("Courier New", 10), padx=10, pady=10, bg="#ffffff")
    log_text.insert(tk.END, content)
    log_text.configure(state="disabled")
    log_text.pack(expand=True, fill="both", padx=20, pady=20)

    btn_frame = tk.Frame(log_window, bg="#f8f8f8")
    btn_frame.pack(pady=10)

    clear_btn = tk.Button(btn_frame, text="Clear Log & Close", command=lambda: clear_log(log_window),
                          font=("Segoe UI", 11), bg="#f44336", fg="white", relief="flat", padx=15, pady=6)
    clear_btn.pack(side="left", padx=10)

    close_btn = tk.Button(btn_frame, text="Close", command=log_window.destroy,
                          font=("Segoe UI", 11), bg="#ddd", relief="flat", padx=15, pady=6)
    close_btn.pack(side="left", padx=10)

def on_enter_select(e):
    select_btn['bg'] = "#4CAF50"
    select_btn['fg'] = 'white'

def on_leave_select(e):
    select_btn['bg'] = "#2196F3"
    select_btn['fg'] = 'white'

def on_enter_exit(e):
    exit_btn['bg'] = "#f44336"
    exit_btn['fg'] = 'white'

def on_leave_exit(e):
    exit_btn['bg'] = "#757575"
    exit_btn['fg'] = 'white'

def on_enter_log(e):
    log_btn['bg'] = "#ffa000"
    log_btn['fg'] = 'white'

def on_leave_log(e):
    log_btn['bg'] = "#ffca28"
    log_btn['fg'] = 'black'

def on_enter_exit_output(e):
    e.widget['bg'] = "#f44336"

def on_leave_exit_output(e):
    e.widget['bg'] = "#757575"

# GUI Setup
root = tk.Tk()
root.title("File Organizer GUI")
root.geometry("500x300")
root.configure(bg="#e6f2ff")

frame = tk.Frame(root, bg="#e6f2ff")
frame.pack(expand=True)

label = tk.Label(frame, text="Organize Files by Type", font=("Helvetica", 16, "bold"), bg="#e6f2ff")
label.pack(pady=20)

select_btn = tk.Button(frame, text="Select Folder", font=("Segoe UI", 12),
                       bg="#2196F3", fg="white", padx=20, pady=10, relief="flat", bd=0)
select_btn.pack(pady=10)
select_btn.bind("<Enter>", on_enter_select)
select_btn.bind("<Leave>", on_leave_select)
select_btn.configure(command=select_folder)

log_btn = tk.Button(frame, text="View Log", font=("Segoe UI", 12),
                    bg="#ffca28", fg="black", padx=20, pady=10, relief="flat", bd=0)
log_btn.pack(pady=5)
log_btn.bind("<Enter>", on_enter_log)
log_btn.bind("<Leave>", on_leave_log)
log_btn.configure(command=view_log)

exit_btn = tk.Button(frame, text="Exit", font=("Segoe UI", 12),
                     bg="#757575", fg="white", padx=20, pady=10, relief="flat", bd=0)
exit_btn.pack(pady=5)
exit_btn.bind("<Enter>", on_enter_exit)
exit_btn.bind("<Leave>", on_leave_exit)
exit_btn.configure(command=root.quit)

root.mainloop()
