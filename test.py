import os
import numpy as np
from functools import reduce
from distutils.dir_util import copy_tree
import shutil

def absoluteFilePaths(directory):
	"""!@brief Returns the full filepaths of the files in the folder

	@return array

	"""

	paths = []

	for dirpath, _, filenames in os.walk(directory): 
		for f in filenames:
			paths.append(os.path.abspath(os.path.join(dirpath, f)))

	return paths



def traintoValidation(folder, test_prct):
	"""!@brief Splits the training set to create a validation set

	@return void
	"""
	classes = os.listdir(os.path.join('trial', folder, 'train')) #Get list of all classes in the train folder

	if not os.path.exists(os.path.join('trial', folder,'val')): #create a validation folder if it doesn't exists
		os.mkdir(os.path.join('trial', folder, 'val'))

	for fol in classes:		

		if not os.path.exists(os.path.join('trial', folder, 'val', fol)): #create the class folder in validation if it doesn't exist
			os.mkdir(os.path.join('trial', folder, 'val', fol))

		files = absoluteFilePaths(os.path.join('trial', folder, 'train'))
		np.random.shuffle(files)
		N = len(files)
		num_valid = int(N * test_prct) #the number of files used for validation

		for i in range(0, num_valid):

			from_file = files[i]

			to_file = os.path.join('trial', folder, 'val', fol, os.path.basename(from_file))

			try: #try to move the file
				os.rename(from_file, to_file)
				#logger.info('Moved file: ' + to_file) 
			
			except FileNotFoundError:
				print('File not found')
				#logger.warning('from_file not found: ' + from_file)



def createFolderStructure(merchant_array):

	if not os.path.exists(os.path.join('trial', 'test_train')): #create folder for training
		os.mkdir(os.path.join('trial', 'test_train'))

	#if not os.path.exists(os.path.join('trial', 'test_train', 'test')): #create folder for training
		#os.mkdir(os.path.join('trial', 'test_train', 'test'))
	if not os.path.exists(os.path.join('trial', 'test_train', 'val')): #create folder for training
		os.mkdir(os.path.join('trial', 'test_train', 'val'))
	if not os.path.exists(os.path.join('trial', 'test_train', 'train')): #create folder for training
		os.mkdir(os.path.join('trial', 'test_train', 'train'))

	merchant_array = [x + '_dataset' for x in merchant_array]
	merchant_base_dict = {x: os.listdir(os.path.join('trial', x)) for x in merchant_array}

	total = 0
	for item in merchant_base_dict.keys():

		total = total + len(merchant_base_dict[item])

	assert total / len(merchant_base_dict.keys()) == 2


	
	folders = [os.listdir(os.path.join('trial',key, 'train')) for key in merchant_base_dict.keys()]
	folders = set(reduce((lambda x,y: x + y), folders))


	#map(lambda x: os.mkdir(os.path.join('trial', 'test_train', 'test', x)), folders)
	map(lambda x: os.mkdir(os.path.join('trial', 'test_train', 'val', x)), folders)
	map(lambda x: os.mkdir(os.path.join('trial', 'test_train', 'train', x)), folders)


	for key in merchant_base_dict.keys():

		for ft in ['val', 'train']:

			folders = os.listdir(os.path.join('trial', key, ft))

			for fol in folders:

				copy_tree(os.path.join('trial', key, ft, fol), os.path.join('trial','test_train', ft, fol))


	shutil.make_archive('trial', 'test_train', 'zip', 'test_train')


	x = 5





if __name__ == '__main__':
	

	all_folders = os.listdir(os.path.join(os.getcwd(), 'trial'))
	
	for fol in all_folders:

		traintoValidation(fol, 0.2)
	

	merchant_array = list(map(lambda x: x.split('_')[0], all_folders))
	createFolderStructure(merchant_array)
	x = 5