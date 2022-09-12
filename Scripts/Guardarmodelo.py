import urllib.request
url = "https://www.mediafire.com/file/zu3kdqjd338rr4t/WilhemNet_86%25281%2529.h5/file"
file = "WilhemNet_86(1).h5"
r = urllib.request.urlopen(url)
f=open(file,"wb")
f.write(r.read())
f.close