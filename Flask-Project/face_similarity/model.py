import os
import re

import glob
import pickle
import numpy as np
import pandas as pd
from PIL import Image
import face_recognition as fr
np.random.seed(50)


# 파일명으로부터 연예인 이름 추출
def get_name(image_path):
    file_name = image_path.split('/')[-1]
    name = file_name.split('.')[0]
    
    return name

# 이미지에서 얼굴을 추출하는 함수
def get_cropped_face(image, model='hog'):                 # model은 HOG와 CNN 두 가지 가능
    face_location = fr.face_locations(image, model=model) # 얼굴 탐지 함수
    top, right, bottom, left = face_location[0]           # 탐지된 box 좌표
    cropped_image = image[top:bottom, left:right]         # 좌표를 이용해 이미지 내에서 해당 area만 추출
    
    return cropped_image

# 두 명의 임베딩 거리 측정하는 함수
def get_distance(name1, name2, embedding_dict):
    name1_embedding = np.stack(embedding_dict[name1], axis=0)
    name2_embedding = np.stack(embedding_dict[name2], axis=0)
    distance = np.linalg.norm(name1_embedding - name2_embedding, ord=2)
    
    return distance

# 한 명의 이름을 먼저 넣고, 나머지 이름을 모두 비교할 수 있도록 도와주는 함수
# 이후에 sorted()를 할 때 key인자로 사용
def sort_key_value(name1):
    def get_distance_from_name1(name2):
        return get_distance(name1, name2, embedding_dict)
    
    return get_distance_from_name1

# key인자에 함수를 이용하여 비교하고자 하는 사람과 나머지 사람들을 전부 비교
def get_nearest_face(name, embedding_dict, top=5):
    key_value = sort_key_value(name)
    result = sorted(embedding_dict.items(), key=lambda x: key_value(x[0]))[1:top+1]
    
    top_distance = [get_distance(name, k, embedding_dict) for k, v  in result]         # 나온 결과를 list로 저장
    
    return result, top_distance


def image_processing(image_path):
    image = fr.load_image_file(image_path)

    cropped = get_cropped_face(image)
    embedding = fr.face_encodings(cropped)
    
    return cropped, embedding


with open('face_cropped_full.pkl', 'rb') as f:     # 저장된 Crop 이미지 불러오기
    cropped_image_dict = pickle.load(f)
    
with open('face_embedding_full.pkl', 'rb') as f:     # 저장된 임베딩 결과 불러오기
    embedding_dict = pickle.load(f)



def get_rank(image_path, 
             cropped_image_dict=cropped_image_dict,
             embedding_dict=embedding_dict):
    
    me_cropped, me_embedding = image_processing(image_path)
    
    cropped_image_dict['me'] = me_cropped
    embedding_dict['me'] = me_embedding
    
    result, top_distance = get_nearest_face('me', embedding_dict, top=5)
    
    return me_cropped, result, top_distance

    
