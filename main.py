from tkinter import *
from datetime import *
from tkinter.scrolledtext import ScrolledText
import pandas as pd
import openpyxl as op

class App(Tk):
    # df = pd.read_excel("RunLog.xlsx") 

    def __init__(self):
        Tk.__init__(self)
        self.title('Running Log App')

        # Date label and input
        self.date_label = Label(self, text="Date (m/d/yyyy):")
        self.date_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.date_input = StringVar()
        self.date_entry = Entry(self, width=30, textvariable=self.date_input)
        self.date_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Run type label with road and trail run selections 
        self.run_type_label = Label(self, text="Run Type:")
        self.run_type_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        self.road_select = Radiobutton(self, width=10, text="Road", value="road")
        self.road_select.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.trail_select = Radiobutton(self, width=10, text="Trail", value="trail")
        self.trail_select.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

        # Hours label and input
        self.hours_label = Label(self, text="Hours")
        self.hours_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")

        self.hours_input = IntVar()
        self.hours_entry = Entry(self, width=30, textvariable=self.hours_input)
        self.hours_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        # Minutes label and input
        self.minutes_label = Label(self, text="Minutes:")
        self.minutes_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")

        self.minutes_input = IntVar()
        self.minutes_entry = Entry(self, width=30, textvariable=self.minutes_input)
        self.minutes_entry.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        # Seconds label and input
        self.seconds_label = Label(self, text="Seconds:")
        self.seconds_label.grid(row=4, column=0, padx=10, pady=10, sticky="e")

        self.seconds_input = IntVar()
        self.seconds_entry = Entry(self, width=30, textvariable=self.seconds_input)
        self.seconds_entry.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

        # Miles label and input 
        self.miles_label = Label(self, text="Miles:")
        self.miles_label.grid(row=5, column=0, padx=10, pady=10, sticky="e")

        self.miles_input = float()
        self.miles_entry = Entry(self, width=30, textvariable=self.miles_input)
        self.miles_entry.grid(row=5, column=1, padx=10, pady=10, sticky="ew")

        # Insert new data button
        self.insert_button = Button(self, text="New Data", command=self.input_data)
        self.insert_button.grid(row=7, column=1, padx=10, pady=10, sticky="w")

        # Edit data button
        self.insert_button = Button(self, text="Edit", command=self.edit_the_data)
        self.insert_button.grid(row=7, column=2, padx=10, pady=10, sticky="w")
        
        # Delete data button
        self.delete_button = Button(self, text="Delete", command=self.delete_row)
        self.delete_button.grid(row=7, column=3, padx=10, pady=10, sticky="w")

        # Scrolled text widget for calculations 
        self.calculations_text = ScrolledText(self, width=100, height=10)
        self.calculations_text.grid(row=9, column=0, columnspan=10, padx=10, pady=10,)

        # Scrolled text widget for displaying excel spreadsheet
        self.excel_text = ScrolledText(self, width=100, height=30)
        self.excel_text.grid(row=10, column=0, columnspan=10, padx=10, pady=10,)


    # Add new row of data
    def input_data(self):
        df = pd.read_excel("RunLog.xlsx") 

        # User inputs with error handling
        date_str = self.date_input.get()
        try:
            # Convert date string into date object (has time)
            datetime_object = datetime.strptime(date_str, "%m/%d/%Y")

            # Extract just the date part to get a pure date object
            date = datetime_object.date()
        except ValueError:
            date_str = input("ERROR! Enter  valid date (M/D/YYYY): ")
            datetime_object = datetime.strptime(date_str, "%m/%d/%Y") 
            date = datetime_object.date()

        run_type = input("Enter run as \"road\" or \"trail\": ")
        if run_type != "road" or run_type != "trail":
            run_type = input("ERROR! Enter run as \"road\" or \"trail\": ")

        try:
            hours = self.hours_input.get()
        except ValueError:
            hours = int(input("ERROR! Enter number of hours: "))

        try:
            minutes = self.minutes_input.get()
        except ValueError:
            minutes = int(input("ERROR! Enter number of minutes: "))

        try:
            seconds = self.seconds_input.get()
        except ValueError:
            seconds = int(input("ERROR! Enter number of seconds: "))

        try:
            miles = self.miles_input()
        except ValueError:
            miles = float(input("ERROR! Enter number of miles: "))

        # Calculating pace
        convert_seconds = seconds / 60
        convert_hours = hours * 60
        total_minutes = minutes + convert_seconds + convert_hours
        pace = total_minutes / miles

        # Creating new row of data based on user inputs
        new_row = pd.DataFrame({'Date': [date], 'Run Type': [run_type], 'Hours': [hours], 'Minutes': [minutes], 'Seconds': [seconds], 'Miles': [miles], 'Pace':[pace]})

        # Adding new row 
        df = pd.concat([df, new_row], ignore_index=True)

        # Sends new row to excel spreadsheet
        df.to_excel("RunLog.xlsx", index=False)


    # Edit data
    def edit_the_data():
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


    # Delete row
    def delete_row():
        df = pd.read_excel("RunLog.xlsx") 

        # User inputting what row to delete
        index_input = int(input("Enter index to delete: "))

        # Delete row base on index
        df.drop([index_input], inplace=True)

        # Sends edit to excel spreadsheet
        df.to_excel("RunLog.xlsx", index=False)


if __name__ == "__main__":
    app = App()
    app.mainloop()