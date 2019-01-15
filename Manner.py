from sys import stdin, stdout
import fileinput

import Actors
import Perf
import Emaip

class manner:
	__actor_attributes = []
	__performance_attributes = []
	__emaip_attributes = []
	# Имена атрибутов, которые будут добавлены автоматически
	__skip_attribute = []

	__actors = dict()
	__performances = dict()
	__emaips = dict()

	__finput = fileinput.FileInput()

	def __init__(self,
		actors,
		performances,
		emaips,
		actor_attributes,
		performance_attributes,
		emaip_attributes,
		skip_attribute):
		self.__actors = actors
		self.__performances = performances
		self.__emaips = emaips
		self.__actor_attributes = actor_attributes
		self.__performance_attributes = performance_attributes
		self.__emaip_attributes = emaip_attributes
		self.__skip_attribute = skip_attribute

	def __print_elements(self, header, dict_val):
		print(header)
		for key, val in dict_val.items():
			print('{} {}'.format(key, val))

	def __print_obj(self, odict, dict_key):
		try: 
			print('{} {}'.format(dict_key, odict[dict_key]))
		except:
			print('Нет такого объектa')

	def print(self):
		self.__print_elements('Актеры:', self.__actors)
		self.__print_elements('Спектакли:', self.__performances)
		self.__print_elements('Расписание:', self.__emaips)

	def __read_properties(self, properties):
		finput = fileinput.FileInput()
		obj = dict()
		for prop in properties:
			if not prop in self.__skip_attribute:
				obj[prop] = input('Введите значение для свойства: {}: '.format(prop))
		return obj

	def __add_element(self, eldict, obj):
		'''
		Добавить элемент с ключом в OderedDict 
		'''	
		incremented_key = int(next(reversed(eldict))) + 1 
		eldict[incremented_key] = obj

	def __remove_element(self, dict_val, del_index):
		del dict_val[del_index]

	def __chek_actor_used(self, actor_index):
		actor = self.__actors[actor_index]
		for key, val in self.__emaips.items():
			if actor is val.get_actor():
				return True
		return False

	def __check_perf_used(self, perf_index):
		performance = self.__performances[perf_index]
		for key, val in self.__emaips.items():
			if performance is val.get_perf():
				return True
		return False		

	def reader(self):
		#for line in self.__finput:
		line = ''
		while True:
			line = input('> ')
			if line.startswith('stop'):
				print('Stopping')
				break
			if line.startswith('print'):
				pargs = line.split()
				if len(pargs) == 3:
					if pargs[1] == 'actor':
						self.__print_obj(self.__actors, pargs[2])
					if pargs[1] == 'perf':
						self.__print_obj(self.__performances, pargs[2])
					if pargs[1] == 'emaip':
						self.__print_obj(self.__emaips, pargs[2])
				else:
					self.print()
				continue
			if line.startswith('new actor'):
				print('Добавление нового актера')
				properties = self.__read_properties(self.__actor_attributes) #отдает словарь
				actor_obj = Actors.actors(properties) #конструируем объект от словаря
				self.__add_element(self.__actors, actor_obj)
				continue
			if line.startswith('new perf'):
				print('Добавление нового спектакля')
				properties = self.__read_properties(self.__performance_attributes)
				perf_obj = Perf.perf(properties)
				self.__add_element(self.__performances, perf_obj)
				continue
			if line.startswith('new emaip'):
				print('Добавление нового расписания')
				properties = self.__read_properties(self.__emaip_attributes)
				emaip_obj = Emaip.emaip(properties, self.__actors, self.__performances)
				self.__add_element(self.__emaips, emaip_obj)
				continue
			if line.startswith('del actor'):
				print('Удаление актера')
				del_index = input('ID удаляемого объекта: ')
				if self.__chek_actor_used(del_index):
					print('Актер учавствует в спектакле, невозможно удалить')
				else:
					self.__remove_element(self.__actors, del_index)
				continue
			if line.startswith('del perf'):
				print('Удаление спектакля')
				del_index = input('ID удаляемого объекта: ')
				if self.__check_perf_used(del_index):
					print('Спектакль задействован в расписании, невозможно удалить')
				else:
					self.__remove_element(self.__performances, del_index)
				continue
			if line.startswith('del emaip'):
				print('Удаление расписания')
				del_index = input('ID удаляемого объекта: ')
				self.__remove_element(self.__emaips, del_index)
				continue
			print('Неопознанная команда: {}'.format(line))
		fileinput.close()

