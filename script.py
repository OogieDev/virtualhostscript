import os
import re

adddel = input('добавить хост - add\nудалить хост - del\n')


if adddel == 'del':
	f = open('/etc/hosts', 'r')
	arr = []
	for i in f:
		arr.append(i)
	f.close()
	delhost = '';
	flag = False
	print('для отмены введите cansel...')
	while(flag == False):
		delhost = input('Введите название хоста, которого нужно удалить: ')
		if delhost not in arr[0]:
			print('такого хоста нет, введите существующее название...')
			continue
		elif delhost == 'cansel':
			exit()
		else:
			flag = True
	
	arr[0] = arr[0].replace(' www.'+delhost, '')
	arr[0] = arr[0].replace(' '+delhost, '')
	
	string = ''
	for i in arr:
		string = string + i

	f = open('/etc/hosts', 'w')
	f.write(string)
	f.close()
	print('hosts успешно удалены...')
	
	f = open('/etc/apache2/sites-available/000-default.conf', 'r')
	
	newarr = ''
	result = []
	resstr = ''
	for line in f:
		newarr = newarr + line
		
	result = newarr.split('<VirtualHost *:80>')
	
	for elem in result:
		if delhost not in elem:
			resstr = resstr + '<VirtualHost *:80>' + elem
	
	f = open('/etc/apache2/sites-available/000-default.conf', 'w')
	f.write(resstr)

	print('000-default.conf успешно переписан...')

	os.system('rm -R /var/www/'+ delhost)
	os.system('sudo service apache2 restart')
	print('директория успешно удалена...')

	print('виртуальный хост успешно удален...')


	
	

elif adddel == 'add':
	f = open('/etc/hosts', 'r')
	arr = []
	for i in f:
		arr.append(i)
	f.close()
	newhost = '';
	flag = False
	print('для отмены введите cansel...')
	while(flag == False):
		newhost = input('Введите название нового хоста: ')
		if newhost in arr[0]:
			print('такой хост уже есть, введите другое название...')
			continue
		elif newhost == 'cansel':
			exit()
		else:
			flag = True
	
	temp = arr[0].split('\n')
	arr[0] = temp[0] + ' ' + newhost + ' ' + 'www.' + newhost + '\n' 

	string = ''
	for i in arr:
		string = string + i

	f = open('/etc/hosts', 'w')
	f.write(string)
	f.close()
	print('hosts успешно записаны...')


	string = '''\n
	<VirtualHost *:80>
	\tDocumentRoot /var/www/'''+ newhost +'''
	\tServerName www.''' + newhost + '''
	\tServerAlias '''+ newhost +'''
	\t\t<Directory /var/www/'''+ newhost +'''>
	\t\tAllowOverride None
	\t\tOrder allow,deny
	\t\tallow from all
	\t</Directory>
	</VirtualHost>\n
	'''
	f = open('/etc/apache2/sites-available/000-default.conf', 'a')
	f.write(string)
	f.close()
	print('000-default.conf успешно записан...')

	os.mkdir('/var/www/'+ newhost)
	os.system('sudo service apache2 restart')
	print('директория успешно создана...')

	print('виртуальный хост готов к работе')

else:
	print('неизвестная команда...')







