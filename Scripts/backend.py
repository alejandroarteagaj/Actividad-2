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

def load_img_file(self):
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
        self.array, img2show = read_dicom_file(filepath)
        self.img1 = img2show.resize((250, 250), Image.ANTIALIAS)
        self.img1 = ImageTk.PhotoImage(self.img1)
        self.text_img1.image_create(END, image=self.img1)
        self.button1["state"] = "enabled"

def run_model(self):
    self.label, self.proba, self.heatmap = predict(self.array)
    self.img2 = Image.fromarray(self.heatmap)
    self.img2 = self.img2.resize((250, 250), Image.ANTIALIAS)
    self.img2 = ImageTk.PhotoImage(self.img2)
    print("OK")
    self.text_img2.image_create(END, image=self.img2)
    self.text2.insert(END, self.label)
    self.text3.insert(END, "{:.2f}".format(self.proba) + "%")

def save_results_csv(self):
    with open("historial.csv", "a") as csvfile:
         w = csv.writer(csvfile, delimiter="-")
         w.writerow(
             [self.text1.get(), self.label, "{:.2f}".format(self.proba) + "%"]
        )
    showinfo(title="Guardar", message="Los datos se guardaron con éxito.")

def create_pdf(self):
    cap = tkcap.CAP(self.root)
    ID = "Reporte" + str(self.reportID) + ".jpg"
    img = cap.capture(ID)
    img = Image.open(ID)
    img = img.convert("RGB")
    pdf_path = r"Reporte" + str(self.reportID) + ".pdf"
    img.save(pdf_path)
    self.reportID += 1
    showinfo(title="PDF", message="El PDF fue generado con éxito.")

def delete(self):
    answer = askokcancel(
        title="Confirmación", message="Se borrarán todos los datos.", icon=WARNING
    )
    if answer:
        self.text1.delete(0, "end")
        self.text2.delete(1.0, "end")
        self.text3.delete(1.0, "end")
        self.text_img1.delete(self.img1, "end")
        self.text_img2.delete(self.img2, "end")
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