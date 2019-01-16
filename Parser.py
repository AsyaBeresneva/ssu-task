import xml.dom.minidom as md   #Стандартная поставка в python

import Actors
import Perf
import Emaip

class writer:
    __xmldoc = md.Document()
    __dumpname = '' # В который сохранять
    __rootname = '' # Имя корневого элемента  
    __rootnode = ''
    __actors = dict()
    __performances = dict()

    def __init__(self, dumpname, rootnode, actors, performances):
        '''
        Создаёт объект XML документа, который должен быть записан
        в файл.
        '''
        self.__dumpname = dumpname
        self.__rootname = rootnode
        root = self.__xmldoc.createElement(self.__rootname) # Создаем элемент
        self.__xmldoc.appendChild(root) # Возвращаем ссылку и добавляем элемент
        self.__rootnode = self.__xmldoc.getElementsByTagName(self.__rootname)[0] # Собираем нужные части
        self.__actors = actors
        self.__performances = performances

    def add_group(self, groupname):
        '''
        Добавляет группу в корневой элемент.
        '''
        xmlgroup = self.__xmldoc.createElement(groupname)
        self.__rootnode.appendChild(xmlgroup)

    def add_element(self, groupname, elemname, el_key, el_val):
        '''
        Вставляет элемент elemname с атрибутами из словаря attributes в
        группу groupname.
        '''
        subgroup = self.__rootnode.getElementsByTagName(groupname)[0]
        newelem = self.__xmldoc.createElement(elemname)
        for attr, value in el_val.as_dict().items(): #Объект преобразуем в словарь
            if attr == 'actorid':
                newelem.setAttribute(attr, str(list(self.__actors.keys())[list(self.__actors.values()).index(el_val.get_actor())]))
                continue
            if attr == 'perf':
                newelem.setAttribute(attr, str(list(self.__performances.keys())[list(self.__performances.values()).index(el_val.get_perf())]))
                continue
            newelem.setAttribute(attr, value)
        subgroup.appendChild(newelem)

    def dump(self):
        '''
        Сбросить сконструированный объект XML в файл __dumpname.
        '''
        handle = open(self.__dumpname, 'w')
        self.__xmldoc.writexml(writer=handle,
            indent='',
            addindent='\t',
            newl='\n', 
            encoding='UTF-8')
        handle.close()

class parser:
    __filename = '' # Имя файла
    __rootnode = '' # Ссылка на объект <>

    def __init__(self, docname, rootnode):
        #print('\nРазбираем файл XML: {}'.format(docname))
        # Читаем XML файл с начальными данными в DOM дерево
        domtree = md.parse(docname) #parse - разбираем файл
        domtree.normalize()

        # Берём корневой элемент документа
        self.__filename = docname
        self.__rootnode = domtree.getElementsByTagName(rootnode)[0] # Обращаемся к первому элементу с этим именем

    def parse_group_for(self, groupname, elemname):
        '''
        Выбрать элементы elemname из группы groupname
        '''
        return self.__rootnode.getElementsByTagName(groupname)[0].getElementsByTagName(elemname)

    def get_attributes(self, entry, attributes):
        '''
        Выбрать все атрибуты из одного элемента XML и вернуть их в
        виде словаря.
        '''
        element = dict()
        for attr in attributes:
            if entry.hasAttribute(attr):
                element[attr] = entry.getAttribute(attr) # Создать ключ и присвоить ему значение атрибута
            else:
                print('Атрибута с именем {} не найден.'.format(attr))
        return element

    def get_entries(self, attrlist, groupname, elemname):
        '''
        Выбрать все элементы атрибуты attrlist из элементов elemname
        из группы groupname и вернуть в виде списка словарей.
        '''
        #print('Создаём список элементов {} из группы {}'.format(elemname, groupname))
        entries = self.parse_group_for(groupname, elemname)
        entry_list = []
        for entry in entries: # Обходим элементы, собираем их атрибуты
            entry_list.append(self.get_attributes(entry, attrlist))

        return entry_list # Возвращаем список словарей

