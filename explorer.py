from init_functions import col_print, winch
from crypt import win_encrypt, win_decrypt
from PIL import Image, ImageSequence
import getpass
import os
import random
global fpswd

fpswd = '<WinCrypt>'

def WinCrypt(pswd):
	global folder
	while True:
		os.system("clear"); winch(70,15)
		col_print("""$B[$RWinCrypt $YLv1.5.1$B]                                        $B~ $RBy Strak $B~
$G             
   __      __ .__         _________                            __   
  /  \\    /  \\|__|  ____  \\_   ___ \\ _______  ___.__.______  _/  |_ 
  \\   \\/\\/   /|  | /    \\ /    \\  \\/ \\_  __ \\<   |  |\\____ \\ \\   __\\\\
   \\        / |  ||   |   \\\\     \\____ |  | \\/ \\___  ||  |_> > |  |  
    \\__/\\  /  |__||___|  / \\______  / |__|    / ____||   __/  |__|  
         \\/            \\/         \\/          \\/     |__|
                                                         $LG1.5

        $LCY1$B. Open a folder
                                                   $LCY0$B. Quit
          $LCY2$B. Create a folder

""")
		try:
			WinCrypt = input()
		except:
			pass

		if WinCrypt==1:
			#EXPLORE FOLDER
			col_print("$YL[*] Insert folder.wc here $ "); WinCrypt = raw_input()
			if "'/" in WinCrypt:
				WinCrypt = WinCrypt[1:-2]
			enctest = open(WinCrypt, "r")
			enctest = enctest.readlines()
			if "<enc>" in enctest[0]:
				col_print("$R[*] Password $ ")
				pswd = getpass.getpass("")
			Explorer(WinCrypt,pswd)

		if WinCrypt==2:
			#CREATE FOLDER
			bal = ""
			while True:
				col_print("$YL[*] Folder name $ "); foldername = raw_input()
				foldername = "{}.wc".format(foldername)
				exists = os.path.isfile(foldername)
				if exists:
					col_print("$R[!] Error, '{}' already exist...".format(foldername))
				else:
					break
			folder = open(foldername, "w")
			col_print("$YL[*] Add password ? (y/n) $ "); mode_secuR = raw_input()
			if mode_secuR =="y":
				col_print("$R[*] Password $ ")
				pswd = getpass.getpass("")
				bal = "<enc>"
			folderinfos = "-{}-WinCrypt\n".format(foldername[:-3])
			folder.write("{}".format(bal) + win_encrypt(folderinfos, pswd))
			folder.close() ; folder = ""
			Explorer(foldername,pswd)

		if WinCrypt==0:
			exit()

def Explorer(folderxname,pswd):
	errors_list = [
	'$R[!] Error, ASCII data corrupted !',
	'$R[!] Error, its has to be a file!\n',
	'$R[!] Error, you have to write a number !\n',
	'$R[!] Error, this file dont exists, try again...\n']
	while True:
		col_print("\n$YL[*] Loading explorer...\n")
		bal = ""
		allfiles = ""
		blank = ""
		blank2 = ""
		data = ""
		file_start = ""
		file_num = 0
		winch_val = 0
		files_names, files_sizes = [], []
		folder = open(folderxname, "r+")
		data = folder.readlines()
		if "<enc>" in data[0]:
			blank2 = "~  $B[$GSecured Mode$B]"
			infoline = data[0][5:]
		else:
			infoline = data[0]
		infoline = win_decrypt(infoline,pswd)
		try:
			if not "WinCrypt" in infoline:
				col_print("$R[!] Error, Folder corrupted !")
				col_print("\n$WHPress $RENTER $WHto continue... ")
				raw_input("")
				WinCrypt(fpswd)
		except:
			col_print("$R[!] Error, wrong pswd or folder corrupted !")
			col_print("\n$WHPress $RENTER $WHto continue... ")
			raw_input("")
			WinCrypt(fpswd)
		
		foldername = infoline.split("-")[1]
		if not len(data[1:]):
			blank = "[!] Folder empty..."
		data = data[1:]
		for line in range(len(data)):
			if "<file:" in data[line]:
				file_num+=1
				file_start = data[line].split(">")[0].split(":")
				files_names.append(win_decrypt(file_start[1],pswd))
				files_sizes.append(win_decrypt(file_start[2],pswd))
		if len(files_names)>=25:
			winch_val=25
		else:
			winch_val= len(files_names)
		file_name = False
		if file_num:
			for file in range(file_num):
				if file+1<10:
					oblank = "0"
				else:
					oblank = ""
				if "(" in files_names[file] and ")" in files_names[file]:
					file_name = True
				if "[" in files_names[file] and "[" in files_names[file]:
					file_name = True
				if ".png" in files_names[file] or ".jpg" in files_names[file] or ".jpeg" in files_names[file]:
					col_file = "$B"
				elif ".avi" in files_names[file] or ".mp4" in files_names[file]:
					col_file = "$LPRP"
				elif ".gif" in files_names[file]:
					col_file = "$PRP"
				elif ".txt" in files_names[file] or ".py" in files_names[file] or ".sh" in files_names[file]:
					col_file = "$LGR"
				else:
					col_file = "$WH"
				if file_name:
					col_inbr = "$WH"
					file_name = files_names[file].replace("[","$WH[$BRW").replace("]","$WH]{}".format(col_file)).replace("(","$DGR({}".format(col_inbr)).replace(")","$DGR){}".format(col_file))
				else:
					file_name = files_names[file]
				allfiles+=" $B[$LCY{0}$B] {3} {1}  $WH($BRW{2}$WH)\n".format(oblank + str(file+1),file_name, files_sizes[file],col_file)

		os.system("clear")
		winch(80,12+winch_val)
		col_print("""$B[Explorer]$R WinCrypt v1.5  $B~  [$YL{0}$B]  {2}
$B - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                                    $B|$WHFiles$B|

$DGR{1}{3}


$B - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

               ($LCYA$B)dd    ($LCYD$B)el    ($LCYE$B)xport    ($LCYR$B)ead   ($LCYQ$B)uit

$WH $ """.format(foldername.replace("'","\\'").replace('(',"\\(").replace(')',"\\)").replace('"','\\"'),blank,blank2,allfiles))
		menu_Explorer = raw_input()



