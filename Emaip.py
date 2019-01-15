class emaip:
    def __init__(self, propdict, actordict, perfdict):
        self.set_perf(perfdict[propdict['perf']]) # передаем словари в объект актера
        self.set_role(propdict['role'])
        self.set_cost(propdict['cost'])
        self.set_actor(actordict[propdict['actorid']]) # передаем словари в объект спектакля

    def __str__(self):
        return 'Спектакль {}, {} в роли \"{}\"'.format(self.__perf, self.__actor, self.__role,)

    def set_role(self,value):
        '''
        Устанавливает роль актера в постановке
        '''
        self.__role=value

    def set_cost(self,value):
        '''
        Устанавливает стоимость годового контракта с актером
        '''
        self.__cost=value

    def set_perf(self,value):
        '''
        Устанавливает название спектакля
        '''
        self.__perf=value

    def set_actor(self,value):
        '''
        Устанавливает актера, занятого в спектакле
        '''
        self.__actor=value

    def get_role(self): 
        '''
        Возвращает роль актера в постановке
        '''
        return self.__role

    def get_cost(self): 
        '''
        Возвращает стоимость годового контракта с актером
        '''
        return self.__cost

    def get_perf(self):
        '''
        Возвращает название спектакля
        '''
        return self.__perf

    def get_actor(self):
        '''
        Возвращает актра, занятого в спектакле
        '''
        return self.__actor

    def as_dict(self):
        '''
        Вернуть все поля объекта в виде словаря
        '''
        return { 'perf': self.__perf,
            'cost': self.__cosc,
            'role': self.__role,
            'actorid': self.__actor }

