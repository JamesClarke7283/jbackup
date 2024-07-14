import customtkinter as ctk
from core.config import Config
from core.backup import Backup
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import subprocess

class BackupApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("jbackup - James's Backup Utility")
        self.geometry("700x600")

        self.config = Config()
        self.backup = Backup(self.config)

        self.create_widgets()

    def create_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(8, weight=1)

        # Source selection
        ctk.CTkLabel(main_frame, text="Backup Source:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.source_entry = ctk.CTkEntry(main_frame)
        self.source_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(main_frame, text="Browse", command=self.browse_source).grid(row=0, column=2, padx=5, pady=5)

        # Destination selection
        ctk.CTkLabel(main_frame, text="Backup Destination:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.dest_entry = ctk.CTkEntry(main_frame)
        self.dest_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(main_frame, text="Browse", command=self.browse_destination).grid(row=1, column=2, padx=5, pady=5)

        # Scheduling options
        ctk.CTkLabel(main_frame, text="Backup Schedule:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.schedule_var = ctk.StringVar(value="daily")
        schedule_options = ctk.CTkOptionMenu(main_frame, variable=self.schedule_var, values=["daily", "weekly", "monthly"])
        schedule_options.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Remote backup options
        self.remote_var = ctk.BooleanVar(value=False)
        remote_check = ctk.CTkCheckBox(main_frame, text="Enable Remote Backup", variable=self.remote_var, command=self.toggle_remote_options)
        remote_check.grid(row=3, column=0, padx=5, pady=5, sticky="w")

        self.remote_frame = ctk.CTkFrame(main_frame)
        self.remote_frame.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
        self.remote_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self.remote_frame, text="Remote Host:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.remote_host_entry = ctk.CTkEntry(self.remote_frame)
        self.remote_host_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(self.remote_frame, text="Remote Path:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.remote_path_entry = ctk.CTkEntry(self.remote_frame)
        self.remote_path_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(self.remote_frame, text="Explore", command=self.explore_remote).grid(row=1, column=2, padx=5, pady=5)

        ctk.CTkLabel(self.remote_frame, text="Delete backups older than:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.delete_older_entry = ctk.CTkEntry(self.remote_frame)
        self.delete_older_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        ctk.CTkLabel(self.remote_frame, text="days").grid(row=2, column=2, padx=5, pady=5, sticky="w")

        self.remote_frame.grid_remove()  # Hide remote options by default

        # Save and Backup buttons
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
        button_frame.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(button_frame, text="Save Configuration", command=self.save_config).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(button_frame, text="Start Backup", command=self.start_backup).grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(main_frame)
        self.progress_bar.grid(row=6, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
        self.progress_bar.set(0)

        self.progress_label = ctk.CTkLabel(main_frame, text="")
        self.progress_label.grid(row=7, column=0, columnspan=3, padx=10, pady=5)

        self.load_config()

    def load_config(self):
        self.source_entry.insert(0, self.config.get("backup.source", ""))
        self.dest_entry.insert(0, self.config.get("backup.destination", ""))
        self.schedule_var.set(self.config.get("backup.schedule", "daily"))
        self.remote_var.set(self.config.get("remote.enabled", False))
        self.remote_host_entry.insert(0, self.config.get("remote.host", ""))
        self.remote_path_entry.insert(0, self.config.get("remote.path", ""))
        self.delete_older_entry.insert(0, str(self.config.get("remote.delete_older_than", 30)))
        self.toggle_remote_options()

    def toggle_remote_options(self):
        if self.remote_var.get():
            self.remote_frame.grid()
        else:
            self.remote_frame.grid_remove()

    def browse_source(self):
        folder = filedialog.askdirectory()
        if folder:
            self.source_entry.delete(0, ctk.END)
            self.source_entry.insert(0, folder)

    def browse_destination(self):
        folder = filedialog.askdirectory()
        if folder:
            self.dest_entry.delete(0, ctk.END)
            self.dest_entry.insert(0, folder)

    def explore_remote(self):
        host = self.remote_host_entry.get()
        path = self.remote_path_entry.get()
        if not host:
            messagebox.showerror("Error", "Please enter a remote host.")
            return
        
        try:
            result = subprocess.run(['ssh', host, f'ls -l {path}'], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                self.show_remote_files(result.stdout)
            else:
                messagebox.showerror("Error", f"Failed to explore remote directory:\n{result.stderr}")
        except subprocess.TimeoutExpired:
            messagebox.showerror("Error", "Connection to remote host timed out.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def show_remote_files(self, file_list):
        file_window = ctk.CTkToplevel(self)
        file_window.title("Remote Files")
        file_window.geometry("500x400")

        text_widget = ctk.CTkTextbox(file_window)
        text_widget.pack(expand=True, fill="both")
        text_widget.insert(ctk.END, file_list)
        text_widget.configure(state="disabled")

    def save_config(self):
        self.config.set_source(self.source_entry.get())
        self.config.set_destination(self.dest_entry.get())
        self.config.set_schedule(self.schedule_var.get())
        self.config.set_remote_enabled(self.remote_var.get())
        self.config.set_remote_host(self.remote_host_entry.get())
        self.config.set_remote_path(self.remote_path_entry.get())
        
        try:
            delete_older = int(self.delete_older_entry.get())
            self.config.set_delete_older_than(delete_older)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of days for deleting old backups.")
            return

        self.config.save_config()
        messagebox.showinfo("Success", "Configuration saved successfully!")

    def start_backup(self):
        source = self.source_entry.get()
        destination = self.dest_entry.get()

        if not source or not destination:
            messagebox.showerror("Error", "Please select both source and destination folders.")
            return

        self.backup.set_source(source)
        self.backup.set_destination(destination)

        if self.remote_var.get():
            self.backup.set_remote(f"{self.remote_host_entry.get()}:{self.remote_path_entry.get()}")
            try:
                delete_older = int(self.delete_older_entry.get())
                self.backup.set_delete_older_than(delete_older)
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number of days for deleting old backups.")
                return

        self.progress_bar.set(0)
        self.progress_label.configure(text="Starting backup...")

        try:
            self.backup.start(progress_callback=self.update_progress)
            messagebox.showinfo("Success", "Backup completed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during backup: {str(e)}")

    def update_progress(self, progress, status):
        self.progress_bar.set(progress)
        self.progress_label.configure(text=status)
        self.update_idletasks()

def main():
    app = BackupApp()
    app.mainloop()

if __name__ == "__main__":
    main()