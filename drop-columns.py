#Developed by ODAT project
#please see https://odat.info
#please see https://github.com/ODAT-Project
import pandas as pd
from tkinter import Tk, filedialog, messagebox, Toplevel, Listbox, Button, MULTIPLE

class DropColumnsApp:
    def __init__(self, root):
        self.root = root
        #enlarge gui window size
        self.root.geometry("400x250")
        self.root.title("Drop Columns from CSV")

        #create select file button
        self.select_file_btn = Button(self.root, text="Select CSV File", command=self.select_file)
        self.select_file_btn.pack(pady=10)

        #create select columns button
        self.drop_columns_btn = Button(self.root, text="Select Columns to Drop", command=self.select_columns)
        self.drop_columns_btn.pack(pady=10)
        self.drop_columns_btn.config(state="disabled")

        #create about button
        self.about_btn = Button(self.root, text="About", command=self.show_about)
        self.about_btn.pack(pady=10)

        self.selected_file = None
        self.columns = []

    def select_file(self):
        #ask user to select a file
        self.selected_file = filedialog.askopenfilename(
            title="Select a CSV File",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )

        if not self.selected_file:
            messagebox.showinfo("no file selected", "please select a csv file.")
        else:
            try:
                #load the csv file
                df = pd.read_csv(self.selected_file)
                self.columns = list(df.columns)
                messagebox.showinfo("file loaded", f"loaded file: {self.selected_file}")

                #enable the select columns button
                self.drop_columns_btn.config(state="normal")

            except Exception as e:
                #handle errors
                messagebox.showerror("error", f"an error occurred while loading the file: {e}")

    def select_columns(self):
        #check if columns list is empty
        if not self.columns:
            messagebox.showerror("error", "no columns found. please load a csv file first.")
            return

        #create a new window for column selection
        column_window = Toplevel(self.root)
        column_window.title("Select Columns to Drop")

        listbox = Listbox(column_window, selectmode=MULTIPLE, width=50, height=15)
        listbox.pack(pady=10)

        #populate the listbox with column names
        for col in self.columns:
            listbox.insert("end", col)

        def drop_selected_columns():
            #get selected indices
            selected_indices = listbox.curselection()
            columns_to_drop = [self.columns[i] for i in selected_indices]

            if not columns_to_drop:
                messagebox.showwarning("no columns selected", "please select at least one column to drop.")
                return

            try:
                #load the original csv file
                df = pd.read_csv(self.selected_file)

                #drop the selected columns
                df = df.drop(columns=columns_to_drop)

                #ask user where to save new file
                save_path = filedialog.asksaveasfilename(
                    title="Save New CSV File",
                    defaultextension=".csv",
                    filetypes=[("CSV Files", "*.csv")]
                )

                if save_path:
                    #save the new csv file
                    df.to_csv(save_path, index=False)
                    messagebox.showinfo("success", f"new csv saved to {save_path}")
                    column_window.destroy()

            except Exception as e:
                #handle errors
                messagebox.showerror("error", f"an error occurred: {e}")

        #create drop columns button
        drop_btn = Button(column_window, text="Drop Selected Columns", command=drop_selected_columns)
        drop_btn.pack(pady=10)

    def show_about(self):
        #display about information
        messagebox.showinfo("About", "Drop Columns from CSV \nDeveloped by ODAT project.")

if __name__ == "__main__":
    root = Tk()
    app = DropColumnsApp(root)
    root.mainloop()
