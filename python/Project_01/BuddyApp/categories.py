class category:    
    """ category class  """
    def __init__(self):
        self.__catId = 111    # defult category Id
        self.catName = ''    
    # category Name property set , get methods
    @property
    def catName(self):
        return self.__catName
    
    @catName.setter
    def catName(self,catName):
        self.__catName = catName            
    # Category Id property get methods                 
    @property
    def catId(self):             # Read only property
        return self.__catId        

class categories:    
    """ collection of categories """
    
    def __init__(self):
        self.categories = []  
              
    def add_category(self, category):        
        self.categories.append(category)

    def view_category(self):
        print('\n')
        print("List of categories: ",end='\n')
        print("------------------ ",end='\n')
        for key in self.dict_categories.items():
            print(key[0],end='\n')        
        
    def create_catDict(self):
        self.dict_categories = {}
        for category in self.categories:
            self.dict_categories[category.catName] = {"categoryId":category.catId}
        return self.dict_categories