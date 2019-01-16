class actors:
    def __init__(self, propdict):
        self.set_name(propdict['name'])
        self.set_surname(propdict['surname'])
        self.set_secname(propdict['secname'])
        self.set_ranc(propdict['rank'])
        self.set_experience(propdict['experience'])

    def __str__(self):
        return '\"{} {} {}\"'.format(self.__name,
            self.__surname,
            self.__secname)

    def set_name(self,value):
        '''
        Устанавливает имя актера
        '''
        self.__name=value

    def set_surname(self,value):
        '''
        Устанавливает фалилию актера
        '''
        self.__surname=value 

    def set_secname(self,value):
        '''
        Устанавливает отчество актера
        '''
        self.__secname=value

    def set_ranc(self,value):
        '''
        Устанавливает звание актера
        '''
        self.__ranc=value

    def set_experience(self,value):
        '''
        Устанавливает стаж актера
        '''
        self.__experience=value

    def get_name(self):
        '''
        Возвращает имя актера
        '''
        return self.__name

    def get_surname(self):
        '''
        Возвращает фамилию актера
        '''
        return self.__surname

    def get_secname(self):
        '''
        Возвращает отчество актера
        '''
        return self.__secname

    def get_ranc(self):
        '''
        Возвращает звание актера
        '''
        return self.__ranc

    def get_experience(self):
        '''
        Возвращает стаж актера
        '''
        return self.__experience

    def as_dict(self):
        '''
        Вернуть все поля объекта в виде словаря.
        '''
        return { 'name': self.__name,
            'surname': self.__surname,
            'secname': self.__secname,
            'rank': self.__ranc,
            'experience': self.__experience}

