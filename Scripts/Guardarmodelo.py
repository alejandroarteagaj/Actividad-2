##Script para cargar modelo
import urllib.request
url = "https://www.dropbox.com/s/yx6n606i7cfcvoz/WilhemNet_86.h5?dl=1&quot"
file = "WilhemNet_86(1).h5"
r = urllib.request.urlopen(url)
f=open(file,"wb")
f.write(r.read())
f.close