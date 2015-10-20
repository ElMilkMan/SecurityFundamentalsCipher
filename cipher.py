#!/usr/bin/python
# Filename: cipher.py
from bitarray import bitarray #Import the BitArray Module (DO THIS ON ALL MACHINES)
import pickle

def inverse(bits):
	bitlist = list(bits)
	for i in range (0,16):
		bit = bitlist[i]
		if bit == "0":
			bit = "1"
		else:
			bit = "0"
		bitlist[i] = bit
	inversedbits = ''.join(bitlist)
	return inversedbits


def main():
	print("Welcome to group 12's cipher")
	#print("Please enter the path to the file you wish to Encrpyt")
	#fileName = raw_input()

	plainText=open("plain.txt",'r') #Takes the path given via user input and assigns the file to object "PlainText", in read mode.
        text = plainText.read()
        #print(text)

	#TODO: Remove as they are done
	#Implement Serialisation
	#Inverse method
	#P-BOX
	#S-BOX
	#Bit-Shift

	textBits = bitarray()
	textBits.frombytes("ab")
	print(textBits.to01())
	inversedbits = inverse(textBits.to01())
	print(inversedbits)
	#print(textBits.to01())



if __name__ == "__main__": main() #Defines the Main module as "Main" and not a library
