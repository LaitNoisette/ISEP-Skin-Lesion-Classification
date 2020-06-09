# -*- coding: utf-8 -*-
"""Utils.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KZinfMBV1F904PLoB1dpKtWhWtJe3PH7
"""

import cv2
from google.colab.patches import cv2_imshow
import pandas as pd
import os, json

import kernel_patching

def imShowScale(im,scale=10):
  imResize=cv2.resize(im,(int(im.shape[1]/scale),int(im.shape[0]/scale)))
  cv2_imshow(imResize)

def prepareExcelFile(rootPath,fileName,metadataFileName):
  def add_name_and_commonPath_columns(data):
     data['name'] = data.iloc[:,0].map(lambda x : (((x.split('\\'))[-1]).split('.'))[0])
     data['commonPath'] = data.iloc[:,0].map(lambda x : '/'.join(((x.split('\\'))[-3:])) )
     return data
  def X_metadata(metadata,X_data):
    metadata = pd.merge(metaData, X_data,  how='inner', on='name')
    metadata['path'] = metadata.commonPath.map(lambda x : os.path.join(rootPath,x))
    return metadata[['name','commonPath','path','meta.clinical.benign_malignant']]

  filePath = os.path.join(rootPath,fileName)

  fileData = pd.read_excel(filePath, header=None,names=['path'])
  fileData= add_name_and_commonPath_columns(fileData)

  metadataPath = os.path.join(rootPath,metadataFileName)
  metaData = pd.read_csv(metadataPath)

  X_filedata_metadata= X_metadata(metaData,fileData)
  return X_filedata_metadata

def loadDataset(fileMetadataList,rootPath,pictureFolderPath,nbPicture=-1):
  patchDictList=[]
  for index, row in fileMetadataList.head(nbPicture).iterrows(): 
    fileName=row["name"]
    fileExtension='.jpg'

    picturePath=os.path.join(rootPath,pictureFolderPath)

    fileNameExt=fileName+fileExtension
    picturePath = os.path.join(picturePath,fileNameExt)

    if os.path.isfile(picturePath):
      print (row["commonPath"])

      kernelPatch=kernel_patching.KernelPatch(3,picturePath,True)
      kernelPatch.extractOverlappingPatchListFromROI()

      for patch in kernelPatch.imPatchList:
        patchDict = {
            "imName": fileNameExt,
            "patch":patch,
            "benign_malignant":row['meta.clinical.benign_malignant']
            }
        #print (patchDict)
        patchDictList.append(patchDict)
  
  return patchDictList

def prepareDataset(patchDictionaryList):
  def convert_to_one_hot(Y, C):
    Y = np.eye(C)[Y.reshape(-1)].T
    return Y
  
  X_dataset=[]
  Y_dataset=[]

  for patchDict in patchDictionaryList:
    X_dataset.append(patchDict['patch'])
    Y_dataset.append(patchDict['benign_malignant'])

  Y_dataset=np.array(Y_dataset)
  #Y_dataset = Y_dataset.reshape((1, Y_dataset.shape[0]))

  Y_dataset[Y_dataset == 'benign']=0
  Y_dataset[Y_dataset == 'malignant']=1

  return np.array(X_dataset),convert_to_one_hot(np.uint(Y_dataset),2)

def savePicture(rootPath,fileName,fileExtension,im):
  fileName=fileName+fileExtension
  filePath = os.path.join(rootPath,fileName)
  if not os.path.isfile(filePath):
    print(filePath)
    cv2.imwrite(filePath,im)