########################################################    A  IS PRESSED   ######################################################## 
		if menu_Explorer=="A" or menu_Explorer=="a":
			while True:
				try:
					col_print("$YL[*] Insert file here $ ")
					filetoadd = input()
					open(filetoadd,"r")
					break
				except:
					col_print(errors_list[1])
					pass
			file_size = os.path.getsize(filetoadd)
			if file_size<1000000:
				file_size = "{0} kB".format(round(float(file_size)/1000,1))
			elif file_size>=1000000 and file_size<1000000000:
				file_size = "{0} MB".format(round(float(file_size)/1000000,1))
			elif file_size>=1000000000:
				file_size = "{0} GB".format(round(float(file_size)/1000000000,1))
			file = open(filetoadd, "r")
			filetoadd = filetoadd.split("/")
			filetoadd = filetoadd[-1]
			if filetoadd in files_names:
				col_print("$R[!] Error, {} already exists !\n".format(filetoadd))
				col_print("$YL[*] Rename file $ ")
				filetoadd = raw_input()
			file = file.readlines()
			file[0] = file[0].replace("\x00", "{{null}}")
			file = "".join(file)
			col_print("$YL[*] Encrypting file...\n")
			filetoadd =  win_encrypt(filetoadd,pswd)
			file_size =  win_encrypt(file_size,pswd)
			file = win_encrypt(file,pswd)
			folder.write("\n<file:{0}:{2}>\n{1}\n<end_file:{0}>".format(filetoadd,file,file_size))
			folder.close() ; folder = ""
########################################################    D  IS PRESSED   ######################################################## 
		if menu_Explorer=="D" or menu_Explorer=="d":
			start_line, end_line = 0,0
			while True:
				col_print("$YL[*] Wich file do you want to delete ? $ ")
				filetodel = raw_input()
				try:
					int(filetodel)/2
				except:
					col_print(errors_list[2])
					pass
				if int(filetodel)<=len(files_names):
					filetodel = files_names[int(filetodel)-1]
					break
				else:
					col_print(errors_list[3])

			col_print("$YL[*] Deleting file...\n")
			efiletodel = win_encrypt(filetodel,pswd)
			for line in range(len(data)):
				if "<file:{}".format(efiletodel) in data[line]:
					start_line = line
				if "<end_file:{}".format(efiletodel) in data[line]:
					end_line = line
			data = data[:start_line] + data[end_line+1:]
			if pswd!="<WinCrypt>":
				bal = "<enc>"
			folderinfos = win_encrypt("-{}-WinCrypt\n".format(foldername), pswd)
			folder.close()
			folder = open(folderxname, "w+")
			folder.write("{}".format(bal) + folderinfos)
			if len(files_names)!=1:
				data = "\n"+"".join(data)
				folder.write(data)
			folder.close() ; folder = ""
########################################################    E  IS PRESSED   ######################################################## 
		if menu_Explorer=="E" or menu_Explorer=="e":
			outputexp=[]
			save_line = False
			start_line, end_line = 0,0
			while True:
				col_print("$YL[*] Wich file do you want to export ? $ ")
				filetoexp = raw_input()
				try:
					int(filetoexp)/2
				except:
					col_print(errors_list[2])
				if int(filetoexp)<=len(files_names):
					filetoexp = files_names[int(filetoexp)-1]
					break
				else:
					col_print(errors_list[3])
			col_print("$YL[*] Exporting file...\n")

			efiletoexp = win_encrypt(filetoexp,pswd)
			for line in range(len(data)):
				if "<file:{}".format(efiletoexp) in data[line]:
					start_line = line
				if "<end_file:{}".format(efiletoexp) in data[line]:
					end_line = line
			outputexp = data[start_line+1:end_line]
			#Enlever dernier saut de ligne
			outputexp = win_decrypt("".join(outputexp),pswd)
			col_print("\n$YL[*] Output name ? $ ")
			filetoexp = raw_input()
			filetoexp = open(filetoexp, "w")
			filetoexp.write(outputexp)
			filetoexp.close()

