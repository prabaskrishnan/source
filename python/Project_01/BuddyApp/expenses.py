class expense:    
    """ Expense class """
    def __init__(self):
        self.expenseId = 111    
        self.expenseCategory = ''  
        self.paidByUser = ''
        self.expenseAmount = ''
        self.users = {}
        self.expenseDate = ''
        self.Notes = ''
    # Expense Category property set , get methods
    @property
    def expenseCategory(self):
        return self.__expenseCategory
    
    @expenseCategory.setter
    def expenseCategory(self,expenseCategory):
        self.__expenseCategory = expenseCategory
            
    # Paid By user property set , get methods            
    @property
    def paidByUser(self):
        return self.__paidByUser
    
    @paidByUser.setter
    def paidByUser(self,paidByUser):
        self.__paidByUser = paidByUser
    @property
    def expenseDate(self):
        return self.__expenseDate    
    @expenseDate.setter
    def expenseDate(self,expenseDate):
        self.__expenseDate = expenseDate  
    @property
    def Notes(self):
        return self.__Notes    
    @Notes.setter
    def Notes(self,Notes):
        self.__Notes = Notes  
    @property
    def expenseAmount(self):
        return self.__expenseAmount    
    @expenseAmount.setter
    def expenseAmount(self,expenseAmount):
        self.__expenseAmount = expenseAmount  
        
class expenses:    
    """ collection of expenses """
    
    def __init__(self):
        self.expenses = []          
               
    def add_expenses(self, expense):        
        self.expenses.append(expense)

    def view_expense(self):
        print('\n')
        print("List of expenses: ",end='\n')
        print("------------------ ",end='\n')
        
        print("%-15s %-15s %-10s %-20s %-15s" % ('Date' , 'Paid By','Amount' ,'Category','Paid For'))
        print('-----------------------------------------------------------------------------------------------------',end='\n')

        for key, value in self.dict_expenses.items():       
            print("%-15s %-15s $%-10.2f %-20s %-15s" % (value["expenseDate"] ,  value["paid_by"], float(value["amount"]) , value["category"]  , value["users"]))
                     


     # Building the expense dictionary.            
    def create_expenseDict(self):
        self.dict_expenses = {}
        for expense in self.expenses:
            self.dict_expenses[expense.expenseId] = {"category": expense.expenseCategory,"amount":expense.expenseAmount, "paid_by":expense.paidByUser,"expenseDate":expense.expenseDate,"users":expense.users,"notes":expense.Notes}
        return self.dict_expenses
