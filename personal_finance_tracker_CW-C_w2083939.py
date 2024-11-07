import json
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

# Constants
FILENAME = "Finance_tracker.json"

# PersonalFinanceTracker Class
class PersonalFinanceTracker(tk.Tk):
    def __init__(self, json_file_path):
        tk.Tk.__init__(self)  # Explicitly call base class constructor
        self.json_file_path = json_file_path
        self.example_data = {}
        self.title("Personal Finance Tracker")
        self.state("zoomed")  # Start in maximized state
        self.config(bg="black")
        self.create_widgets()
        self.load_json_data()

    def create_widgets(self):
        '''Function which have all the config and layouts frames'''
        title = tk.Label(self, text=" Welcome To Personal Finance Tracker ", font=('Consolas', 18, "underline"), bg="black", fg="#39FF14")
        title.pack(pady=10)  # Add some padding around the title
        try:
            self.iconphoto(True,tk.PhotoImage(file='ptr.png'))#for the tiltle icon
        except Exception as e:
            messagebox.showinfo('Title icon missing',f"Failed to load icon: {e}")
        # Search Frame
        sframe = tk.Frame(self, bg="#222222")  # Search frame with a dark background
        sframe.pack(fill='x', pady=0)

        self.search_var = tk.StringVar()  # Variable for search
        search_entry = tk.Entry(sframe, textvariable=self.search_var, font=('Consolas', 12), width=30)
        search_entry.pack(pady=10, padx=10, side='left')  # Align left with some padding

        search_button = tk.Button(sframe, text="Search", font=('Calibri', 13), command=self.search_treeview)  # Add command for search functionality
        search_button.pack(pady=10, padx=10, side='left')  # Align left with some padding

        # Entry Frame
        entry = tk.Frame(self, bg='black')  # Frame to contain all entry widgets
        entry.pack(fill='x', pady=10)

        # Transaction ID
        lbid = tk.Label(entry, text="Transaction - ID", font=('Consolas', 13, 'bold'), bg="black", fg="#39FF14")
        lbid.grid(row=0, column=0, pady=3, padx=5, sticky='w')  # Changed row and column
        entryid_var = tk.StringVar()  # Example variable, set it as needed
        entryid = tk.Entry(entry, textvariable=entryid_var, font=('Consolas', 12), width=22)
        entryid.grid(row=0, column=1, pady=3, padx=5, sticky='w')  # Changed row and column

        # Transaction Type config
        lbtype = tk.Label(entry, text="Transaction Type", font=('Consolas', 13, 'bold'), bg="black", fg="#39FF14")
        lbtype.grid(row=1, column=0, pady=3, padx=5, sticky='w')
        combotype = ttk.Combobox(entry, font=('Consolas', 12), width=20, state="readonly")  # Combo box for type
        combotype['values'] = ("Income", "Expense")  # Options for dropdown menu
        combotype.grid(row=1, column=1, pady=3, padx=5, sticky='w')

        # Amount config
        lbamount = tk.Label(entry, text="Amount \u20A8", font=('Consolas', 13, 'bold'), bg="black", fg="#39FF14")
        lbamount.grid(row=2, column=0, pady=3, padx=5, sticky='w')  
        entryamount_var = tk.StringVar()  
        entryamount = tk.Entry(entry, textvariable=entryamount_var, font=('Consolas', 12), width=22)
        entryamount.grid(row=2, column=1, pady=3, padx=5, sticky='w')  

        # Source config
        lbsource = tk.Label(entry, text="Source", font=('Consolas', 13, 'bold'), bg="black", fg="#39FF14")
        lbsource.grid(row=0, column=2, pady=3, padx=5, sticky='w')
        entrysource_var = tk.StringVar()  
        entrysource = tk.Entry(entry, textvariable=entrysource_var, font=('Consolas', 12), width=20)
        entrysource.grid(row=0, column=3, pady=3, padx=5, sticky='w')

        # Date config
        lbdate = tk.Label(entry, text="Date", font=('Consolas', 13, 'bold'), bg="black", fg="#39FF14")
        lbdate.grid(row=1, column=2, pady=3, padx=5, sticky='w')
        entrydate_var = tk.StringVar()  
        entrydate = tk.Entry(entry, textvariable=entrydate_var, font=('Consolas', 12), width=20)
        entrydate.grid(row=1, column=3, pady=3, padx=5, sticky='w')

        # Button Frame 
        btnframe = tk.Frame(entry, bg='black')  
        btnframe.grid(row=6, columnspan=200, column=0, pady=3, padx=5, sticky='w')  

       #Buttons
        btn_add = tk.Button(btnframe,command = self.message, text="Add", font=('Calibri', 13, 'bold'), width=15, bg='#16a885', fg='black', bd=0)
        btn_add.grid(row=0, column=0, sticky='w')  # Add button

        btn_dlt = tk.Button(btnframe,command = self.message, text="Delete", font=('Calibri', 13, 'bold'), width=15, bg='red', fg='black', bd=0)
        btn_dlt.grid(row=0, column=1, sticky='w', padx=10)  # Delete button

        btn_update = tk.Button(btnframe,command =self. message, text="Update", font=('Calibri', 13, 'bold'), width=15, bg='blue', fg='black', bd=0)
        btn_update.grid(row=0, column=2, sticky='w', padx=10)  # Update button

        btn_summary = tk.Button(btnframe, command = self.message,text="Summary", font=('Calibri', 13, 'bold'), width=15, bg='orange', fg='black', bd=0)
        btn_summary.grid(row=0, column=3, sticky='w', padx=10)  # Summary button
        # Treeview Style
        style = ttk.Style()
        style.configure('mystyle.Treeview', font=('Consolas', 13), rowheight=30)
        style.configure('mystyle.Treeview.Heading', font=('Consolas', 13))

        # Tree Frame
        tree_frame = tk.Frame(self, bg="pink")
        tree_frame.pack(expand=True, fill='both')

        self.table = ttk.Treeview(tree_frame, columns=(1, 2, 3, 4, 5), style='mystyle.Treeview')
        columns = ["Transaction ID", "Source", "Amount", "Transaction Type", "Date"]

        for i, col in enumerate(columns):
            self.table.heading(str(i + 1), text=col, command=lambda c=i: self.sort_treeview(c))
            self.table.column(str(i + 1), width=150)

        self.table['show'] = 'headings'
        self.table.pack(expand=True, fill='both')
    def message(self):
        messagebox.showinfo('Yet to implement',"Given for a visual layout!!!")# if any buttons are clicked it will call this function
    def load_json_data(self):
        '''Function to load json data'''
        try:
            with open(self.json_file_path, "r") as file:
                self.example_data = json.load(file)
            self.populate_treeview()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load JSON data: {str(e)}")

    def populate_treeview(self):
        '''Function to create a table view'''
        self.table.delete(*self.table.get_children())
        for category, transactions in self.example_data.items():
            for transaction in transactions:
                self.table.insert("", "end", values=(transaction["Transaction_id"],category,transaction["Amount"],transaction["Transaction_type"],transaction["Date"] ))

    def search_treeview(self):
        '''Function to search in table GUI'''
        search_term = self.search_var.get().lower()
        self.table.delete(*self.table.get_children())
        results = []

        # Search through data
        for category, transactions in self.example_data.items():
            for transaction in transactions:
                print(category)
                if search_term in str(transaction.values()).lower()or search_term in category.lower().strip():#@ if they asked why catergory not wrking
                    results.append((transaction, category))

        if not results:
            messagebox.showinfo("Search Result", "No results found.")
        else:
            for item, category in results:
                self.table.insert( "", "end", values=(item["Transaction_id"],category,item["Amount"],item["Transaction_type"],item["Date"] ))

    def sort_treeview(self, col, descending=False):
        '''Function to sort column wise'''
        print( self.table.get_children())#@
        items = [(self.table.set(child, col), child) for child in self.table.get_children()]
        print(items)
        items.sort(reverse=descending, key=lambda x: x[0])
        for index, (val, child) in enumerate(items):
            self.table.move(child, '', index)
        self.table.heading(str(col + 1), command=lambda: self.sort_treeview(col, not descending))


