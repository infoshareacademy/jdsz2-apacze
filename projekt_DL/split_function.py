import os
import numpy as np
import shutil

# # Creating Train / Val / Test folders (One time use)
root_dir = 'C:/Users/K56/Downloads/Images/'

folders = [name for name in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, name))]

for folder_name in folders:
   if 'train' not in folder_name and 'val' not in folder_name:
       print(folder_name)
       print(os.getcwd())
       try:
         os.makedirs('C:/Users/K56/Downloads/Images/train/' + str(folder_name))
         os.makedirs('C:/Users/K56/Downloads/Images/val/' + str(folder_name))
       except:
         pass

       # Creating partitions of the data after shuffeling
       src = "C:/Users/K56/Downloads/Images/" + str(folder_name)

       allFileNames = os.listdir(src)
       np.random.shuffle(allFileNames)
       train_FileNames, val_FileNames = np.split(np.array(allFileNames), [int(len(allFileNames)*0.7)])


       train_FileNames = [src+'/'+ name for name in train_FileNames.tolist()]
       val_FileNames = [src+'/' + name for name in val_FileNames.tolist()]

       print('Total images: ', len(allFileNames))
       print('Training: ', len(train_FileNames))
       print('Validation: ', len(val_FileNames))

       # Copy-pasting images
       for name in train_FileNames:
         shutil.copy(name, "C:/Users/K56/Downloads/Images/train/" + str(folder_name))

       for name in val_FileNames:
         shutil.copy(name, "C:/Users/K56/Downloads/Images/val/" + str(folder_name))


