
#import xml.dom.minidom as md 
import argparse # Модуль обработки аргументов командной строки
import sys

import Runner
import Parser

def main(argv):
    '''
    Здесь мы разбираем флаги командной строки и определяемся:
    - из файла или БД читать данные
    - в файл или в БД писать данные
    '''
    parser = argparse.ArgumentParser(description='Театр')
    from_group = parser.add_mutually_exclusive_group() #Создаем две группы взаимоисключающих опций (куда записать и где прочитать)
    to_group = parser.add_mutually_exclusive_group()
    from_group.add_argument('-x', '--xml', # Добавляем флаг для xml (add_argument)
        type=str,
        default='theatre.xml', # Опция всегда активна
        help='Прочитать начальные данные из XML файла')
    from_group.add_argument('-s', '--sqlite',
        type=str,
        help='Прочитать начальные данные из базы данных SQLite3')
    to_group.add_argument('-f', '--toxml',
        type=str,
        help='Сохранить данные в файл XML')
    to_group.add_argument('-d', '--tosqlite',
        type=str,
        help='Сохранить данные в базу данных SQLite3')
    args = parser.parse_args() # Отправляет в парсер
    application = Runner.runner()
    if args.xml:
        application.run_from_xml(args.xml, 'theatre')

    if args.sqlite: 
        application.run_from_sqlite(args.sqlite)

    application.repl()

    if args.toxml:
        application.save_to_xml(args.toxml)
    if args.tosqlite:
        application.save_to_sqlite(args.tosqlite)

if __name__ == '__main__':
    main(sys) #Список аргументов командной строки

	
