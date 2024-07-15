import tkinter as tk
from tkinter import filedialog
import pandas as pd


class File_app(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("400x200")

         # Bind the close event so we can save the current DataFrame
        self.protocol("WM_DELETE_WINDOW", self.save_on_close)

        self.load_button = tk.Button(self, text="Load XLSX", command=self.load_xlsx)
        self.load_button.grid(row=0, column=0, padx=10, pady=20)
        self.save_button = tk.Button(self, text="Save XLSX", command=self.save_xlsx)
        self.save_button.grid(row=0, column=1, padx=10, pady=20)
        self.save_as_button = tk.Button(self, text="Save As XLSX", command=self.save_as_xlsx)
        self.save_as_button.grid(row=0, column=2, padx=10, pady=20)

        self.current_file = None # no file is currently loaded
        self.df = None # no DataFrame is currently loaded

    def save_xlsx(self):
        # save the current DataFrame to an XLSX file
        if self.current_file:
            self.df.to_excel(self.current_file, index=False)
            print(f"Saved {self.current_file}")

    def save_as_xlsx(self):
        if self.current_file:
            # Save the current DataFrame to a new XLSX file
            file_path = filedialog.asksaveasfilename(filetypes=[("XLSX files", "*.xlsx")])
            if file_path:
                # Ensure the file path ends with '.xlsx'
                if not file_path.endswith('.xlsx'):
                    file_path += '.xlsx'
                self.current_file = file_path
                self.df.to_excel(file_path, index=False)
                print(f"Saved {self.current_file}")

    def load_xlsx(self):
        # Open a dialog to select the XLSX file
        file_path = filedialog.askopenfilename(filetypes=[("XLSX files", "*.xlsx")])
        if file_path:  # If a file was selected
            self.current_file = file_path # Save the file path for future reference
            # Load the XLSX file into a DataFrame
            self.df = pd.read_excel(file_path)
            # For demonstration, print the DataFrame to the console
            print(self.df)

    # when app is closed, save the current DataFrame to the current file
    def save_on_close(self):
        if self.current_file:
            self.df.to_excel(self.current_file, index=False)
            print(f"Saved {self.current_file}")
        self.destroy()

             
if __name__ == "__main__":
    app = File_app()
    app.mainloop()