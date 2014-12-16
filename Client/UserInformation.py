class UserInformation():
    uinfoDict={'uID': '', 'firstName': '', 'lastName': '', 'middleName': '', 'gender': '', 'birthday': ''
        , 'hom_country': '', 'hom_city': '', 'hom_address1': '', 'hom_address2': '', 'hom_address3': '', 'hom_postal':''
        , 'com_country': '', 'com_city': '', 'com_address1': '', 'com_address2': '', 'com_address3': '', 'com_postal':''
        , 'email': '', 'phone_mobile': '', 'phone_home': '', 'phone_work':''
    }
    def __init__(self,tuple):
        for i,key in enumerate(self.uinfoDict):
            self.uinfoDict[key] = tuple[i]