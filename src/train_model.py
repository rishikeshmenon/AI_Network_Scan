
"""
This module will train an AI Model from a library of images saved in a certain mannner.
"""
from imageai.Classification.Custom import ClassificationModelTrainer
import os
from PIL import Image

def cleanup(folder_path):
    """
    This function cleans up the images in the library to avoid any errors in the file type while training the Model.
    This will also remove any corruputed files in the training data
    """
    extensions = []
    corupt_img_paths=[]
    for fldr in os.listdir(folder_path):
        sub_folder_path = os.path.join(folder_path, fldr)
        for filee in os.listdir(sub_folder_path):
            file_path = os.path.join(sub_folder_path, filee)
            print('** Path: {}  **'.format(file_path), end="\r", flush=True)
            try:
                im = Image.open(file_path)
            except:
                print(file_path)
                os.remove(file_path)
                continue
            else:   
                rgb_im = im.convert('RGB')
                if filee.split('.')[1] not in extensions:
                    extensions.append(filee.split('.')[1])

def train (database,num_experiments,batch_size):
    model_trainer = ClassificationModelTrainer()
    model_trainer.setModelTypeAsResNet50()
    model_trainer.setDataDirectory(database)
    model_trainer.trainModel(num_experiments, batch_size)
        
if __name__ == "__main__":
    database = "TRAIN_TEST_DATA"  #Update this to the path of the folder containing train and test data
    num_experiments = 200  #Update this with the numer of experiments to run in order to train the model
    batch_size = 80 #Update this wtith the number of images to be processed simultaneously. Keep it a multiple of 8
    cleanup(database+r"\test")
    cleanup(database+r"\train")
    train(database,num_experiments,batch_size)

