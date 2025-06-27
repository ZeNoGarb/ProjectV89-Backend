import cv2
import numpy as np
import onnxruntime as ort
from PIL import Image
import torchvision.transforms as transforms
from .roi import get_bed_roi

CLASSES = ["bed", "sleep", "sit"]

def preprocess_image(frame):
    transform = transforms.Compose([
        transforms.Resize((160, 160)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225])
    ])
    
    roi, _ = get_bed_roi(frame, roi_width=1000)
    roi = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(roi)
    
    image = transform(pil_image)
    image = image.unsqueeze(0)
    return image.numpy()

def predict_pose_class(frame):
    session = ort.InferenceSession("model/bed_pose_mobilenetv2_3.onnx")

    input_tensor = preprocess_image(frame)
    outputs = session.run(None, {'input': input_tensor})

    probabilities = outputs[0]
    predicted_class = np.argmax(probabilities, axis=1)[0]
    
    return CLASSES[predicted_class]
