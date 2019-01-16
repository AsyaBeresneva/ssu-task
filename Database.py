from collections import OrderedDict
import sqlite3

import Actors
import Perf
import Emaip

class db:
    __actors = {}
    __perfs = {}
    __emaips = {}
    __actor_attributes = []
    __perf_attributes = []
    __emaip_attributes = []
    __path = '' # Path to the database
    __conn = ''
    __cursor = ''

    __create_actors = '''
    CREATE TABLE IF NOT EXISTS {} ({});
    '''
    __create_perfs = '''
    CREATE TABLE IF NOT EXISTS {} ({});
    '''
    __create_emaips = '''
    CREATE TABLE IF NOT EXISTS {}
    (
        {},
        FOREIGN KEY (actors) REFERENCES actors(id),
        FOREIGN KEY (perf) REFERENCES perfs(id)
    );
    '''

    def __init__(self,
            path,
            actors,
            perfs,
            emaips,
            actor_attributes,
            perf_attributes,
            emaip_attributes):
        self.__actors = actors
        self.__actor_attributes = actor_attributes

        self.__perfs = perfs
        self.__perf_attributes = perf_attributes

        self.__emaips = emaips
        self.__emaip_attributes = emaip_attributes

        # Устанавливаем соединение с базой данных
        self.__path = path
        self.__conn = sqlite3.connect(self.__path)
        self.__cursor = self.__conn.cursor()
        self.__conn.row_factory = sqlite3.Row
        #self.__row_factory = self.__dict_factory
        #self.__row_factory = self.__dict_factory

    def __attr_list(self, alist, dots=False):
        '''
        Склеить лист колоночек для создания таблички.
        '''
        attrs = ''
        if not dots:
            for elem in alist:
                attrs += elem + ' TEXT' + ', '
        else:
            for elem in alist:
                attrs += ':' + elem + ', '
        attrs = attrs[:-2]
        return attrs

    def __create_table(self, tname, attrs, query):
        '''
        Создаём табличку. Принимаем её имя, список колоночек и шаблон
        SQL запроса.
        '''
        print('Creating table {}'.format(tname))
        print(query.format(tname, self.__attr_list(attrs)))
        self.__conn.execute(query.format(tname, self.__attr_list(attrs)))
        self.__conn.commit()

    def __dump_data(self, tname, attributes, objects):
        query = 'INSERT INTO {} VALUES ({})'.format(tname, self.__attr_list(attributes, True))
        print('Executing query: {}'.format(query))
        for key, value in objects.items():
            tmp_val = value.as_dict()
            tmp_val['id'] = key
            if 'actors' in tmp_val:
                tmp_val['actors'] = list(self.__actors.keys())[list(self.__actors.values()).index(value.get_actor())]
            if 'perfs' in tmp_val:
                tmp_val['perfs'] = list(self.__perfs.keys())[list(self.__perfs.values()).index(value.get_perf())]
            self.__conn.execute(query, tmp_val)
        self.__conn.commit()

    def save(self):
        '''
        Функция сохранения таблички.
        '''
        self.__create_table('actors', self.__actor_attributes, self.__create_actors)
        self.__create_table('perfs', self.__perf_attributes, self.__create_perfs)
        self.__create_table('emaips', self.__emaip_attributes, self.__create_emaips)

        self.__dump_data('actors', self.__actor_attributes, self.__actors)
        self.__dump_data('perfs', self.__perf_attributes, self.__perfs)
        self.__dump_data('emaips', self.__emaip_attributes, self.__emaips)

    def __row2dict(self, inrow):
        return dict(zip(inrow.keys(), inrow))

    def __read_table(self, tname, objdict, objattribtes):
        self.__cursor = self.__conn.cursor()
        self.__cursor.execute('SELECT * FROM `{}`'.format(tname))
        rows = [dict(row) for row in self.__cursor]
        return rows

    def read(self):
        '''
        Читать из базы.
        '''
        actors = self.__read_table('actors', self.__actors, self.__actor_attributes)
        perfs = self.__read_table('perfs', self.__perfs, self.__perf_attributes)
        emaips = self.__read_table('emaips', self.__emaips, self.__emaip_attributes)

        for actor in actors:
            actor_obj = Actors.actors(actor)                      #обходим конкретные атрибуты определенного клиента
            self.__actors[actor['id']] = actor_obj         #соотносим конкретному клиенту ID

        # Преобразуем dict клиентов в OrderedDict
        self.__actors = OrderedDict(sorted(self.__actors.items()))

        for perf in perfs:
            perf_obj = Perfs.perf(perf)
            self.__perfs[perf['id']] = perf_obj

        # Преобразуем dict продуктов в defaultdict
        self.__perfs = OrderedDict(sorted(self.__perfs.items()))

        for emaip in emaips:
            try:
                emaip_obj = Emaips.emaip(emaip, self.__actors, self.__perfs)
                self.__emaips[emaip['id']] = emaip_obj
            except:
                if not emaip['actor'] in self.__actors.keys():
                    print('Отсутствует ссылка на актера: {}'.format(emaip['actor']))
                if not emaip['perf'] in self.__perfs.keys():
                    print('Отсутствует ссылка на спектакль: {}'.format(emaip['perf']))
        self.__emaips = OrderedDict(sorted(self.__emaips.items()))