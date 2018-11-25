import sys
import generic
import os.path
import datetime

from users import users
from users import user
from categories import categories
from categories import category
from expenses import expenses
from expenses import expense
from payments import payments
from payments import payment

import getpass
import pickle as pick

 # Load the data into objects from the pickle serialization files for users.
if os.path.isfile("users.pickle"):
    with open('users.pickle', 'rb') as handle:
        obj_users = pick.load(handle)   
else: obj_users = users()
dict_Users = obj_users.create_userDict()

# Load the data into objects from the pickle serialization files for categories.
if os.path.isfile("categories.pickle"):
    with open('categories.pickle', 'rb') as handle:
        obj_categories = pick.load(handle) 
else: obj_categories = categories()
dict_categories = obj_categories.create_catDict()

# Load the data into objects from the pickle serialization files for expenses.
if os.path.isfile("expenses.pickle"):
    with open('expenses.pickle', 'rb') as handle:
        obj_expenses = pick.load(handle) 
else: obj_expenses = expenses()
dict_expenses = obj_expenses.create_expenseDict()

# Load the data into objects from the pickle serialization files for payments.
if os.path.isfile("payments.pickle"):
    with open('payments.pickle', 'rb') as handle:
        obj_payments = pick.load(handle) 
else: obj_payments = payments()
dict_payments = obj_payments.create_paymentDict() 

def main_func(str):
    # Function that returns a specific method to be executed based on the input selection by the user.
    return dictFunctions[str]


def add_user():    
    # Method to invoke the user , users object collection to add a new user.
    global obj_users
    userName = input("Enter the name of the user to be added: ")
    newUser = user()
    newUser.userName = userName    
    try:
        obj_users.add_user(newUser)
    except Exception as e:
        print(e)
    else:
        with open('users.pickle', 'wb') as handle:
            pick.dump(obj_users,handle)
        with open('users.pickle', 'rb') as handle:
            obj_users = pick.load(handle)
        print('\n')
        print("User Added Successfully.")
        print('\n')

def login_user(strUserName,strPassword):
    # Authentication method
    import pickle
    with open('users.pickle', 'rb') as handle:
        obj_users = pickle.load(handle)
    for user in obj_users.users:
        if user.userName == strUserName and user.passWord == strPassword:
            return True
    return False

def add_category():
    # Method to add new categories.
    global obj_categories
    catName = input("Enter the name of the category to be added: ")
    print('\n')
    newcategory = category()
    newcategory.catName = catName    
    try:
        obj_categories.add_category(newcategory)
    except Exception as e:
        print(e)
    else:
        with open('categories.pickle', 'wb') as handle:
            pick.dump(obj_categories,handle)
        obj_categories.create_catDict()
        print('\n Category Added Successfully. \n')

def add_expense():
    # Function to add the new expenses.
    global obj_expenses
    global obj_categories
    global obj_users
    global dict_expenses
    list_category = [cat.catName for cat in obj_categories.categories]
    while 1==1:
        try:
            print("Categories: ", [str(list_category.index(item)+1) + ':' + item for item in list_category])
            expenseCategory = list_category[int(input("Enter category for the expense: ")) -1]
        except:
            print("Please enter a valid number from the list above. ")
            continue
        else:
            break
    while 1==1:
        try:
            expenseDate = input('Enter the date of the expense, hit [Enter] for today: ')
            if expenseDate=='':
                expenseDate = datetime.date.today()
            #expenseDate = datetime.date(expenseDate)
        except: 
            print("Please enter valid date format. ")
            continue
        else:
            print(expenseDate)
            break
    while 1==1:
        try:
            expenseAmount = "{:.2f}".format(float(input('Enter the amount in $: ')))
        except:
            print("Please enter valid amount. ")
            continue
        else:
            break
           
    list_users =  [user.userName for user in obj_users.users]
    while 1==1:
        try:
            print("Users: ", [str(list_users.index(item)+1) + ':' + item for item in list_users])
            expensepaidbyUser = list_users[int(input("Who paid for this expense? : ")) -1]            
        except:
            print("Please enter a valid number from the list above. ")
            continue
        else:
            break
    
    while 1==1:
        try:
            print("Users: ", [str(list_users.index(item)+1) + ':' + item for item in list_users])
            expenseUser = input("Enter the numbers of people from above for this expense (comma seperated):  ")
            expenseUser = expenseUser.split(',')
            expenseUser = [list_users[int(expenseUser[i])-1] for i in range(len(expenseUser))]                       
        except:
            print("Please enter a valid number from the list above. ")
            continue
        else:
            break

    expenseNotes = input("Print any additional notes for this expense: ")
    
    # New Expense OBject
    newExpense = expense()
    newExpense.expenseAmount = float(expenseAmount) / len(expenseUser)
    newExpense.expenseCategory = expenseCategory
    newExpense.expenseDate = expenseDate
    newExpense.paidByUser = expensepaidbyUser
    newExpense.Notes = expenseNotes
    newExpense.users = expenseUser
    # Max value + 1 for New ID.
    if len(dict_expenses) > 0:
        max_key = max([int(s) for s in dict_expenses.keys()])
    else: max_key = 100
    newExpense.expenseId = max_key +1

    try:
        obj_expenses.add_expenses(newExpense)
    except Exception as e:
        print(e)
    else:
        with open('expenses.pickle', 'wb') as handle:
            pick.dump(obj_expenses,handle)
        
        dict_expenses = obj_expenses.create_expenseDict()
        print('\n Expenses Added Successfully \n')    



