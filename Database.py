from collections import OrderedDict
import sqlite3


class db:
    __actors = {}
    __performances = {}
    __emaips = {}
    __client_attributes = []
    __product_attributes = []
    __sale_attributes = []
    __path = '' # Path to the database
    __conn = ''
    __cursor = ''

    __create_clients = '''
    CREATE TABLE IF NOT EXISTS {} ({});
    '''
    __create_products = '''
    CREATE TABLE IF NOT EXISTS {} ({});
    '''
    __create_sales = '''
    CREATE TABLE IF NOT EXISTS {}
    (
        {},
        FOREIGN KEY (client) REFERENCES clients(id),
        FOREIGN KEY (product) REFERENCES products(id)
    );
    '''

    def __init__(self,
            path,
            clients,
            products,
            sales,
            client_attributes,
            product_attributes,
            sale_attributes):
        self.__clients = clients
        self.__client_attributes = client_attributes

        self.__products = products
        self.__product_attributes = product_attributes

        self.__sales = sales
        self.__sale_attributes = sale_attributes

        # Establish database connection
        self.__path = path
        self.__conn = sqlite3.connect(self.__path)
        self.__cursor = self.__conn.cursor()

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
            if 'product' in tmp_val:
                tmp_val['product'] = list(self.__products.keys())[list(self.__products.values()).index(value.getProduct())]
            if 'client' in tmp_val:
                tmp_val['client'] = list(self.__clients.keys())[list(self.__clients.values()).index(value.getClient())]
            self.__conn.execute(query, tmp_val)
        self.__conn.commit()

    def save(self):
        '''
        Функция сохранения таблички.
        '''
        self.__create_table('clients', self.__client_attributes, self.__create_clients)
        self.__create_table('products', self.__product_attributes, self.__create_products)
        self.__create_table('sales', self.__sale_attributes, self.__create_sales)

        self.__dump_data('clients', self.__client_attributes, self.__clients)
        self.__dump_data('products', self.__product_attributes, self.__products)
        self.__dump_data('sales', self.__sale_attributes, self.__sales)

