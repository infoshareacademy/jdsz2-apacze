Binary classification -> Categorical classifiaction

0. shear_range wywali� + rotation_range=10 -> do parametr�w (wypr�buj w 0_data_augmentation)
1. Model VGG19 indlude_top=false
2. bootleneck - ImageDataGenerator.flow_from_directory(class mode = categorical)
3. p�tla tak jak w "0_data_augmentation" - dla bootleneck w def main, musza by� dwa pliki features i labels
4. train_model - 1 warstwa 1024, 2 warstwa 67 klas, model.compile loss=categorical_crossentropy, activation=softmax
5. load data fetures i labels z pliku (nie array generowany)

6. fine tune - taki sam model + layer 1:17 trainable=false + loss categorical


Funkcja 

wej�cie dane wej�ciowe Images
os.dirlist ()->�cie�ka
for folder in dirlist:
	len(dirlist.folder):