def view_balance():
    # Function to view the balance
    
    dict_balance = {}
    for user1 in dict_Users:
        for user2 in dict_Users:
            if user1 != user2:
                dict_balance[(user1,user2)] = 0

    for key, value in dict_expenses.items():
        for user in value["users"]:
            dict_balance[(user, value["paid_by"])] = dict_balance[(user, value["paid_by"])] +  float(value["amount"])
    print('\n')
    # Deduct all the payments that have been done already
    for key,value in dict_payments.items():
        dict_balance[(value["paidBy"], value["paidTo"])] = dict_balance[(value["paidBy"], value["paidTo"])] - float(value["paymentAmount"])

    for key, value in dict_balance.items():
        if float(value) > 0:
            print (key[0] + " Owes " + key[1] + "  $" + str("{:.2f}".format(value)) + '.')
    print('\n')

def make_payment():
    # Function to make the payments.
    global obj_users
    global dict_payments
    # Payment Amount
    while 1==1:
        try:
            paymentAmount = "{:.2f}".format(float(input('Enter the payment amount in $: ')))
        except:
            print("Please enter valid amount. ")
            continue
        else:
            break           
    list_users =  [user.userName for user in obj_users.users]
    
    # Paid To user
    while 1==1:
        try:
            print("Users: ", [str(list_users.index(item)+1) + ':' + item for item in list_users])
            paymentpaidTo = list_users[int(input("Who are you paying to? : ")) -1]
            
        except:
            print("Please enter a valid number from the list below. ")
            continue
        else:
            break
    
        # Payment Notes
    paymentNotes = input("Print any additional notes for this payment: ")
    # Create a new payment object and add it to payments
    newPayment = payment()
    newPayment.paidTo = paymentpaidTo
    newPayment.paymentAmount = paymentAmount
    newPayment.paymentDate = datetime.date.today() 
    newPayment.paymentMode = "Online"
    newPayment.paymentNotes = paymentNotes
    newPayment.paidBy = strUserName    

    if len(dict_payments) > 0:
        max_key = max([int(s) for s in dict_payments.keys()])
    else: max_key = 100
    newPayment.paymentId = max_key +1

    try:
        obj_payments.add_payment(newPayment)
    except Exception as e:
        print(e)
    else:
        with open('payments.pickle', 'wb') as handle:
            pick.dump(obj_payments,handle)        
        dict_payments = obj_payments.create_paymentDict()
        print('\n')
        print("Payment Processed Successfully.")
        print('\n')

# View functions for Users , Categories , Expenses and Payments.
def view_user():
   obj_users.view_user()
    
def view_category():
   obj_categories.view_category()
   
def view_expense():    
    obj_expenses.view_expense()
    
def view_payment():
    obj_payments.view_payment()
    
generic.print_Welcome()   
 # Login screen
while 1==1:
    strUserName = input("User Name: ")
    if strUserName == 'exit': sys.exit()
    strPassword = getpass.getpass("Password: ")
    boolLogin = login_user(strUserName,strPassword)
    if boolLogin is False:
        print('Incorrect UserId or Password... ')
        continue
    else: break

print('\nWelcome back ' , strUserName ,' great to see you again !!! , How can I help you today?  \n')
# List of actions that user can perform  
dictFunctions = {}
dictFunctions['1'] = view_balance
dictFunctions['2'] = add_expense
dictFunctions['3'] = make_payment
dictFunctions['4'] = add_category
dictFunctions['5'] = add_user
dictFunctions['6'] = view_user
dictFunctions['7'] = view_category
dictFunctions['8'] = view_expense
dictFunctions['9'] = view_payment
# Shows the command prompt to receive the user action    
while 1==1:
    
    generic.show_Options()
    strOption = input("command$: ")
    if strOption == 'Q' or strOption=='q':
        sys.exit()
    elif strOption == 'help':
        generic.show_Options()
        strOption = input("command$: ")
    try: 
        main_func(strOption)()
    except:
        print("\n Please choose a proper option. \n")
        continue



