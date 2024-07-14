import customtkinter as ctk
from core.config import Config
from core.backup import Backup
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox

class BackupApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("jbackup - James's Backup Utility")
        self.geometry("600x400")

        self.config = Config()
        self.backup = Backup(self.config)

        self.create_widgets()

    def create_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(3, weight=1)

        # Source selection
        source_frame = ctk.CTkFrame(main_frame)
        source_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        ctk.CTkLabel(source_frame, text="Backup Source:").grid(row=0, column=0, padx=5, pady=5)
        self.source_entry = ctk.CTkEntry(source_frame)
        self.source_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(source_frame, text="Browse", command=self.browse_source).grid(row=0, column=2, padx=5, pady=5)

        # Destination selection
        dest_frame = ctk.CTkFrame(main_frame)
        dest_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        
        ctk.CTkLabel(dest_frame, text="Backup Destination:").grid(row=0, column=0, padx=5, pady=5)
        self.dest_entry = ctk.CTkEntry(dest_frame)
        self.dest_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(dest_frame, text="Browse", command=self.browse_destination).grid(row=0, column=2, padx=5, pady=5)

        # Backup button
        ctk.CTkButton(main_frame, text="Start Backup", command=self.start_backup).grid(row=2, column=0, padx=10, pady=10)

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(main_frame)
        self.progress_bar.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        self.progress_bar.set(0)

        self.progress_label = ctk.CTkLabel(main_frame, text="")
        self.progress_label.grid(row=4, column=0, padx=10, pady=5)

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

    def start_backup(self):
        source = self.source_entry.get()
        destination = self.dest_entry.get()

        if not source or not destination:
            messagebox.showerror("Error", "Please select both source and destination folders.")
            return

        self.backup.set_source(source)
        self.backup.set_destination(destination)

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