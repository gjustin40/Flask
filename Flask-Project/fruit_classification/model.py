from PIL import Image
import torch
import torch.optim as optim
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
import numpy as np
import os

# 학습 된 모델만 들어오면 된다.


fruit_class = {1:'banana', 2:'grape', 3:'orange', 0:'strawberry', 4:'apple', 5:'pineapple', 6:'unknown'}

model = torchvision.models.vgg16(pretrained=True)
model_dict = torch.load('trained_model_epoch80_acc85.49618320610686_class7.pth')
model.classifier[6] = nn.Linear(4096, 7)
model.load_state_dict(model_dict)

transform = transforms.Compose([
    transforms.Resize((200,200)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# if torch.cuda.is_available():
#     device = 'cuda'
# else:
#     device = 'cpu'

#model.to(device)
def image_processing(image_path):
    img = Image.open(image_path)
    img_tensor = transform(img).unsqueeze(0)

    return img_tensor

def fruit_classification(image_path):

    img_tensor = image_processing(image_path)

    #img = img_tensor.to(device)

    model.eval()
    output = model(img_tensor)
    fruit_class_id = output.argmax(dim=1).item()
    fruit = fruit_class[fruit_class_id]

    return fruit