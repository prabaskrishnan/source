class payment():
    """ users class with two different types: admin user and the regular user """
    def __init__(self):
        self.paymentId = 1
        self.paymentMode = 'Online'    # default Payment Mode
        self.paymentAmount = 0.0
        self.paidBy = ''
        self.paidTo = ''
        self.paymentDate = ''
        self.paymentNotes = ''
  
    # userName property set , get methods
    @property
    def paymentId(self):
        return self.__paymentId
     
    @paymentId.setter
    def paymentId(self,paymentId):
        self.__paymentId = paymentId

    @property
    def paymentMode(self):
        return self.__paymentMode
    
    @paymentMode.setter
    def paymentMode(self,paymentMode):
        self.__paymentMode = paymentMode
    # passWord property set , get methods
    @property
    def paymentAmount(self):
        return self.__paymentAmount
    
    @paymentAmount.setter
    def paymentAmount(self,paymentAmount):
        self.__paymentAmount = paymentAmount
            
    @property
    def paidBy(self):
        return self.__paidBy
    
    @paidBy.setter
    def paidBy(self,paidBy):
        self.__paidBy = paidBy         
  
    @property
    def paidTo(self):
        return self.__paidTo
    
    @paidTo.setter
    def paidTo(self,paidTo):
        self.__paidTo = paidTo
        
    @property
    def paymentDate(self):
        return self.__paymentDate
    
    @paymentDate.setter
    def paymentDate(self,paymentDate):
        self.__paymentDate = paymentDate
        
    @property
    def paymentNotes(self):
        return self.__paymentNotes
    
    @paymentNotes.setter
    def paymentNotes(self,paymentNotes):
        self.__paymentNotes = paymentNotes

class payments:
    """ collection of payments """
    def __init__(self):
        self.payments = []  
        self._user_count = 0
               
    def add_payment(self, payment):
        self.payments.append(payment)
         
    def view_payment(self):
        print('\n')
        print("List of payments: ",end='\n')
        print("------------------ ",end='\n')
        
        print("%-15s %-15s  %-20s %-10s %-15s" % ('Date','Paid By', 'Paid To','Amount','Notes'))
        print('-----------------------------------------------------------------------------------------------------',end='\n')
        for key, value in self.dict_payments.items():        
            
            print("%-15s %-15s %-20s $%-10.2f %-15s" % (value["paymentDate"] ,  value["paidBy"],   value["paidTo"]  ,float(value["paymentAmount"]), value["paymentNotes"]))

    # Method to convert the objects into dictionary
        
    def create_paymentDict(self):
        self.dict_payments = {}
        for payment in self.payments:
            self.dict_payments[payment.paymentId] = {"paymentMode": payment.paymentMode,"paymentAmount":payment.paymentAmount,"paidBy":payment.paidBy,"paidTo":payment.paidTo,"paymentDate":payment.paymentDate,"paymentNotes":payment.paymentNotes}
        return self.dict_payments
