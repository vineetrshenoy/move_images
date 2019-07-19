import os
import sys
import datetime
import shutil
import datetime
from functools import reduce
from distutils.dir_util import copy_tree
from azure.storage.blob import BlockBlobService, PublicAccess


def sendFolderToBlob(dataset):

	block_blob_service = BlockBlobService(account_name='pytorchml3960338808',
                                          account_key='HZK8SliRQf660rcX6yEln78vB+c1CfRsvbSWQda0fPPqBP3fLsmAIB+bB0H9G2OiNOTYZIXwcU514Cdux/8QnQ== ')

	container_name = 'vineettest'
	block_blob_service.create_container(container_name)
	block_blob_service.set_container_acl(container_name, public_access=PublicAccess.Container)
	folder_list = os.listdir(dataset)

	for folder in folder_list:

		archive = shutil.make_archive(folder, 'zip', os.path.join(dataset, folder))
		local_file_name = folder + '.zip'
		block_blob_service.create_blob_from_path(container_name, local_file_name,
                                             os.path.join(os.getcwd(), local_file_name))

		os.remove(local_file_name)
		shutil.rmtree(os.path.join(dataset, folder))


	print('done')
	
if __name__ == '__main__':

	folder = sys.argv[1]

	sendFolderToBlob(folder)
