from Crypto.Hash import SHA256
import os

bsize=1024
fname='b.mp4'
fhand=open(fname,'rb')
lastsize=os.stat(fname).st_size%bsize
fhand.seek(-lastsize, 2)
block_n=fhand.read(lastsize)
h=SHA256.new()
h.update(block_n)
fhand.seek(-lastsize, 1)
while fhand.tell()>0:
    fhand.seek(-bsize,1)
    block=fhand.read(bsize)+h.digest()
    h=SHA256.new()
    h.update(block)
    fhand.seek(-bsize,1)
print h.hexdigest()
