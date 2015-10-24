#!/usr/bin/python
# Filename: cipher.py
from bitarray import bitarray #Import the BitArray Module (DO THIS ON ALL MACHINES)
import pickle
import random
import string
import struct

#Returns the inversed bits
def inverse(block):
	#the list of the new bits
	bitlist = []
	#goes through every bit and inverses it
	for i in range (0,len(block)):
		bit = block[i]
		if bit:
			bit = False
		else:
			bit = True
		#the inversed bit gets assigned into the list
		bitlist.append(bit)
	return bitlist

#Slices the text into smaller portions (in order to be 16bits) and returns a list
def tolist(text):
	i = 0
	#the list of the portion of the text to get ecnrypted
	textlist = []
	#This loop goes through all the text and gets 2 letters per time
	while (i < len(text)):
		seq = ""
		if (i+2) > len(text):
			seq = (text[i]," ")
		else:
			seq = (text[i],text[i+1])
		var =  ''.join(seq)
		textlist.append(var)
		i = i+2
	return textlist

#XORes the block with the key
def XOR(block,key):
	#this list will hold the output of the xor
	output = []
	#this is were the XOR happens
	for i in range(0, len(block)):
		if block[i] == key[i]:
			output.append(False)
		else:
			output.append(True)
	return output

#It creates an initial vector for the purposes of CBC
def initialVector():
	key = ""
	for i in range(0,2):
		key = key+random.choice(string.ascii_letters)
	ba = bitarray()
	ba.fromstring(key)
	return ba.tolist()

#This is an extension PBOX which changes the order of the bits and adds more bits
#to make the cipher more complex
def PBoxEncrypt(block):
	#gets the PBOX dictionary
	pbox = getEncryptPBOXDict()
	#List were the new bits will be stored
	output = []
	#the process of changes the order of the block
	for i in range(0, len(pbox)):
		output.append(block[pbox[i]])
	#Changes the object from a list into one string
	return output

def PBoxDecrypt(block):
	#gets the PBOX dictionary
	pbox = getDecryptPBOXDict()
	#List were the new bits will be stored
	output = []
	#the process of changes the order of the block
	for i in range(0, len(pbox)):
		output.append(block[pbox[i]])
	#Changes the object from a list into one string
	return output


#Generates a dictionary which holds the sequence of the PBOX
def getEncryptPBOXDict():
	pbox = {
		0 : 7,
		1 : 3,
		2 : 5,
		3 : 12,
		4 : 8,
		5 : 12,
		6 : 1,
		7 : 6,
		8 : 4,
		9 : 15,
		10 : 13,
		11 : 7,
		12 : 9,
		13 : 3,
		14 : 9,
		15 : 10,
		16 : 6,
		17 : 11,
		18 : 5,
		19 : 13,
		20 : 0,
		21 : 2,
		22 : 14,
		23 : 1}
	return pbox

def getDecryptPBOXDict():
	pbox = {
		0 : 20,
		1 : 6,
		2 : 21,
		3 : 1,
		4 : 8,
		5 : 2,
		6 : 7,
		7 : 11,
		8 : 4,
		9 : 12,
		10 : 15,
		11 : 17,
		12 : 3,
		13 : 10,
		14 : 22,
		15 : 9}
	return pbox

#Shifts the bits of the block left or right and a specific number of steps
#The "left" parameter is a boolean and states if the rotation is happening to the left or the right
#The "rotation" parameter is an int and is the number of steps the bits will be shifted
def bitShift(block, left, rotation):
	#the list of the new bits
	output = []
	# If the rotation is towards the left
	if left:
		for i in range(0, len(block)):
			#n is the new position of bit i
			n = i-rotation
			#if n is below 0, the bit will be taken from the end of the list
			if n < 0:
				n = n+len(block)
			output.insert(n,block[i])
	#If the rotation is towards the right
	else:
		for i in range(0, len(block)):
			#n is the new position of bit i
			n = i+rotation
			#if n is greater than it goes at the beginning of the list
			if n > len(block)-1:
				n = n-len(block)
			output.insert(n,block[i])
	return output

#This is a 4-bit S-Box, it replaces 4-bit portions of the block with the correspoding one on the SBoxdict list
#Only encrypts
def SBoxEncrypt(block):
	sbox = getEncryptSBOXDict()
	output = []
	i = 0
	while (i<len(block)):
		#Gets the 4-bit portion
		bits =[]
		for x in range(0,4):
			bits.append(block[i+x])
		#forms it into a string
		strbits = "".join(bits)
		#finds the corresponding portion
		strbits = sbox[strbits]
		for x in range(0, len(strbits)):
			if strbits[x] == "1":
				output.append(True)
			else:
				output.append(False)
		i = i+4
	return output

#This is a 4-bit S-Box, it replaces 4-bit portions of the block with the correspoding one on the SBoxdict list
#Only decrypts
def SBoxDecrypt(block):
	sbox = getDecryptSBOXDict()
	output = []
	i = 0
	while (i<len(block)):
		#Gets the 4-bit portion
		bits =[]
		for x in range(0,4):
			bits.append(block[i+x])
		#forms it into a string
		strbits = "".join(bits)
		#finds the corresponding portion
		strbits = sbox[strbits]
		for x in range(0, len(strbits)):
			if strbits[x] == "1":
				output.append(True)
			else:
				output.append(False)
		i = i+4
	return output

