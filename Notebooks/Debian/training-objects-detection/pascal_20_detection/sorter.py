import os

val_images = os.listdir('anns_validation')

for file in os.listdir('anns'):
    filename = file#.split(".")[0]+".jpg"
    if filename in val_images:
        print(file)
        os.remove(os.path.join('anns',file))  
