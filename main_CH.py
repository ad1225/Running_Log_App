from tkinter import *
from tkcalendar import Calendar # pip install tkcalendar
from tkinter import ttk
from datetime import *
from tkinter.scrolledtext import ScrolledText
import pandas as pd
import openpyxl as op
from tkinter import messagebox
class App(Tk):
    # df = pd.read_excel("RunLog.xlsx") 

    def __init__(self):
        Tk.__init__(self)
        self.title('Running Log App')

        # Date label and input
        self.date_label = Label(self, text="Date (mm/dd/yyyy):")
        self.date_label.grid(row=1, column=3, padx=10, pady=10, sticky="e", columnspan=1)
        self.date_label.grid_configure(ipadx=50, ipady=10)  # center label

        # get the current year, month, and day and select it in the calendar
        current_year = datetime.now().year
        current_month = datetime.now().month
        current_day = datetime.now().day

        '''
        self.date_input = StringVar()
        self.date_entry = Entry(self, width=30, textvariable=self.date_input)
        self.date_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        '''
        self.date_entry = Calendar(self, selectmode="day", font="Arial 7",
            locale="en_US", year=current_year, month=current_month, day=current_day, date_pattern="M/D/YYYY")
        self.date_entry.grid(row=2, rowspan=4, column=3, padx=10, pady=10, sticky="nsew")

        # Run type label with road and trail run selections
        
        self.run_type_label = Label(self, text="Run Type:")
        self.run_type_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        self.radio_value = StringVar() # holds the value of the selected radio button
        # CH neede to add the variable attribute to the Radiobuttons
        self.road_select = Radiobutton(self, width=10, text="Road",  variable=self.radio_value, value="road") 
        self.road_select.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.road_select.select() # on at start
        self.trail_select = Radiobutton(self, width=10, text="Trail", variable=self.radio_value, value="trail")
        self.trail_select.grid(row=1, column=2, padx=10, pady=10, sticky="ew")
        self.trail_select.deselect() # off at start
        self.trail_select.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

        # Hours label and input
        
        self.hours_label = Label(self, text="Hours")
        self.hours_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        
        #self.hours_input = IntVar()
        #self.hours_entry = Entry(self, width=30, textvariable=self.hours_input)
        self.hours_label = Label(self, text="Hours")
        self.hours_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        
        self.hours_input = IntVar()
        self.hours_entry = Scale(self, from_=0, to=23, orient=HORIZONTAL, length=200, variable=self.hours_input)
        self.hours_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        # Minutes label and input
        self.minutes_label = Label(self, text="Minutes:")
        self.minutes_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")

        self.minutes_input = IntVar()
        self.minutes_entry = Scale(self, from_=0, to=59, orient=HORIZONTAL, length=200, variable=self.minutes_input)
        self.minutes_entry.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        # Seconds label and input
        self.seconds_label = Label(self, text="Seconds:")
        self.seconds_label.grid(row=4, column=0, padx=10, pady=10, sticky="e")

        self.seconds_input = IntVar()
        self.seconds_entry = Scale(self, from_=0, to=59, orient=HORIZONTAL, length=200, variable=self.seconds_input)
        self.seconds_entry.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

        # Miles label and input 
        self.miles_label = Label(self, text="Miles:")
        self.miles_label.grid(row=5, column=0, padx=10, pady=10, sticky="e")

        self.miles_input = DoubleVar()
        self.miles_entry = Scale(self, from_=0.1, to=30, resolution=0.1, orient=HORIZONTAL, length=200)
        self.miles_entry.grid(row=5, column=1, padx=10, pady=10, sticky="ew")

        # Insert new data button
        self.insert_button = Button(self, text="Add to table", command=self.input_data)
        self.insert_button.grid(row=7, column=1, padx=10, pady=10, sticky="w")

        # CH change this to save table b/c editing will always be "on" in the treeview
        self.save_table_button = Button(self, text="Save Table", command=self.save_table)
        self.save_table_button.grid(row=7, column=2, padx=10, pady=10, sticky="w")
        
        # Delete data button
        self.delete_button = Button(self, text="Delete Selected Row", command=self.delete_row)
        self.delete_button.grid(row=7, column=3, padx=10, pady=10, sticky="w")

        # Scrolled text widget for calculations 
        self.calculations_text = ScrolledText(self, width=100, height=10)
        self.calculations_text.grid(row=9, column=0, columnspan=5, padx=10, pady=10,)

        # Scrolled text widget for displaying excel spreadsheet
        #self.excel_text = ScrolledText(self, width=100, height=30)
        #self.excel_text.grid(row=10, column=0, columnspan=10, padx=10, pady=10,)

        # make df an attribute that we keep around and only save after new data is added
        # or cells were edited (also maybe on app quit?)
        self.df = pd.read_excel("RunLog.xlsx")

        # Create a Treeview widget
        self.tree = ttk.Treeview(self, columns=list(self.df.columns), show='headings')
        self.tree.grid(row=10, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")
        self.current_cell = None  # Initialize the current cell reference

        # Bind single click event to edit cells
        self.tree.bind("<Button-1>", self.edit_cell)

        # Define columns
        for col in self.df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        # Insert data into the treeview
        for index, row in self.df.iterrows():
            self.tree.insert("", "end", values=list(row))


    # Add new row of data
    def input_data(self):
        #df = pd.read_excel("RunLog.xlsx") # moved to init

        # User inputs with error handling
        date_str = self.date_entry.get_date() # from calendar widget
        date = datetime.strptime(date_str, "%m/%d/%Y").date()

        # convert into a date object using "%m/%d/%Y"


        # CH with the calender widget the date is always in the M/D/YYYY format 
        # so no need to check for that
        #try:
        #    # Convert date string into date object (has time)
        #    datetime_object = datetime.strptime(date_str, "%m/%d/%Y")
        #
        #   # Extract just the date part to get a pure date object
        #    date = datetime_object.date()
        #except ValueError:
        #    date_str = messagebox.askstring("Invalid Date", "ERROR! Enter a valid date (M/D/YYYY):")


        run_type = self.radio_value.get()   # need to use radio_value.get() to get the selected value
        # CH not needed as your are guaranteed to get a either "road" or "trail"
        #if run_type != "road" or run_type != "trail":
        #    messagebox.showerror("Invalid Run Type", "ERROR! Enter run as \"road\" or \"trail\"")

        # CH no validation needed as the sliders will only return into in the correct range
        #try:
        hours = int(self.hours_entry.get()) # needed to be hours_entry not hours_input!
        #    if hours < 0 or hours > 24: raise ValueError # so we can catch it below with the same error message
        #except ValueError:
        #        messagebox.showerror("Invalid Input", "ERROR! Enter 0 to 24")
        #        return # need to bail out as we can't do math with an invalid value later!

        #try:
        minutes = int(self.minutes_entry.get())
        #    if minutes < 0 or minutes > 60: raise ValueError
        #except ValueError:
        #    messagebox.showerror("Invalid Input", "ERROR! Enter 0 to 60")
        #    return

        #try:
        seconds = int(self.seconds_entry.get())
        #    if seconds < 0 or seconds > 60: raise ValueError
        #except ValueError:
        #    messagebox.showerror("Invalid Input", "ERROR! Enter 0 to 60")
        #    return

        # again not needed as the slider will only return a float 0 to 30
        #try:
        miles = float(self.miles_entry.get())
        #    if miles < 0 or miles > 30: raise ValueError
        #except ValueError:
        #    messagebox.showerror("Invalid Input", "ERROR! Enter 0.1 to 30") # I assume 30 miles is a good max?
        #    return

        # Calculating pace
        convert_seconds = seconds / 60
        convert_hours = hours * 60
        total_minutes = minutes + convert_seconds + convert_hours
        pace = round(total_minutes / miles, 2) # miles must never be 0!

        # Creating new row of data based on user inputs
        new_row = pd.DataFrame({'Date': [date], 'Run Type': [run_type], 'Hours': [hours], 'Minutes': [minutes], 'Seconds': [seconds], 'Miles': [miles], 'Pace':[pace]})

        # Adding new row 
        self.df = pd.concat([self.df, new_row], ignore_index=True)

        # append data into the treeview
        self.tree.insert("", "end", values=list(new_row.iloc[0]))

        # Sends new row to excel spreadsheet
        self.df.to_excel("RunLog.xlsx", index=False)

    def edit_cell(self, event):
        '''handles editing and validating of a cell'''

        # Identify the row and column clicked
        row_id = self.tree.identify_row(event.y)
        column_id = self.tree.identify_column(event.x)

        if row_id == "" or column_id == "": return  # Click is not on a cell but on the header

        # Destroy the current entry widget if it exists
        # this prevents the user from creating multiple entry widgets
        if self.current_cell is not None:
            self.current_cell.destroy()
            self.current_cell = None  # Reset the reference

        # Calculate the x position of the column
        x = self.tree.bbox(row_id, column=column_id)[0]

        # Calculate the y position of the row
        y = self.tree.bbox(row_id)[1]

        # Get the width of the column
        width = self.tree.column(column_id, width=None)

        # Assuming a fixed height for the Entry widget
        height = 20  # This should be adjusted based on your UI

        # Create and place the Entry widget
        self.current_cell = Entry(self.tree)
        current_value = self.tree.item(row_id, "values")[int(column_id[1:]) - 1]
        self.current_cell.insert(0, current_value)
        self.current_cell.place(x=x, y=y, width=width, height=height)

        # Bind the entry widget to update the value on Enter key press
        col_name = self.tree.heading(column_id)['text']
        self.current_cell.bind("<Return>", lambda e: self.update_value(self.current_cell, row_id, col_name))

        # Set focus to the Entry widget
        self.current_cell.focus_set()

    def update_value(self, entry, row, col_name):
        new_value = entry.get()

        # verify the new value
        if col_name == 'Run Type':
            if new_value not in ['road', 'trail']:
                messagebox.showerror("Invalid Run Type", "Must be road or trail")
                entry.destroy()
                return
        elif col_name == 'Hours':
            if new_value < 0 or new_value > 24:
                messagebox.showerror("Invalid Hour value", "Must be 0 - 24")
                entry.destroy()
                return

        # TODO: add more validations for other columns

        # Update the treeview
        self.tree.set(row, col_name, new_value)
        
        # Update the DataFrame
        row_index = self.tree.index(row)
        self.df.at[row_index, col_name] = new_value
        
        # Destroy the entry widget
        entry.destroy()

    # Edit data

    def save_table(self):
        # Destroy the current cell edit entry widget if it exists
        if self.current_cell is not None: 
            self.current_cell.destroy()
            self.current_cell = None  # Reset the reference
        self.df.to_excel("RunLog.xlsx", index=False)



    

    '''
    def edit_the_data(self): # Ch missing self
        df = pd.read_excel("RunLog.xlsx") 

        # User inputting what row and column to make edits in 
        index_input = int(input("Enter index to edit: "))
        select_column = input("Enter column name to edit: ")
    
        # Depending on column, will convert user input to correct data type
        if select_column == "Date":
            user_edit = input("Enter new data: ")
            
            # Convert date string into date object (has time)
            datetime_object = datetime.strptime(user_edit, "%m/%d/%Y")

            # Extract just the date part to get a pure date object
            date = datetime_object.date()

            # Changes the data at the selected index and column
            df.at[index_input, select_column] = date
        elif select_column == "Run Type":
            user_edit = input("Enter new data: ")

            # Changes the data at the selected index and column
            df.at[index_input, select_column] = user_edit
        elif select_column == "Miles":
            df.at[index_input, 'Miles'] = None
            user_edit = float(input("Enter new data: "))

            # Changes the data at the selected index and column
            df.at[index_input, select_column] = user_edit

            # Recalculating pace
            convert_seconds = df.loc[index_input].at["Seconds"] / 60
            convert_hours = df.loc[index_input].at["Hours"] * 60
            total_minutes = df.loc[index_input].at["Minutes"] + convert_seconds + convert_hours
            pace = total_minutes / df.loc[index_input].at["Miles"]

            df.at[index_input, "Pace"] = pace

        else:
            user_edit = int(input("Enter new data: "))

            # Changes the data at the selected index and column
            df.at[index_input, select_column] = user_edit

            # Recalculating pace
            convert_seconds = df.loc[index_input].at["Seconds"] / 60
            convert_hours = df.loc[index_input].at["Hours"] * 60
            total_minutes = df.loc[index_input].at["Minutes"] + convert_seconds + convert_hours
            pace = total_minutes / df.loc[index_input].at["Miles"]

            df.at[index_input, "Pace"] = pace

        # Sends edit to excel spreadsheet
        df.to_excel("RunLog.xlsx", index=False)
    '''

    # Delete row
    def delete_row(self):
        #f = pd.read_excel("RunLog.xlsx") 

        # User inputting what row to delete
        #index_input = int(input("Enter index to delete: "))

        # Selecting a row must be done by selecting a cell to edit
        # so we remove that edit entry widget if it exists
        # this is also a good check for when no row is selected
        if self.current_cell is not None:
            self.current_cell.destroy()
            self.current_cell = None

            # Get current active row from Treeview
            row_str  = self.tree.selection()[0] # sth like 'I003' for row 3
            index_input = int(row_str[1:]) - 1

            # Eliminate the row from the Treeview
            self.tree.delete(row_str)        

            # Delete row base on index
            self.df.drop([index_input], inplace=True)

            # Sends edit to excel spreadsheet
            self.df.to_excel("RunLog.xlsx", index=False)


if __name__ == "__main__":
    app = App()
    app.mainloop()