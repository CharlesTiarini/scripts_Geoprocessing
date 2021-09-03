## Script para compactação de arquivos
## Criado por Charles Tiarini - Visiona Tecnologia Espacial

import os
import zipfile

cwd = os.getcwd()
folders = sorted([os.path.join(cwd, x) for x in os.listdir(".") if os.path.isdir(os.path.join(cwd, x))])
length = int(len(folders)/2)

for idx in range(length):

	file_list = [folders[idx*2], folders[idx*2+1]]
	name = os.path.split(folders[idx*2])[-1][:20]

	print("Compressing: "+name)

	with zipfile.ZipFile(name+'.zip', 'w') as zipMe:
		for file in file_list:
			files = list(os.walk(file))[0][2]
			for obj in files:
				archive = file+'/'+obj		
				zipMe.write(archive, os.path.basename(archive), compress_type=zipfile.ZIP_DEFLATED)