#Returns the S-Box list
def getEncryptSBOXDict():
	sbox = {
		"0000" : "1011",#
		"0001" : "0100",#
		"0010" : "1010",#
		"0011" : "0110",#
		"0100" : "0000",#
		"0101" : "1111",
		"0110" : "0010",#
		"0111" : "1101",
		"1000" : '0011',#
		"1001" : "1110",
		"1010" : "0001",#
		"1011" : "1000",#
		"1100" : "0111",#
		"1101" : "1001",#
		"1110" : "0101",#
		"1111" : "1100"}
	return sbox

def getDecryptSBOXDict():
	sbox = {
		"0000" : "0100",
		"0001" : "1010",
		"0010" : "0110",
		"0011" : "1000",
		"0100" : "0001",
		"0101" : "1110",
		"0110" : "0011",
		"0111" : "1100",
		"1000" : "1011",
		"1001" : "1101",
		"1010" : "0010",
		"1011" : "0000",
		"1100" : "1111",
		"1101" : "0111",
		"1110" : "1001",
		"1111" : "0101"}
	return sbox

def writeCipherFile(cipher, filename):
	filenames = filename.split(".",1)
	cipherfile = open(filenames[0]+"_encrypted."+filenames[1],"wb")
	cipherfile.write(cipher)

#Encrypts the plain text into cipher
#The encryption algorithm is:
#Inversion>circle shift (5 to the left)>S-Box>XOR>Ext PBOX>Inversion>S-Box>circle shift (2 to the right)
def encrypt(text, filename, key):
	textlist = tolist(text)
	# key = initialVector()
	cipherlist = []
	for i in range(0, len(textlist)):
		textBits = bitarray()
		textBits.fromstring(textlist[i])
		textBits = bitarray(inverse(textBits.tolist()))
		textBits = bitarray(bitShift(textBits, True, 5))
		textBits = bitarray(SBoxEncrypt(bitarray(textBits).to01()))
		# print textBits.to01()
		if i == 0:
			textBits = bitarray(XOR(textBits.tolist(),key))
		else:
			textBits = bitarray(XOR(textBits,cipherlist[-1]))
		textBits = bitarray(PBoxEncrypt(textBits))
		textBits = bitarray(inverse(textBits.tolist()))
		textBits = bitarray(SBoxEncrypt(bitarray(textBits).to01()))
		textBits = bitarray(bitShift(textBits, False, 2))
		cipherlist.append(textBits.tolist())
	completeCipher = []
	for row in cipherlist:
		for item in row:
			completeCipher.append(item)
	ba = bitarray(completeCipher)
	writeCipherFile(ba.tobytes(), filename)
	print("Key to decrypt: "+bitarray(key).tostring())

#Decryption function
#Circle shift (2 to the left)>S-Box>Inversion>Ext P-Box>XOR>S-Box>circle shift (5 to the right)>Inversion
def decrypt(key):
	cipherText = open("plain_encrypted.txt","rb")
	text = cipherText.read()
	charlist = struct.unpack("s" * ((len(text))), text)
	i = len(charlist)-1
	textlist = []
	while (i > 1):
		cipherBits = bitarray()
		cipherBits.frombytes(charlist[i-2]+charlist[i-1]+charlist[i])
		cipherBits = bitarray(bitShift(cipherBits, True, 2))
		cipherBits = bitarray(SBoxDecrypt(cipherBits.to01()))
		cipherBits = bitarray(inverse(cipherBits.tolist()))
		cipherBits = bitarray(PBoxDecrypt(cipherBits))
		if i < 3:
			cipherBits = bitarray(XOR(cipherBits.tolist(),key))
		else:
			ba  = bitarray()
			ba.frombytes(charlist[i-5]+charlist[i-4]+charlist[i-3])
			cipherBits = bitarray(XOR(cipherBits.tolist(),ba.tolist()))
		# print cipherBits.to01()
		cipherBits = bitarray(SBoxDecrypt(cipherBits.to01()))
		cipherBits = bitarray(bitShift(cipherBits, False, 5))
		cipherBits = bitarray(inverse(cipherBits.tolist()))
		i = i - 3
		textlist.append(cipherBits.tobytes())
	x = len(textlist)-1
	text = ""
	while(x > 0):
		text = text + textlist[x]
		x = x - 1
	print text

def writeTextFile(cipher, filename):
	filenames = filename.split(".",1)
	cipherfile = open(filenames[0]+"_decrypted."+filenames[1],"wb")
	cipherfile.write(cipher)

def main():
	print("Welcome to group 12's cipher")
	#print("Please enter the path to the file you wish to Encrpyt")
	#fileName = raw_input()

	plainText=open("plain.txt",'rb') #Takes the path given via user input and assigns the file to object "PlainText", in read mode.
        text = plainText.read()

	#TODO: Remove as they are done
	#Implement Serialisation
	#Expansion P-BOX (16-bit -> 24-bit)
	#S-BOX (4-bit)
	#Bit-Shift (Swift)
	key = initialVector()
	# XOR("10110010","100011011")
	encrypt(text, "plain.txt", key)
	decrypt(key)

if __name__ == "__main__": main() #Defines the Main module as "Main" and not a library
