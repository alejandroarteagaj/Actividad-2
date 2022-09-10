##Script para cargar modelo en dicker
import urllib.request
url = "https://www.dropbox.com/s/yx6n606i7cfcvoz/WilhemNet_86.h5?dl=1&quot"

r = urllib.request.urlopen(url)

f.write(r.read())
f.close