########################################################    R  IS PRESSED   ######################################################## 
		if menu_Explorer=="R" or menu_Explorer=="r":
			read_loop = False
			outputexp=[]
			save_line = False
			start_line, end_line = 0,0
			while True:
				col_print("$YL[*] Wich file do you want to read ? $ ")
				filetoread = raw_input()
				try:
					int(filetoread)/2
				except:
					col_print(errors_list[2])
					break
				if int(filetoread)<=len(files_names):
					filetoread = files_names[int(filetoread)-1]
				else:
					col_print(errors_list[3])
				if ".txt" in filetoread or ".png" in filetoread or ".jpg" in filetoread or ".jpeg" in filetoread or ".py" in filetoread or ".avi" in filetoread  or ".mp4" in filetoread or ".gif" in filetoread:

					efiletoread = win_encrypt(filetoread,pswd)
					for line in range(len(data)):
						if "<file:{}".format(efiletoread) in data[line]:
							start_line = line
						if "<end_file:{}".format(efiletoread) in data[line]:
							end_line = line
					dataToRead = data[start_line+1:end_line]

					if ".png" in filetoread or ".jpg" in filetoread or ".jpeg" in filetoread:
						col_print("$YL[*] Reading image... \n")
						rgb = range(0,255)
						imgexpn="{}.png".format(random.choice(range(999999)))
						imgToWrite = win_decrypt("".join(dataToRead),pswd)
						imgToRead = open(imgexpn, "w")
						imgToRead.write(imgToWrite); imgToRead.close()

						imgToRead = Image.open(imgexpn)
						imgToRead.show()
						
						ReadPix =  imgToRead.load()
						for y in range(0, imgToRead.size[1]):
						    for x in range(0, imgToRead.size[0]):
						        ReadPix[x,y] = (random.choice(rgb),random.choice(rgb),random.choice(rgb))
						imgToRead = imgToRead.resize((420,420))
						imgToRead.save(imgexpn)
						os.rename(imgexpn, "0.bash")
						os.remove("0.bash")

					if ".avi" in filetoread or ".mp4" in filetoread or ".gif" in filetoread:
						videxpn = random.choice(range(999999))
						if ".avi" in filetoread :
							videxpn="{}.avi".format(videxpn)
						elif ".mp4" in filetoread:
							videxpn="{}.mp4".format(videxpn)
						elif ".gif" in filetoread:
							videxpn="{}.gif".format(videxpn)
						
						vidToWrite = win_decrypt("".join(dataToRead),pswd)
						vidToRead = open(videxpn, "w")
						vidToRead.write(vidToWrite); vidToRead.close()
						if ".avi" in filetoread or ".mp4" in filetoread:
							ReadVideo(videxpn)
						elif ".gif" in filetoread :
							ReadGif(videxpn)
						vidToRead = open(videxpn, "w+")
						vidToRead.write(str(random.choice(range(999999))))
						vidToRead.close()
						os.rename(videxpn, "0.bash")
						os.remove("0.bash")

					if ".txt" in filetoread or ".py" in filetoread:
						col_print("$YL[*] Reading file... \n")
						strToRead = win_decrypt("".join(dataToRead),pswd)

						if len(strToRead.split("\n"))>=30:
							winch_val=30
						else:
							winch_val= len(strToRead.split("\n"))
						while True:
							os.system('clear')
							winch(100,14+int(winch_val))
							col_print("""$B[Reader]$R WinCrypt v1.5  $B~  [$YL{0}$B]
$B - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

$WH{1}

$B - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

	($LCYB$B)ack
""".format(filetoread,strToRead))
							col_print(" $ ")
							menu_Read = raw_input()
							if menu_Read=="B" or menu_Read=="b":
								Explorer(folderxname, pswd)

				else:
					col_print("$R[!] Error, {} can't be read ! ...\n".format(filetoread))
					col_print("$WHPress $RENTER $WHto continue... ");raw_input("")
				folder.close() ; folder = ""
				if not read_loop:
					break


########################################################    Q  IS PRESSED   ######################################################## 
		if menu_Explorer=="Q" or menu_Explorer=="q" or menu_Explorer=="0" or menu_Explorer=="b" or menu_Explorer=="B":
			WinCrypt(fpswd)


def return_main():
	WinCrypt(fpswd)