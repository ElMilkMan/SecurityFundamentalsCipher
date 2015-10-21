#!/usr/bin/python
# Filename: cipher.py
from bitarray import bitarray #Import the BitArray Module (DO THIS ON ALL MACHINES)
import pickle
import random

#Returns the inversed bits
def inverse(block):
	#creates a list of the bits of the block
	bitlist = list(block)
	#goes through every bit and inverses it
	for i in range (0,len(block)):
		bit = bitlist[i]
		if bit == "0":
			bit = "1"
		else:
			bit = "0"
		#the inversed bit gets assigned into the list
		bitlist[i] = bit
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
	#creates a list of block
	blocklist = list(block)
	#create a list of the key
	keylist = list(key)
	#this list will hold the output of the xor
	output = []
	#this is were the XOR happens
	for i in range(0, len(block)):
		if blocklist[i] == keylist[i]:
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

def main():
	print("Welcome to group 12's cipher")
	#print("Please enter the path to the file you wish to Encrpyt")
	#fileName = raw_input()

	plainText=open("plain.txt",'r') #Takes the path given via user input and assigns the file to object "PlainText", in read mode.
        text = plainText.read()
        #print(text)

	#TODO: Remove as they are done
	#Implement Serialisation
	#P-BOX
	#S-BOX
	#Bit-Shift


	textlist = tolist(text)
	key = initialVector()
	#Code for testing purposes
	for block in textlist:
		textBits = bitarray()
		textBits.frombytes(block)
		print("before: "+textBits.to01())
		inversedbits = XOR(textBits.to01(),key)
		print("after : "+inversedbits)





if __name__ == "__main__": main() #Defines the Main module as "Main" and not a library
