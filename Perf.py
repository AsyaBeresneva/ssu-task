class perf:
    def __init__(self, propdict):
        self.set_name(propdict['name'])
        self.set_year(propdict['year'])
        self.set_budget(propdict['budget'])
        
    def __str__(self):
        return '\"{}\"'.format(self.__name)

    def set_name(self,value):
        '''
        Устанавливает название спектакля
        '''
        self.__name=value

    def set_year(self,value):
        '''
        Устанавливает год постановки спектакля
        '''
        self.__year=value

    def set_budget(self,value):
        '''
        Устанавливает бюджет спектакля
        '''
        self.__budget=value

    def get_name(self):
        '''
        Возвращает название спектакля 
        '''
        return self.__name

    def get_year(self):
        '''
        Возвращает год постановки спектакля
        '''
        return self.__year

    def get_budget(self):
        '''
        Возвращает бюджет спектакля
        '''
        return self.__budget

    def as_dict(self):
        '''
        Вернуть все поля объекта в виде словаря
        '''
        return { 'name': self.__name,
            'year': self.__year,
            'budget': self.__budget }

