cfrom tkinter import *
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
from PIL import Image,ImageTk
from tkinter import *
import PIL
import UI
import Inference

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

def load_img_file():##Funciona
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
        array, img2show = read_jpg_file(filepath)
        img1 = img2show.resize((250, 250), PIL.Image.ANTIALIAS)
        img1 = ImageTk.PhotoImage(img1)
        return img1

def run_model(img1):
    array=preprocess(img1)
    label, proba, heatmap = Inference.predict(array)
    img2 = Image.fromarray(heatmap)
    img2 = img2.resize((250, 250), Image.ANTIALIAS)
    img2 = ImageTk.PhotoImage(img2)
    print("OK")
    return img2
    

def save_results_csv(self):
    with open("historial.csv", "a") as csvfile:
         w = csv.writer(csvfile, delimiter="-")
         w.writerow(
             [UI.text1.get(), self.label, "{:.2f}".format(self.proba) + "%"]
        )
    showinfo(title="Guardar", message="Los datos se guardaron con éxito.")

def create_pdf():
    cap = tkcap.CAP(UI.root)
    ID = "Reporte" + str(UI.reportID) + ".jpg"
    img = cap.capture(ID)
    img = Image.open(ID)
    img = img.convert("RGB")
    pdf_path = r"Reporte" + str(UI.reportID) + ".pdf"
    img.save(pdf_path)
    reportID += 1
    showinfo(title="PDF", message="El PDF fue generado con éxito.")

def delete():
    answer = askokcancel(
        title="Confirmación", message="Se borrarán todos los datos.", icon=WARNING
    )
    if answer:
        UI.text1.delete(0, "end")
        UI.text2.delete(1.0, "end")
        UI.text3.delete(1.0, "end")
        UI.text_img1.delete(UI.img1, "end")
        UI.text_img2.delete(UI.img2, "end")
        showinfo(title="Borrar", message="Los datos se borraron con éxito")


def read_jpg_file(path):
    img = cv2.imread(path)
    img_array = np.asarray(img)
    img2show = PIL.Image.fromarray(img_array)
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