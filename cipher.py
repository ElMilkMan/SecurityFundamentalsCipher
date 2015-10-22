#!/usr/bin/python
# Filename: cipher.py
from bitarray import bitarray #Import the BitArray Module (DO THIS ON ALL MACHINES)
import pickle
import random

#Returns the inversed bits
def inverse(block):
	#the list of the new bits
	bitlist = []
	#goes through every bit and inverses it
	for i in range (0,len(block)):
		bit = block[i]
		if bit == "0":
			bit = "1"
		else:
			bit = "0"
		#the inversed bit gets assigned into the list
		bitlist.append(bit)
	#The list gets assembled into a block again
	inversedbits = ''.join(bitlist)
	return inversedbits

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
	#create a list of the key
	keylist = list(key)
	#this list will hold the output of the xor
	output = []
	#this is were the XOR happens
	for i in range(0, len(block)):
		if block[i] == keylist[i]:
			output.append("0")
		else:
			output.append("1")
	#This output of the xor gets assembled into one 16-bit block
	xoredbits = ''.join(output)
	return xoredbits

#It creates an initial vector for the purposes of CBC
def initialVector():
	#The array that will store the bits for now
	vector = []
	#randomly generate bits 16 times in order to create the 16-bit vector
	for i in range(0,16):
		var  = bool(random.getrandbits(1))
		if var:
			vector.append("1")
		else:
			vector.append("0")
	#final assembly of the vector
	key = ''.join(vector)
	return key

#This is an extension PBOX which changes the order of the bits and adds more bits
#to make the cipher more complex
def PBox(block):
	#gets the PBOX dictionary
	pbox = getPBOXDict()
	#List were the new bits will be stored
	newblock = []
	#the process of changes the order of the block
	for i in range(1,25):
		newblock.append(block[pbox[i]])
	#Changes the object from a list into one string
	output = ''.join(newblock)
	return output

#Generates a dictionary which holds the sequence of the PBOX
def getPBOXDict():
	pbox = {
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
		23 : 1,
		24 : 7}
	return pbox

#Shifts the bits of the block left or right and a specific number of steps
#The "left" parameter is a boolean and states if the rotation is happening to the left or the right
#The "rotation" parameter is an int and is the number of steps the bits will be shifted
def bitShift(block, left, rotation):
	#the list of the new bits
	newblock = []
	# If the rotation is towards the left
	if left:
		for i in range(0, len(block)):
			#n is the bit that goes to position i
			n = i-rotation
			#if n is below 0, the bit will be taken from the end of the list
			if n < 0:
				n = n+len(block)
			newblock.append(block[n])
	#If the rotation is towards the right
	else:
		for i in range(0, len(block)):
			#n is the new position of bit i
			n = i+rotation
			#if n is greater than it goes at the beginning of the list
			if n > 0:
				n = n-len(block)
			newblock.insert(n,block[i])
	output = ''.join(newblock)
	return output

#This is a 4-bit S-Box, it replaces 4-bit portions of the block with the correspoding one on the SBoxdict list
def SBox(block):
	sbox = getSBOXDict()
	output = ""
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
		#adds it to the new block
		output = output+strbits
		i = i+4
	return output

#Returns the S-Box list
def getSBOXDict():
	sbox = {
		"0000" : "1011",
		"0001" : "0100",
		"0010" : "1010",
		"0011" : "0110",
		"0100" : "0000",
		"0101" : "1111",
		"0110" : "0010",
		"0111" : "1101",
		"1000" : '0011',
		"1001" : "1110",
		"1010" : "0001",
		"1011" : "1000",
		"1100" : "0111",
		"1101" : "1001",
		"1110" : "0101",
		"1111" : "1100"}
	return sbox

def main():
	print("Welcome to group 12's cipher")
	#print("Please enter the path to the file you wish to Encrpyt")
	#fileName = raw_input()

	plainText=open("plain.txt",'r') #Takes the path given via user input and assigns the file to object "PlainText", in read mode.
        text = plainText.read()
        #print(text)

	#TODO: Remove as they are done
	#Implement Serialisation
	#Expansion P-BOX (16-bit -> 24-bit)
	#S-BOX (4-bit)
	#Bit-Shift (Swift)


	textlist = tolist(text)
	key = initialVector()
	#Code for testing purposes
	#for block in textlist:
		#textBits = bitarray()
		#textBits.frombytes(block)
		#print("before: "+textBits.to01())
		#inversedbits = XOR(textBits.to01(),key)
		#print("after : "+inversedbits)
	textBits = bitarray()
	textBits.frombytes(textlist[0])
	block = textBits.to01()
	print("Original : "+block)
	block = inverse(block)
	print("Inverse  : "+block)
	block = XOR(block,key)
	print("Key      : "+key)
	print("XOR      : "+block)
	block = PBox(block)
	print("Ext PBOX : "+block)
	block = bitShift(block, True, 3)
	print("3L Shisft: "+block)
	block = SBox(block)
	print("S-Box    : "+block)

if __name__ == "__main__": main() #Defines the Main module as "Main" and not a library
