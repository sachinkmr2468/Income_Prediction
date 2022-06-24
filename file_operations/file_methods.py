import pickle
import os
import shutil
from application_logging.logger import App_Logger
from app_exception.exception import AppException
import sys

ob = App_Logger()

class File_Operation:
    """
                This class shall be used to save the model after training
                and load the saved model for prediction.
                """
    def __init__(self):
        self.file_object = open('Training_Logs/File_Operationlog.txt','a+')
        self.model_directory='file_operations/models/' # give the path

    def save_model(self,model,filename): #model,filename - will be passed when this model will be called
        """
            Method Name: save_model
            Description: Save the model file to directory
            Outcome: File gets saved
            On Failure: Raise Exception
"""
        ob.log(self.file_object,'Entered the save_model method of the File_Operation class')
        try:
            path = os.path.join(self.model_directory,filename) #create seperate directory for each cluster
            if os.path.isdir(path): #remove previously existing models for each clusters
                shutil.rmtree(self.model_directory) #removing the dir itself if exit
                os.makedirs(path) # making the dir
            else:
                os.makedirs(path) #Making the dir
            with open(path +'/' + filename+'.sav',
                      'wb') as f:
                pickle.dump(model, f) # save the model to file
            ob.log(self.file_object,'Model File '+filename+' saved. Exited the save_model method of the Model_Finder class')

            return 'success'
        except Exception as e:
            ob.log(self.file_object,'Exception occured in save_model method of the Model_Finder class,  Exception message'+str(e))
            ob.log(self.file_object,'Model File '+filename+' could not be saved. Exited the save_model method of the Model_Finder class')

#            raise Exception()
#        except Exception as e:
            raise AppException(e, sys) from e

    def load_model(self,filename): # file name will be passed when this method is called
        """
                    Method Name: load_model
                    Description: load the model file to memory
                    Output: The Model file loaded in memory
                    On Failure: Raise Exception
        """
        ob.log(self.file_object,'Entered the load_model method of the File_Operation class')

        try:
            with open(self.model_directory + filename + '/' + filename + '.sav',
                      'rb') as f:
                ob.log(self.file_object,
                                       'Model File ' + filename + ' loaded. Exited the load_model method of the Model_Finder class')
                return pickle.load(f)
        except Exception as e:
            ob.log(self.file_object,
                                   'Exception occured in load_model method of the Model_Finder class. Exception message:  ' + str(
                                       e))
            ob.log(self.file_object,
                                   'Model File ' + filename + ' could not be saved. Exited the load_model method of the Model_Finder class')
#            raise Exception()
#        except Exception as e:
            raise AppException(e, sys) from e

    def find_correct_model_file(self, cluster_number):
        """
                            Method Name: find_correct_model_file
                            Description: Select the correct model based on cluster number
                            Output: The Model file
                            On Failure: Raise Exception

                """
        ob.log(self.file_object,
                               'Entered the find_correct_model_file method of the File_Operation class')
        try:
            self.cluster_number = cluster_number
            self.folder_name = self.model_directory
            self.list_of_model_files = []
            self.list_of_files = os.listdir(self.folder_name)
            for i in self.list_of_files:
                try:
                    if (i.index(str( self.cluster_number))!=-1):
                        self.model_name=i
                except:
                    continue
            self.model_name = self.model_name.split('.')[0]
            ob.log(self.file_object,
                                   'Exited the find_correct_model_file method of the Model_Finder class.')
            return self.model_name
        except Exception as e:
            ob.log(self.file_object,
                                   'Exception occured in find_correct_model_file method of the Model_Finder class. Exception message:  ' + str(
                                       e))
            ob.log(self.file_object,
                                   'Exited the find_correct_model_file method of the Model_Finder class with Failure')
#        except Exception as e:
            raise AppException(e, sys) from e