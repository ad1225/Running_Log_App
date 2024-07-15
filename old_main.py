from tkinter import *
from datetime import *
from tkinter.scrolledtext import ScrolledText
import pandas as pd
import openpyxl as op

class App(Tk):
    df = pd.read_excel("RunLog.xlsx") 

    def __init__(self):
        Tk.__init__(self)
        self.title('Running Log App')

        # Index label and input
        self.index_label = Label(self, text="Index (ONLY to Edit or Delete):")
        self.index_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.index_user_input = IntVar()
        self.index_entry = Entry(self, width=30, textvariable=self.index_user_input)
        self.index_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Columns label and drop down menu selection
        self.col_label = Label(self, text="Select column (ONLY to Edit data):")
        self.col_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        col_name = StringVar()
        self.col = OptionMenu(self, col_name, "Date", "Run Type", "Hours", "Minutes", "Seconds", "Miles")
        self.col.grid(row=1, column=1, padx=10, pady=10, sticky="e")

        # Date label and input
        self.date_label = Label(self, text="Date (M/D/YYYY):")
        self.date_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")

        self.date_input = StringVar()
        self.date_entry = Entry(self, width=30, textvariable=self.date_input)
        self.date_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        # Run type label with road and trail run radio button selections 
        self.run_type_label = Label(self, text="Run Type (select one):")
        self.run_type_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        
        self.run_select = StringVar()
        self.road_select = Radiobutton(self, width=10, text="Road", variable=self.run_select, value="road")
        self.road_select.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        self.trail_select = Radiobutton(self, width=10, text="Trail", variable=self.run_select, value="trail")
        self.trail_select.grid(row=3, column=2, padx=10, pady=10, sticky="ew")

        # Hours label and input
        self.hours_label = Label(self, text="Hours")
        self.hours_label.grid(row=4, column=0, padx=10, pady=10, sticky="e")

        self.hours_input = IntVar()
        self.hours_entry = Entry(self, width=30, textvariable=self.hours_input)
        self.hours_entry.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

        # Minutes label and input
        self.minutes_label = Label(self, text="Minutes:")
        self.minutes_label.grid(row=5, column=0, padx=10, pady=10, sticky="e")

        self.minutes_input = IntVar()
        self.minutes_entry = Entry(self, width=30, textvariable=self.minutes_input)
        self.minutes_entry.grid(row=5, column=1, padx=10, pady=10, sticky="ew")

        # Seconds label and input
        self.seconds_label = Label(self, text="Seconds:")
        self.seconds_label.grid(row=6, column=0, padx=10, pady=10, sticky="e")

        self.seconds_input = IntVar()
        self.seconds_entry = Entry(self, width=30, textvariable=self.seconds_input)
        self.seconds_entry.grid(row=6, column=1, padx=10, pady=10, sticky="ew")

        # Miles label and input 
        self.miles_label = Label(self, text="Miles:")
        self.miles_label.grid(row=7, column=0, padx=10, pady=10, sticky="e")

        self.miles_input = DoubleVar()
        self.miles_entry = Entry(self, width=30, textvariable=self.miles_input)
        self.miles_entry.grid(row=7, column=1, padx=10, pady=10, sticky="ew")

        # Insert new data button
        self.insert_button = Button(self, text="Submit New Data", command=self.input_data)
        self.insert_button.grid(row=8, column=1, padx=10, pady=10, sticky="w")

        # Edit data button
        self.insert_button = Button(self, text="Submit Edited Data", command=self.edit_the_data)
        self.insert_button.grid(row=8, column=2, padx=10, pady=10, sticky="w")
        
        # Delete data button
        self.delete_button = Button(self, text="Delete Selected Row", command=self.delete_row)
        self.delete_button.grid(row=8, column=3, padx=10, pady=10, sticky="w")

        # Scrolled text widget for calculations 
        self.calculations_text = ScrolledText(self, width=100, height=10)
        self.calculations_text.grid(row=12, column=0, columnspan=10, padx=10, pady=10,)
        # self.calculations_text.insert()

        # Scrolled text widget for displaying excel spreadsheet
        self.excel_text = ScrolledText(self, width=100, height=20)
        self.excel_text.grid(row=14, column=0, columnspan=10, padx=10, pady=10,)
        self.excel_text.insert(END, self.df)

    # FIXME: FIGURE OUT HOW TO BETTER HANDLE UESR ERROR
    # Add new row of data
    def input_data(self):
        # User inputs with error handling
        try:
            date_str = self.date_input.get()

            # Convert date string into date object (has time)
            datetime_object = datetime.strptime(date_str, "%m/%d/%Y")

            # Extract just the date part to get a pure date object
            date = datetime_object.date()
        except ValueError:
            print("ERROR! Enter valid date (M/D/YYYY)")
            datetime_object = datetime.strptime(date_str, "%m/%d/%Y")
            date = datetime_object.date()

        run_type = self.run_select.get()

        try:
            hours = self.hours_input.get()
        except ValueError:
            print("ERROR! Enter number of hours")

        try:
            minutes = self.minutes_input.get()
        except ValueError:
            print("ERROR! Enter number of minutes")

        try:
            seconds = self.seconds_input.get()
        except ValueError:
            print("ERROR! Enter number of seconds")

        try:
            miles = self.miles_input.get()
        except ValueError:
            print("ERROR! Enter number of miles")

        # Calculating pace
        convert_seconds = seconds / 60
        convert_hours = hours * 60
        total_minutes = minutes + convert_seconds + convert_hours
        pace = total_minutes / miles

        # Creating new row of data based on user inputs
        new_row = pd.DataFrame({'Date': [date], 'Run Type': [run_type], 'Hours': [hours], 'Minutes': [minutes], 'Seconds': [seconds], 'Miles': [miles], 'Pace':[pace]})

        # Adding new row 
        self.df = pd.concat([self.df, new_row], ignore_index=True)

        # Sends new row to excel spreadsheet
        self.df.to_excel("RunLog.xlsx", index=False)
        
        # Clears and diplays changes in excel textbox
        self.excel_text.delete("1.0", END)
        self.excel_text.insert(END, self.df)


    # Edit data
    def edit_the_data(self):
        index_input = self.index_user_input.get()

        # FIXME: GET THE SELECTED COLUMN NAME
        select_column = self.col.get()
    
        # Depending on column, will convert user input to correct data type
        if select_column == "Date":
            user_edit = self.date_input.get()
            
            # Convert date string into date object (has time)
            datetime_object = datetime.strptime(user_edit, "%m/%d/%Y")

            # Extract just the date part to get a pure date object
            date = datetime_object.date()

            # Changes the value at the selected index and column
            self.df.at[index_input, select_column] = date
        elif select_column == "Run Type":
            user_edit = self.run_select.get()
            self.df.at[index_input, select_column] = user_edit
        elif select_column == "Hours":
            user_edit = self.hours_input.get()
            self.df.at[index_input, select_column] = user_edit
        elif select_column == "Minutes":
            user_edit = self.minutes_input.get()
            self.df.at[index_input, select_column] = user_edit
        elif select_column == "Seconds":
            user_edit = self.seconds_input.get()
            self.df.at[index_input, select_column] = user_edit
        elif select_column == "Miles":
            self.df.at[index_input, 'Miles'] = None
            user_edit = self.miles_input.get()
            self.df.at[index_input, select_column] = user_edit

        # Recalculating pace
        convert_seconds = self.df.loc[index_input].at["Seconds"] / 60
        convert_hours = self.df.loc[index_input].at["Hours"] * 60
        total_minutes = self.df.loc[index_input].at["Minutes"] + convert_seconds + convert_hours
        pace = total_minutes / self.df.loc[index_input].at["Miles"]
        self.df.at[index_input, "Pace"] = pace

        # Sends edit to excel spreadsheet
        self.df.to_excel("RunLog.xlsx", index=False)

        # Clears and diplays changes in excel textbox
        self.excel_text.delete("1.0", END)
        self.excel_text.insert(END, self.df)


    # Delete row
    def delete_row(self):
        # User inputting what row to delete
        index_input = self.index_user_input.get()

        # Delete row base on index
        self.df.drop([index_input], inplace=True)

        # Sends edit to excel spreadsheet
        self.df.to_excel("RunLog.xlsx", index=False)

        # Clears and diplays changes in excel textbox
        self.excel_text.delete("1.0", END)
        self.excel_text.insert(END, self.df)


if __name__ == "__main__":
    app = App()
    app.mainloop()

