import urllib2
import sys





TARGET = 'http://crypto-class.appspot.com/po?er='
CIPHER_STRING = "f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4"
CIPHER = 0xf20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4
CIPHER_LENGTH = len(CIPHER_STRING)
BLOCK_SIZE = 16
BYTE_SIZE = 8
TEXT_RANGE = range(256)



#--------------------------------------------------------------
# padding oracle
#--------------------------------------------------------------
class PaddingOracle(object):
    def query(self, q):
        target = TARGET + urllib2.quote(q)    # Create query URL
        req = urllib2.Request(target)         # Send HTTP request to server
        try:
            f = urllib2.urlopen(req)          # Wait for response
        except urllib2.HTTPError, e:
            #print "We got: %d" % e.code       # Print response code
            if e.code == 404:
                return True # good padding
            return False # bad padding

#--------------------------------------------------------------
#PaddingOracle
#if cipher is updated to
#(the byte of cipher) xor (the byte of original message) xor (padding)
#after decryption, the original message will be updated to
#(the byte of original message) xor [(the byte of original message)] xor (padding)
#which is
#(padding).
#However,
#if it is the last few bytes, and the original message is also padded.
#(the byte of original message) xor [(padding)] xor (padding) = (the byte of original message)
#it also works.
#Note that in the description above, the text in [] is the text we try.
#--------------------------------------------------------------

#--------------------------------------------------------------
#Function: generatePadding
#Input value:
#   padding_order: padding_order stands for the number of how many of the last bytes are padding.
#Return value: padding
#e.g. paddingOrder = 1, padding 0x01
#     paddingOrder = 2, padding 0x0202
#--------------------------------------------------------------
def generatePadding(padding_order):
    j = 0
    padding = 0
    padding_number = padding_order + 1
    while j < padding_number:
        padding = padding << BYTE_SIZE
        padding += padding_number
        j += 1
    return padding

#--------------------------------------------------------------
#Function: guessOriginalByteText
#Input value:
#   padding:
#   padding_order:
#   block_order: indicate which block we are decrypting:
#       (CIPHER_LENGTH/BLOCK_SIZE) - (block_order + 1)
#   text_guess:
#       from 0 to 256
#Return value: True or False
#   True if the text_guess satisify the padding oracle
#--------------------------------------------------------------
def guessOriginalByteText(padding, padding_order, block_order, byte_guess, this_block_hex):
    po = PaddingOracle()
    #Here padding start from 0x01
    temp_byte_hex_guess = byte_guess << (BYTE_SIZE*(padding_order))
    #Here we process block from the second last
    temp_cipher = CIPHER>>(block_order*BLOCK_SIZE*BYTE_SIZE)
    temp_guess= (temp_byte_hex_guess^padding^this_block_hex) << (BLOCK_SIZE*BYTE_SIZE)
    target_guess = temp_cipher^temp_guess

    target_guess_string = hex(target_guess)
    target_guess_string = target_guess_string[2:(len(target_guess_string)-1)]
    return po.query(target_guess_string)

#--------------------------------------------------------------
#Function: determineOrignalTextInBlock
#Input value:
#   block_order: indicate which block we are decrypting:
#       (CIPHER_LENGTH/BLOCK_SIZE) - (block_order + 1)
#Return value: The original text ascii value of this block.
#--------------------------------------------------------------
def determineOrignalTextInBlock(block_order):
    this_block_hex = 0
    this_block_str = ""
    #this_block_cipher = ( CIPHER >> (block_order * BLOCK_SIZE * BYTE_SIZE) ) & bytesOfOne(BLOCK_SIZE)
    #--------------------variables used for verification need case---------------------#
    #vn_bool = {}
    #vn_byte_hex_guess_success = {}

    for padding_order in range(BLOCK_SIZE):
    #for padding_order in range(3):
        padding = generatePadding(padding_order)
        byte_hex_guess_success_times = 0
        byte_hex_guess_success = []
        #Guess original text of each byte from 0 to 0xFF
        for byte_hex_guess in TEXT_RANGE:
            byte_hex_guess_bool = guessOriginalByteText(padding, padding_order, block_order, byte_hex_guess, this_block_hex)
            if byte_hex_guess_bool:
                byte_hex_guess_success_times += 1
                byte_hex_guess_success.append(byte_hex_guess)

        print ("correct result",byte_hex_guess_success_times)
        if (byte_hex_guess_success_times > 1):
            this_block_hex = this_block_hex
        elif (byte_hex_guess_success_times == 1):
            this_block_hex = this_block_hex^(byte_hex_guess_success[0]<<(padding_order*BYTE_SIZE))
            this_block_str = chr(byte_hex_guess_success[0]) + this_block_str
        else:
            this_block_hex = this_block_hex^(9<<(padding_order*BYTE_SIZE))

    return this_block_str


#---------------------------MAIN--------------------------#
decrypt_result = ""
for block_order in range(CIPHER_LENGTH/BLOCK_SIZE):
    decrypt_result += determineOrignalTextInBlock(block_order)
    print decrypt_result

"""
if __name__ == "__main__":
    po = PaddingOracle()
    po.query(sys.argv[1])       # Issue HTTP query with the given argument
"""
