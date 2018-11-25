class user():
    """ users class with two different types: admin user and the regular user """
    def __init__(self):
        self.__userType = 'R'    # Regular user by Default
        self.passWord = ''    
    # userName property set , get methods
    @property
    def userName(self):
        return self.__userName
     
    @userName.setter
    def userName(self,userName):
        self.__userName = userName
    @property
    def userId(self):
        return self.__userId
     
    @userId.setter
    def userId(self,userId):
        self.__userId = userId
    # passWord property set , get methods
    @property
    def passWord(self):
        return self.__passWord
   
    @passWord.setter
    def passWord(self,passWord):
        self.__passWord = passWord
    @property
    def userType(self):             # Read only property
        return self.__userType
        

class users:
    """ collection of users """   
    def __init__(self):
        self.users = []  
        self._user_count = 0
               
    def add_user(self, user):     
        self._user_count +=1
        user.userId = self._user_count
        self.users.append(user)

    def view_user(self):
        print('\n')
        print("List of users: ",end='\n')
        print("-------------- ",end='\n')

        for key in self.dict_users.items():
            print(key[0],end='\n')

    def create_userDict(self):
        self.dict_users = {}
        for user in self.users:
            self.dict_users[user.userName] = {"userId": user.userId,"passWord":user.passWord,"userType":user.userType}
        return self.dict_users
