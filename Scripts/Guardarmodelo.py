import urllib.request
url = "https://drive.google.com/file/d/1IRctNklwe2Aa2dBRK32nYGtS7xtJ1CXr/view?usp=sharing"
file = "WilhemNet_86(1).h5"
r = urllib.request.urlopen(url)
f=open(file,"wb")
f.write(r.read())
f.close