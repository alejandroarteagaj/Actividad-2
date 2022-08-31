from tkinter import *
from tkinter import ttk, font, filedialog, Entry
from tkinter.messagebox import askokcancel, showinfo, WARNING
import getpass
from PIL import ImageTk, Image
import csv
import pyautogui
import tkcap
import img2pdf
import numpy as np
import time
import tensorflow as tf
import pydicom as dicom
from UI import button1
from UI import text_img1
from UI import text2
from UI import text1
from UI import text3
from UI import text_img2
from UI import reportID
from UI import root
from UI import img1
from UI import img2
from Inference import predict
tf.compat.v1.disable_eager_execution()
tf.compat.v1.experimental.output_all_intermediates(True)
import cv2

def read_dicom_file(path):
    img = dicom.read_file(path)
    img_array = img.pixel_array
    img2show = Image.fromarray(img_array)
    img2 = img_array.astype(float)
    img2 = (np.maximum(img2, 0) / img2.max()) * 255.0
    img2 = np.uint8(img2)
    img_RGB = cv2.cvtColor(img2, cv2.COLOR_GRAY2RGB)
    return img_RGB, img2show

def load_img_file():
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
        array, img2show = read_dicom_file(filepath)
        img1 = img2show.resize((250, 250), Image.ANTIALIAS)
        img1 = ImageTk.PhotoImage(img1)
        text_img1.image_create(END, image=img1)
        button1["state"] = "enabled"
## voy aqui ojo
def run_model(array):
    label, proba, heatmap = predict(array)
    img2 = Image.fromarray(heatmap)
    img2 = img2.resize((250, 250), Image.ANTIALIAS)
    img2 = ImageTk.PhotoImage(img2)
    print("OK")
    text_img2.image_create(END, image=img2)
    text2.insert(END, label)
    text3.insert(END, "{:.2f}".format(proba) + "%")

def save_results_csv(label,proba):
    with open("historial.csv", "a") as csvfile:
         w = csv.writer(csvfile, delimiter="-")
         w.writerow(
             [text1.get(), label, "{:.2f}".format(proba) + "%"]
        )
    showinfo(title="Guardar", message="Los datos se guardaron con éxito.")

def create_pdf():
    cap = tkcap.CAP(root)
    ID = "Reporte" + str(reportID) + ".jpg"
    img = cap.capture(ID)
    img = Image.open(ID)
    img = img.convert("RGB")
    pdf_path = r"Reporte" + str(reportID) + ".pdf"
    img.save(pdf_path)
    reportID += 1
    showinfo(title="PDF", message="El PDF fue generado con éxito.")

def delete():
    answer = askokcancel(
        title="Confirmación", message="Se borrarán todos los datos.", icon=WARNING
    )
    if answer:
        text1.delete(0, "end")
        text2.delete(1.0, "end")
        text3.delete(1.0, "end")
        text_img1.delete(img1, "end")
        text_img2.delete(img2, "end")
        showinfo(title="Borrar", message="Los datos se borraron con éxito")

def read_dicom_file(path):
    img = dicom.read_file(path)
    img_array = img.pixel_array
    img2show = Image.fromarray(img_array)
    img2 = img_array.astype(float)
    img2 = (np.maximum(img2, 0) / img2.max()) * 255.0
    img2 = np.uint8(img2)
    img_RGB = cv2.cvtColor(img2, cv2.COLOR_GRAY2RGB)
    return img_RGB, img2show


def read_jpg_file(path):
    img = cv2.imread(path)
    img_array = np.asarray(img)
    img2show = Image.fromarray(img_array)
    img2 = img_array.astype(float)
    img2 = (np.maximum(img2, 0) / img2.max()) * 255.0
    img2 = np.uint8(img2)
    return img2, img2show

def preprocess(array):
    array = cv2.resize(array, (512, 512))
    array = cv2.cvtColor(array, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(4, 4))
    array = clahe.apply(array)
    array = array / 255
    array = np.expand_dims(array, axis=-1)
    array = np.expand_dims(array, axis=0)
    return array