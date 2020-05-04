import os
import cv2
import datetime
import imageio
def winch(x,y):
	col,lin = x,y
	os.system("printf '\\e[8;{0};{1}t'".format(lin,col))

def getdate():
	date = str(datetime.datetime.now()).split(" ")
	hour = date[1][:8]
	date = date[0]
	return date, hour

def col_print(arg):
	colors_names = [
	"BLK",
	"R",
	"G",
	"BRW",
	"B",
	"PRP",
	"CY",
	"LGR",
	"DGR",
	"LR",
	"LG",
	"YL",
	"LB",
	"LPRP",
	"LCY",
	"WH"]
	colors =  "BLK='\033[0;30m';R='\033[0;31m';G='\033[0;32m';BRW='\033[0;33m';B='\033[0;34m';PRP='\033[0;35m';CY='\033[0;36m';LGR='\033[0;37m';DGR='\033[1;30m';LR='\033[1;31m';LG='\033[1;32m';YL='\033[1;33m';LB='\033[1;34m';LPRP='\033[1;35m';LCY='\033[1;36m';WH='\033[1;37m';NC='\033[0m';"

	for name in range(len(colors_names)):
		arg = arg.replace("${}".format(colors_names[name]), "${{{}}}".format(colors_names[name]))
	commandline = colors + "printf \"{}${{NC}}\"".format(arg)
	os.system(commandline)

def ReadVideo(videoname):
	rv_leave = False
	col_print("\n$YL[*] $WHPress $LRQ$WH to leave ")
	while rv_leave==False:
		cv2.namedWindow(videoname)
		cv2.startWindowThread()
		cap = cv2.VideoCapture(videoname)
		while cv2.getWindowProperty(videoname, 0) >= 0:
			ret, frame = cap.read()
			if not ret:
				break
			cv2.imshow(videoname,frame)
			if cv2.waitKey(30) & 0xFF == ord('q') :
				rv_leave = True
				break
		cap.release()
		cv2.destroyAllWindows()

def ReadGif(gifname):
	col_print("\n$YL[*] $WHPress $LRQ$WH to leave ")
	gifname = gifname.replace(" ", "")
	gif = imageio.mimread(gifname)
	nums = len(gif)
	imgs = [cv2.cvtColor(img, cv2.COLOR_RGB2BGR) for img in gif]
	i = 0
	while True:
	    cv2.imshow(gifname, imgs[i])
	    if cv2.waitKey(100)&0xFF == ord('q') or cv2.waitKey(100)&0xFF == 27:
	        break
	    i = (i+1)%nums
	cv2.destroyAllWindows()
