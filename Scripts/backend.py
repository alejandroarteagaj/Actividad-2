#Hecho por Juan camilo giraldo y Alejandro Arteaga 

from tkinter import *
from tkinter import ttk, font, filedialog, Entry
from tkinter.messagebox import askokcancel, showinfo, WARNING
from PIL import ImageTk, Image
import csv
import tkcap
import numpy as np
import tensorflow as tf
import pydicom as dicom
from tkinter import *
import UI
import Inference
import PIL
tf.compat.v1.disable_eager_execution()
tf.compat.v1.experimental.output_all_intermediates(True)
import cv2

def read_jpg_file(path):#Funciona
    img = cv2.imread(path)
    img_array = np.asarray(img)
    img2show = PIL.Image.fromarray(img_array)
    img2 = img_array.astype(float)
    img2 = (np.maximum(img2, 0) / img2.max()) * 255.0
    img2 = np.uint8(img2)
    return img2, img2show


def read_dicom_file(path):
    img = dicom.read_file(path)
    img_array = img.pixel_array
    img2show = Image.fromarray(img_array)
    img2 = img_array.astype(float)
    img2 = (np.maximum(img2, 0) / img2.max()) * 255.0
    img2 = np.uint8(img2)
    img_RGB = cv2.cvtColor(img2, cv2.COLOR_GRAY2RGB)
    return img_RGB, img2show

def load_img_file(self):##Funciona
    filepath = filedialog.askopenfilename(
        initialdir="/",
        title="Select image",   
        filetypes=(
            ("DICOM", "*.dcm"),
            ("JPEG", "*.jpeg"),
            ("jpg files", "*.jpg"),
            ("png files", "*.png"),
            ),
        )
    if filepath:
        global img1
        global array
        array, img2show = read_jpg_file(filepath)
        img1 = img2show.resize((250, 250), PIL.Image.ANTIALIAS)
        img1 = ImageTk.PhotoImage(img1)
        return img1

def run_model():
    global label 
    global proba
    label, proba, heatmap = Inference.predict()
    global img2
    img2 = PIL.Image.fromarray(heatmap)
    img2 = img2.resize((250, 250), PIL.Image.ANTIALIAS)
    img2 = ImageTk.PhotoImage(img2)
    print("OK")
    return img2, label, proba
    

def delete():
    answer = askokcancel(
        title="Confirmación", message="Se borrarán todos los datos.", icon=WARNING
    )
    return answer



## ERROR AQUI
def preprocess():
    global array21
    array21= cv2.resize(array, (512, 512))
    array2 = cv2.cvtColor(array21, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(4, 4))
    global array23
    global array24
    array24 = clahe.apply(array2)
    array23 = array24 / 255
    array2 = np.expand_dims(array23, axis=-1)
    array2 = np.expand_dims(array2, axis=0)
    return array2 ,array