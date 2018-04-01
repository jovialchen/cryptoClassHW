import gmpy2
from gmpy2 import mpz

p = 13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031858186486050853753882811946569946433649006084171
g = 11717829880366207009516117596335367088558084999998952205599979459063929499736583746670572176471460312928594829675428279466566527115212748467589894601965568
h = 3239475104050450443565264378728065788649097520952449527834792452971981976143292558073856937958553180532878928001494706097394108577585732452307673444020333
B = 2**20
gB = gmpy2.powmod(g,B,p)
x1_tbl = {}
# build table for x1
for x1 in range(B):
    gx1 = gmpy2.powmod(g,x1,p)
    temp = gmpy2.divm(h, gx1, p)
    x1_tbl[temp]=x1

for x0 in range(B):
    temp = gmpy2.powmod(gB,x0,p)
    x1 = x1_tbl.get(temp, None); 
    if x1:
        temp = B*x0+x1
        print temp
        break