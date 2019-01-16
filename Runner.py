from collections import OrderedDict

import Actors
import Perf
import Emaip
import Manner  # Читалка комманд с терминала.

import Parser  # Модуль чтения и записи XML.

import Database # Модуль чтения и записи БД SQLite3

class runner:
    __actor_attributes = ('name',
        'surname',
        'secname',
        'rank',
        'experience',
        'id')
    __performance_attributes = ('name',
        'year',
        'budget',
        'id')
    __emaip_attributes = ('perf',
        'cost',
        'role',
        'actorid',
        'id')
    __skip_attribute = ('id')
    __source_path = ''
    __actors = dict()
    __performances = dict()
    __emaips = dict()

    def run_from_xml(self, source, rootnode):
        theatre_xml = Parser.parser(source, rootnode)
        # Получаем список словарей-актёров, лист с табличками словарями
        actors = theatre_xml.get_entries(self.__actor_attributes,
            'actors',
            'actor')
        # Конструируем объекты актёров из словарей и мапим айдишники
        # актёров в объекты актёров. Это понадобится, чтобы связать
        # айдишники актёров с расписаниями спектаклей.
        for actor in actors:
            actor_obj = Actors.actors(actor) # Обходим атрибуты определенного аутера
            self.__actors[actor['id']] = actor_obj # Соотносим конкретному актеру ID
 
        self.__actors = OrderedDict(sorted(self.__actors.items())) # Преобразуем dict актеров в OrderedDict

        # Здесь мы получаем список словарей-спектаклей
        # Каждый словарь это набор свойств одного спектакля.
        performances = theatre_xml.get_entries(self.__performance_attributes,
            'perfs',
            'perf')
        #  айдишники спектаклей в объекты спектаклей. Это нужно для связи расписаний со спектаклями.
        for performance in performances:
            performance_obj = Perf.perf(performance)
            self.__performances[performance['id']] = performance_obj

        self.__performances = OrderedDict(sorted(self.__performances.items()))

        # Cобираем список словарей расписаний.
        emaips = theatre_xml.get_entries(self.__emaip_attributes,
            'emaips',
            'emaip')
        # Конструируем объекты расписаний, мапим их номера в объекты,заодно подтягиваем айдишники спектаклей и актёров.
        for emaip in emaips:
            try:
                emaip_obj = Emaip.emaip(emaip, self.__actors, self.__performances)
                self.__emaips[emaip['id']] = emaip_obj
            except:
                if not emaip['actor'] in self.__actors.keys():
                    print('Актер отсутствует: {}'.format(emaip['actor']))
                if  not emaip['performance'] in self.__performances.keys():
                    print('Спектакль отсутствует: {}'.format(emaip['performance']))
        self.__emaips = OrderedDict(sorted(self.__emaips.items()))

    def run_from_sqlite(self, dbfile='theatre.sqlite3'):
        '''
        Прочитать данные для работы из базы данных SQLite3.
        '''
        database = Database.db(dbfile,
            self.__actors,
            self.__performances,
            self.__emaips,
            self.__actor_attributes,
            self.__performance_attributes,
            self.__emaip_attributes)
        database.read()

    def save_to_xml(self, xmlfile='new.xml'):
        '''
        Сохранить структуры данных в XML файл.
        '''
        dump = Parser.writer(xmlfile, 'theatre', self.__actors, self.__performances)
        dump.add_group('actors')
        dump.add_group('perfs')
        dump.add_group('emaips')
        for actor_key, actor_val in self.__actors.items():
            dump.add_element('actors', 'actor', actor_key, actor_val)
        for perf_key, perf_val in self.__performances.items():
            dump.add_element('perfs', 'perf', perf_key, perf_val)
        for emaip_key, emaip_val in self.__emaips.items():
            dump.add_element('emaips', 'emaip', emaip_key, emaip_val)
        dump.dump()

    def save_to_sqlite(self, dbfile='db.sqlite3'):
        '''
        Сохранить результаты работы в базу данных SQLite3.
        '''
        database = Database.db(dbfile,
            self.__actors,
            self.__performances,
            self.__emaips,
            self.__actor_attributes,
            self.__performance_attributes,
            self.__emaip_attributes)
        database.save()

    def repl(self):
        '''
        Редактировать в консоли (читать, писать, изменять, удалять)
        '''
        repl = Manner.manner(self.__actors,
            self.__performances,
            self.__emaips,
            self.__actor_attributes,
            self.__performance_attributes,
            self.__emaip_attributes,
            self.__skip_attribute )
        
        repl.reader()
        
