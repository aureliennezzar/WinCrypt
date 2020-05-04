from init_functions import col_print
import random
import binascii
import base64
import sys


def update_progress(progress,total,text):
	progress = 100 * (progress / float(total))
	sys.stdout.write('\r\033[0;33m{2} [{0}] {1}%'.format('#'*(int(progress)/10), int(progress),text))
	sys.stdout.flush()

def win_encrypt(data,key):
	from explorer import return_main
	loading, encrypted ="",""
	try:
		key = "".join([format(ord(char),'#010b')[2:] for char in key])
		data = "".join([format(ord(char),'#010b')[2:] for char in data])
	except:
		col_print(errors_list[0])
		col_print("\nWHPress $RENTER $WHto continue... ")
		raw_input("")
		return_main()
	totaldata = len(data)/8
	if totaldata >= 100000:
		loading = True
		loadcount = 0
	keyvals, datavals , secretvals, encryptlist = [],[], [],[]
	k_char = 0
	for i in range(2):
		if i<1:
			crypt_data = data
		for bit in range(len(crypt_data)+1):
			if bit%4==0 and bit !=0 or bit==len(crypt_data):
				bits= crypt_data[bit-4:bit]
				encryptlist.append(int(bits,2))
			if loading and i<1 and bit%20480==0:
				loadcount+=1
				update_progress(loadcount,totaldata/2560,"  Collecting data (1/2)...")
		if i<1:
			datavals = encryptlist
			encryptlist = []
			bits = ""
			crypt_data = key
		else:
			keyvals = encryptlist
	if loading:
		print("\n")
		totaldata,loadcount = len(datavals),0

	for val in range(len(datavals)):
		encrypted+= chr( int(datavals[val]) + int(keyvals[k_char]) )
		if loading and val%16384==0:
			loadcount+=1
			update_progress(loadcount,totaldata/16384,"  Encrypting data (2/2)...")
		if k_char != len(keyvals)-1:
			k_char+=1
		else:
			k_char=0
	if loading:
		print("\n")
	return encrypted.replace("\n","0").replace("\r","1")

def win_decrypt(data, key):
	from explorer import return_main
	loading, decrypted ="",""
	try:
		key = "".join([format(ord(char),'#010b')[2:] for char in key])
	except:
		col_print(errors_list[0])
		col_print("\nWHPress $RENTER $WHto continue... ")
		raw_input("")
		return_main()
	data = list(data.replace("\n","").replace("0","\n").replace("1","\r"))
	keyvals = []
	k_char=0
	totaldata = len(data)
	if totaldata >= 100000:
		loading = True
		loadcount = 0
	for bit in range(len(key)+1):
		if bit%4==0 and bit !=0 or bit==len(key):
			bits= key[bit-4:bit]
			keyvals.append(int(bits,2))
	k_char=0
	for char in range(len(data)):
		decrypted += bin(ord(data[char]) - int(keyvals[k_char]))[2:].zfill(4)
		if loading and char%16384==0:
			loadcount+=1
			update_progress(loadcount,totaldata/16384,"[*] Decrypting data ...")
		if k_char != len(keyvals)-1:
			k_char+=1
		else:
			k_char=0
	try:
		decrypted = binascii.unhexlify('%x' % int('0b' + '{}'.format(decrypted), 2))
		return decrypted.replace("{{null}}", "\x00")
		
	except:
		col_print("$R[!] Error, Binary data corrupted !")
		col_print("\nWHPress $RENTER $WHto continue... ")
		raw_input("")
		return_main()