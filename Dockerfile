#Hecho por Juan camilo giraldo y Alejandro Arteaga 
FROM python:3.8

RUN git clone https://github.com/alejandroarteagaj/Actividad-2.git
RUN cd /Actividad-2
WORKDIR /Actividad-2

RUN apt update -y && \
   apt-get install python3-opencv -y 


RUN pip3 install --upgrade pip
RUN pip3 install pyproject-toml
RUN pip3 install --upgrade pip setuptools wheel
RUN pip3 install -r requirements.txt
RUN pip3 install Xlib
WORKDIR /Actividad-2/Scripts
#RUN curl "https://www.dropbox.com/s/yx6n606i7cfcvoz/WilhemNet_86.h5?dl=1" -L -o WilhemNet_86.h5

ENTRYPOINT python UI.py