# FinanceTracker Class
class FinanceTracker:
    def __init__(self):#@to denote the instance
        self.transactions = self.load()#@transaction class's attribute

    def load(self):
        '''Load transactions from the JSON file'''
        try:
            with open(FILENAME, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            print(f"\t\t\t!!!File Not Found!!!\n\tCreating new file called '{FILENAME}'")
            data = {}
        except Exception as e:
            print(f"An error occurred: {e}\nResetting file '{FILENAME}', now it's empty")
            data = {}
        return data
    def bulk_read(self):
        '''Assumption - The text file which we are trying to read is also in the same folder ,where this python file is saved '''
        '''Function to add larger data of transaction'''
        while True:
            try:
                print(f"{' ' * 5}{'!' * 4}Make sure the txt file and the python programme in the same folder{'!' * 4}")
                name = input("\nGive filename for importing transaction data: ")
                name += ".txt"
                with open(name, 'r') as text:
                    lines=text.readlines()
                    if len(lines)==0:#If the text file is empty 
                        print("\t\t!!!Nothing in the text file!!!\n\t\tDirecting TO Main Menu !!!")
                        return
                    for line in lines:
                        elements = line.strip().split(',') #each line in the text assigned to elements one by one
                        if len(elements) > 4: # if more than 4 element in text file single line the programme is instruted to stop wrking and direct to main menu
                            print(f"\n\tIn Given text file line(s) has more than 4 components to unpack, which is not allowed in this programme\n\t\t\t!!!Directing to Main Menu!!!")
                            return
                        trans_type = source = amount = date = "Not-Given"  # Initialize all components of transaction to NOt-Given so if anything doesnt got value it will take Not-Given
                        for i in range(len(elements)):
                            component = elements[i].lower()
                            punc = ['-', '/', '.', ',', ':']
                            for mark in punc:
                                if mark in component:
                                    date = component.split(mark)#Assuming the date in text file is in yyyy-mm-dd or dd-mm-yyyy format
                                    if len(date[0]) == 4: # if the year part at start then following lines to get date in yyyy-mm-dd format
                                        year = date[0]
                                        month = date[1]
                                        day = date[2]
                                    elif len(date[2]) == 4:#if the year part at end then following lines to get date in yyyy-mm-dd format
                                        year = date[2]
                                        month = date[1]
                                        day = date[0]
                                    date = year + '-' + month + '-' + day  #to make sure date is given to add() in a format,wheter the format in text file is clumpsy
                                    break
                            else:
                                if component == "income" or component == "expense":
                                    trans_type = component.title()  # if trans_type is given, it will updated
                                elif component.isdigit():
                                    amount = float(component)
                                elif component.isalpha():
                                    source = component.title()
                        self.add(source, amount, trans_type, date)

                    
            except FileNotFoundError: #if txt file is not there error message will be printed
                print(" " * 15 + "!!!!File not found!!!!")
                repeat = input("\nEnter 'y' to try again |or|Press 'n' to exit: ").lower()
                if repeat == 'y':
                    continue
                elif repeat == 'n':
                    break
                else:
                    print("Not valid input to continue!!! - Directing to MainMenu")
                    break

            except Exception as e: #If error found
                print("An error occurred:", e)
            else:
                break
        return


    def dump(self):
        '''Dump transactions to the JSON file'''
        with open(FILENAME, 'w') as file:
            json.dump(self.transactions, file, indent=4)
            
    def checking(self,message, data_type, errormessage="Invalid Input, Enter a valid input!!!"):
        '''Function to do error handling for all inputs'''
        while True:
            try:
                if data_type == 1:#If it should take only input alphanumeric values
                    user = input(message)
                    user = user.replace(".", "")#If there is a decimal to make it as a digit to find digit
                    if user == '':
                        print("Cannot enter empty values!!!")
                        continue
                    elif user.isdigit():
                        print('Cannot give numeric values only,add alphabets too!!!')
                        continue
                    elif user == ' ':
                        print("Cannot enter space only!!!")
                        continue
                    return user.title()
                elif data_type == 2:#For a input which takes numeric values and alphabets
                    user = input(message)
                    if user == '':
                        print("Cannot enter empty values!!!")
                        continue
                    elif user == ' ':
                        print("Cannot enter space only!!!")
                        continue
                    return user.title()
                elif data_type == 3:#FOr input which takes only decimal values
                    user = float(input(message))
                    return user
                elif data_type == 4:#For inputs inly take whole numbers
                    user = int(input(message))
                    return user
            except ValueError:
                print(errormessage)
    def transaction_id(self):
        '''Gener a unique transaction ID'''
        high = 0
        for source, transaction_list in self.transactions.items():
            for transaction in transaction_list:
                uid = int(transaction['Transaction_id'][1:])
                if high < uid:
                    high = uid
        return f"T{str(high + 1).zfill(3)}"

    

    def new(self):
        '''Function to add transaction'''
        global transactions
        print(f"\t\t{'' * 10}New Transaction Requirements{'' * 10}\n")
        while True:
            amount = self.checking("Enter the amount \u20A8: ", 3)
            source = [(x) for x, y in self.transactions.items()]#To check ,is there any past sources
            if source:
                print("Past sources:")
                for index, item in enumerate(source, 1):
                    print(f"{index}. {item}")
                choice = self.checking("Enter the INDEX corresponding to the Past source |or| INPUT NEW SOURCE: ", 2)#User can simply give the index of the pastsource no need to type again
                if choice.isdigit() and 1 <= int(choice) <= len(source):
                    source = source[int(choice) - 1]
                else:
                    source = choice
            else:
                source = self.checking("Enter source of transaction: ", 1)#if no past transaction 

            

            while True:
                date_op = self.checking("\nTransaction date :\n1. Today's date\n2. Custom date\n\n\tChoose the index to select : ", 4)#to get a desired date
                if date_op not in [1, 2]:
                    print("Invalid option.")
                    continue
                if date_op == 1:
                    date = datetime.now().strftime("%Y-%m-%d")#it will give the current date and time
                elif date_op == 2:
                    year = self.checking("Enter year: ", 4)
                    if len(str(year)) != 4:
                        print("Invalid year, Format- YYYY")#To check format of year
                        continue
                    month = self.checking("Enter month: ", 4)#To get a valid month
                    if not 1 <= month <= 12:
                        print("Invalid month.")
                        continue
                    day = self.checking("Enter day: ", 4)#to get a valid day
                    if not 1 <= day <= 31:
                        print("Invalid day.")
                        continue
                    if month == 2:
                        if not (year % 4 == 0):#To check leap year and to make sure of days in february
                            if day > 28:
                                print("February cannot have MORETHAN 28 for date in the YEAR you entered!!!")
                                continue
                        elif (year % 4 == 0):
                            if day > 29:
                                print("February cannot have MORETHAN 29 for date in LEAP year!!!")
                                continue
                    elif month in [4, 6, 9, 11]:#To get valid day from month with 30 days
                        if day > 30:
                            print("In the MONTH you entered Date 31 is not there, Please check !!!")
                            continue

                    date = f"{year}-{month:02d}-{day:02d}"
                break

            while True:
                trans_type = self.checking("\n1. Income\n2. Expense\n\n\tChoose index to select transaction type : ", 4)
                if trans_type == 1:
                    trans_type = "Income"
                    break
                elif trans_type == 2:
                    trans_type = "Expense"
                    break
                else:
                    print('Choose between "1" or "2"')
                    continue
            break
        
        self.add(source,amount, trans_type, date)
        return

    def add(self, source, amount, trans_type, date):
        '''Add a new transaction'''
        transaction_id = self.transaction_id()
        if source in self.transactions:
            self.transactions[source].append({"Transaction_id": transaction_id,"Amount": amount,"Transaction_type": trans_type,"Date": date})
        else:
            self.transactions[source] = [{"Transaction_id": transaction_id,"Amount": amount,"Transaction_type": trans_type,"Date": date}]
        self.dump()
        print(f"\n\t***Transaction added successfully: {transaction_id}***")
        
    def views(self):
        '''View all transactions'''
        if not self.transactions:
            print("\nNo Transactions Found")
            return

        print("{:<10}{:<12}{:<0} {:<10} {:<25} {:<15}".format("ID", "Category", "", "Amount", "Transaction Type", "Date"))
        print("-" * 70)
        for source, transaction_list in self.transactions.items():
            for transaction in transaction_list:
                print(
                    "{:<10}{:<12}{:<0} {:<10} {:<20} {:<15}".format(transaction['Transaction_id'], source, '\u20A8.', transaction['Amount'], transaction['Transaction_type'], transaction['Date']))

    def update(self):
        '''Function to update transactions'''
        print(f"\t\t{'' * 10}Update Transaction {'' * 10}\n")
        if len(self.transactions) == 0:# check is there any transactions
            print(" !!!Currently no recorded transactions.!!!")
            return

        while True:
            print(f"\n{'-' * 3}Your Transaction History{'-' * 3}")
            self.views()
            option = self.checking(f"\n\tTo Update the whole transaction{'-' * 13}Enter -1\n\tTo Update certain part of the transaction{'-' * 2} Enter -2\n\nEnter your option: ", 4)
            transaction_id = input("\nEnter the numeric value of the Transaction ID you want to update: ")
            transaction_id = "T" + transaction_id.zfill(3)

            for source, transaction_list in self.transactions.items():
                for transaction in transaction_list:
                    if transaction['Transaction_id'] == transaction_id:
                        if option == 2:#here specifically certain elements are updated
                            print("Select field to update:")
                            print(f"\nTo change\n\t Amount{'-' * 10} Enter 1")
                            print(f"\t Date{'-' * 12} Enter 2")
                            print(f"\t Transaction Type Enter 3")
                            choice = input("\nEnter your choice: ")

                            if choice == '1':
                                amount = self.checking("\nEnter the new amount \u20A8:", 3)
                                transaction['Amount'] = amount 
                            elif choice == '2':
                                while True:
                                    year = self.checking("Enter year: ", 4)#check the year format
                                    if len(str(year)) != 4:
                                        print("Invalid year, Format- YYYY")
                                        continue
                                    month = self.checking("Enter month: ", 4)# check month is valid
                                    if not 1 <= month <= 12:
                                        print("Invalid month.")
                                        continue
                                    day = self.checking("Enter day: ", 4) # check day is valid
                                    if not 1 <= day <= 31:
                                        print("Invalid day.")
                                        continue

                                    if month == 2:
                                        if not (year % 4 == 0):#check its not a leap year
                                            if day > 28:
                                                print("February cannot have MORETHAN 28 for date in the YEAR you entered!!!")
                                                continue
                                        elif (year % 4 == 0):#if its a leap year
                                            if day > 29:
                                                print("February cannot have MORETHAN 29 for date in LEAP year!!!")
                                                continue
                                    elif month in [4, 6, 9, 11]:
                                        if day > 30: # these months cant have 31 in day
                                            print("In the MONTH you entered Date 31 is not there, Please check !!!")
                                            continue

                                    date = f"{year}-{month:02d}-{day:02d}"
                                    transaction['Date'] = date
                                    break
                            elif choice == '3':
                                trans_type = self.checking("\n1. Income\n2. Expense\n\n\tChoose index to select transaction type: ", 4)
                                transaction['Transaction_type'] = "Income" if trans_type == 1 else "Expense"
                            else:
                                print("Invalid choice.")
                                return

                        elif option == 1:#here all elemnts in a transaction excpet source adn ID 
                            while True:
                                amount = self.checking("\nEnter the new amount\u20A8:", 3)
                                year = self.checking("Enter year: ", 4)
                                if len(str(year)) != 4:
                                    print("Invalid year, Format- YYYY")
                                    continue
                                month = self.checking("Enter month: ", 4)
                                if not 1 <= month <= 12:
                                    print("Invalid month.")
                                    continue
                                day = self.checking("Enter day: ", 4)
                                if not 1 <= day <= 31:
                                    print("Invalid day.")
                                    continue

                                if month == 2:
                                    if not (year % 4 == 0):
                                        if day > 28:
                                            print("February cannot have MORETHAN 28 for date in the YEAR you entered!!!")
                                            continue
                                    elif (year % 4 == 0):
                                        if day > 29:
                                            print("February cannot have MORETHAN 29 for date in LEAP year!!!")
                                            continue
                                elif month in [4, 6, 9, 11]:
                                    if day > 30:
                                        print("In the MONTH you entered Date 31 is not there, Please check !!!")
                                        continue
                                break

                            date = f"{year}-{month:02d}-{day:02d}"
                            trans_type = self.checking("\n1. Income\n2. Expense\n\n\tChoose index to select transaction type: ", 4)
                            transaction['Amount'] = amount
                            transaction['Date'] = date
                            if trans_type == 1:
                                transaction['Transaction_type'] = "Income"
                            else:
                                transaction['Transaction_type'] = "Expense"
                        else:
                            print("Invalid choice.")
                            return

                        self.dump()
                        print(f"\t{'' * 20}Transaction updated successfully{'' * 20}.")
                        return

            print("!!!Transaction ID not found. Please try again.!!!")

    def delete(self):
        '''Delete a transaction'''
        if not self.transactions:
            print("No transactions to delete.")
            return

        self.views()
        choice = self.checking(" To delete all transactions - Enter -1 \n To delete a specific one - Enter -2: ", 4)
        if choice == 1:
            self.transactions.clear()
            self.dump()
            print("\tAll transactions deleted successfully!!!.")
        elif choice == 2:
            transaction_id = self.checking("Enter the numeric value of the Transaction ID to delete: ", 2)
            transaction_id = f"T{transaction_id.zfill(3)}"

            found = False
            for source, transaction_list in self.transactions.items():
                for transaction in transaction_list:
                    if transaction['Transaction_id'] == transaction_id:
                        transaction_list.remove(transaction)
                        found = True
                        break
                if found:
                    break

            if found:
                self.dump()
                print("\t***Transaction deleted successfully***.")
            else:
                print("Transaction ID not found.!!!")
        else:
            print("Invalid choice.")

    def summary(self):
        '''Display summary of transactions'''
        if not self.transactions:
            print("No transactions to summarize.")
            return

        total_income = 0
        total_expense = 0
        income_sources = {}
        expense_sources = {}

        for source, transaction_list in self.transactions.items():
            for transaction in transaction_list:
                if transaction['Transaction_type'] == 'Income':
                    total_income += transaction['Amount']
                    income_sources[source] = income_sources.get(source, 0) + transaction['Amount']
                elif transaction['Transaction_type'] == 'Expense':
                    total_expense += transaction['Amount']
                    expense_sources[source] = expense_sources.get(source, 0) + transaction['Amount']

        print(f"Total Income: \u20A8{total_income}")
        for source, amount in income_sources.items():
            print(f"  - Income from {source}: \u20A8{amount}")

        print(f"\nTotal Expense: \u20A8{total_expense}")
        for source, amount in expense_sources.items():
            print(f"  - Expense from {source}: \u20A8{amount}")

        cash_in_hand = total_income - total_expense
        print(f"\nCash in Hand: \u20A8{cash_in_hand}")

    def gui(self):
        '''Funtion to open GUI'''
        print(f"\t\t{'*'*8}Minimize the shell and look for GUI{'*'*8}")
        json_file_path = FILENAME  # Path to JSON data
        app = PersonalFinanceTracker(json_file_path)
        app.mainloop()  # Start the GUI
    
class Person():
    def __init__(self,name):
        self.name=name
        self.age=21
    def vote(self,name):
        if self.age > 18:
            print(f"{name}eligible")
        else:
            print(f'{name} non')
    def lunch(self,name,food):
        print(f"{self.name} ate {food}")
        

# Main Function
def main():
    '''Program manager'''
    tracker = FinanceTracker()#@iniator
    
    #person1.name='peter'
    #person1.age=15
    print(f"\n\t\t*{'' * 10}Personal Finance Tracker{'' * 10}*")
    while True:
        print("\nMain Menu")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Update Transaction")
        print("4. Delete Transaction")
        print("5. Transaction Summary")
        print("6. GUI for View transactions using Sort & Search")
        print("7. Exit")

        choice = tracker.checking("\nEnter your choice: ", 4)
        if choice == 1:
            sub_choice = tracker.checking(" To add manually - Enter 1 \n To bulk read from text file - Enter 2: ", 4)
            if sub_choice == 1:
                tracker.new()
            elif sub_choice == 2:
                tracker.bulk_read()
        elif choice == 2:
            tracker.views()
        elif choice == 3:
            tracker.update()
        elif choice == 4:
            tracker.delete()
        elif choice == 5:
            tracker.summary()
        elif choice == 6:
            tracker.gui()
        elif choice == 7:
            person1.vote('king')
            print("Thank you! Exiting.")
            break
        else:
            print("Invalid choice. Please try again.")



main() 
