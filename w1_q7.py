msg1 = "attack at dawn"
cipher1 = "09e1c5f70a65ac519458e7e53f36"
cipher1 = int (cipher1,16)
print "cipher1 "+ hex(cipher1)
eorig = 0
for ch in msg1:
	eorig *= 256
	eorig += ord(ch)

print "eorig   "+hex(eorig)
key = eorig^cipher1
msg2 = "attack at dusk"
eterm = 0
for ch in msg2:
	eterm *= 256
	eterm += ord(ch);

print "eterm   "+ hex(eterm)
cipher2 = eterm^key
print "cipher2 "+ hex(cipher2)
