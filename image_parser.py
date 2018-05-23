# importing necessary packages
from color_shape_size_classifier import ShapeDetector
from color_shape_size_classifier import ColorLabeler
import imutils
import cv2
import numpy as np
import os
 
cfull = {"red":"red", "yel":"yellow", "blu":"blue" }
shfull = {"tri":"triangle", "sqr":"square", "cir":"circle" }
sifull = {"sml":"small", "med":"medium", "lrg":"large" }

class ProcessedImage:
	# initialization method - do nothing
	def __init__(self):
		pass

	def image_processing(self, imagepath, asp_rule_file, asp_fact_file):
		img = cv2.imread(imagepath)
		img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

		lower_black = np.array([0,0,0]) 
		upper_black = np.array([40,40,40])
		mask_black = cv2.inRange(img_hsv, lower_black, upper_black)

		output1_img = img.copy()
		output1_img[np.where(mask_black==255)] = [0, 0, 255]
		img_hsv2 = cv2.cvtColor(output1_img, cv2.COLOR_BGR2HSV)

		lower_blue = np.array([0,120,255])
		upper_blue = np.array([130,255,255])
		mask_blue = cv2.inRange(img_hsv2, lower_blue, upper_blue)

		lower_yellow = np.array([20,240,240]) 
		upper_yellow = np.array([40,255,255])
		mask_yellow = cv2.inRange(img_hsv2, lower_yellow, upper_yellow)

		lower_red = np.array([144,0,0]) 
		upper_red = np.array([255,0,0])
		mask_red = cv2.inRange(img_hsv2, lower_red, upper_red)

		mask = mask_blue + mask_yellow + mask_red

		output2_img = output1_img.copy()
		output2_img[np.where(mask==0)] = 0

		resized = imutils.resize(output2_img, width=500) #1000
		ratio = output2_img.shape[0] / float(resized.shape[0])
		 
		gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
		lab = cv2.cvtColor(resized, cv2.COLOR_BGR2LAB)
		thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)[1]

		cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		cnts = cnts[0] if imutils.is_cv2() else cnts[1]
		 
		sd = ShapeDetector()
		cl = ColorLabeler()

		result = []
		asp = ""
		figlist = ""
			
		xlocdict = {}
		ylocdict = {}
		boxdict = {}		
		above = []
		left = []
		top = []

		for i, c in enumerate(cnts):
			M = cv2.moments(c)
			cX = int((M["m10"] / M["m00"]) * ratio)
			cY = int((M["m01"] / M["m00"]) * ratio)
		 
			shape = sd.detect(c)
			color = cl.label(lab, c)
		 
			c = c.astype("float")
			c *= ratio
			c = c.astype("int")
			text = "{} {}".format(color, shape)
			cv2.drawContours(output2_img, [c], -1, (0, 255, 0), 1)
			cv2.putText(output2_img, text, (cX, cY), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, (255, 255, 255), 1)

			if cX <= 110:
				box = "1"
			elif (cX >= 140 and cX <= 260):
				box = "2"
			elif (cX >= 290 and cX <= 400):
				box = "3"
			else:
				print "box not identified correctly"

			c, si, sh = text.split()
			
			for key in cfull:
				if c==key:
					c = c.replace(c, cfull[key])
			for key in sifull:
				if si==key:
					si = si.replace(si, sifull[key])
			for key in shfull:
				if sh==key:
					sh = sh.replace(sh, shfull[key])
   
			result.append((i, c, si, sh))

			figName = "o" + str(i + 1)
			#print figName
			xlocdict[i+1] = cX
			ylocdict[i+1] = cY	
			boxdict[i+1] = box			 

			figlist += figName+";" 
			asp += ("has(" + figName + ", size, "+ si + ").") + "\n"
			asp += ("has(" + figName + ", shape, "+ sh + ").") + "\n"
			asp += ("has(" + figName + ", color, "+ c + ").") + "\n"
			asp += ("inBox(" + figName + ", "+ box +").") + "\n"
			asp += ("\n")

			with open (asp_fact_file, 'w') as fp: 
				fp.write(asp)

		appstr1 = ""
		appstr2 = ""
		appstr3 = ""

		for i in boxdict:
			for j in boxdict:
				if i<j and boxdict[i]==boxdict[j]:

					if xlocdict[i]<xlocdict[j]:
						appstr1 = "leftTo(o" + str(i) + ", o" + str(j) +")." + "\n"
					elif xlocdict[i]>xlocdict[j]:
						appstr1 = "leftTo(o" + str(j) + ", o" + str(i) +")."	+ "\n"
					if appstr1:
						left.append(appstr1) 

					if ylocdict[i]<ylocdict[j]:
						appstr2 = "aboveThan(o" + str(i) + ", o" + str(j) +")." + "\n"
					elif ylocdict[i]>ylocdict[j]:
						appstr2 = "aboveThan(o" + str(j) + ", o" + str(i) +")." + "\n"
					if appstr2:
						above.append(appstr2)	

					if xlocdict[i]==xlocdict[j] and (ylocdict[i]-ylocdict[j]>=15 and ylocdict[i]-ylocdict[j]<=27):
						appstr3 = "onTop(o" + str(j) + ", o" + str(i) +")." + "\n"
						top.append(appstr3)
					elif xlocdict[i]==xlocdict[j] and (ylocdict[j]-ylocdict[i]>=15 and ylocdict[j]-ylocdict[i]<=27):
						appstr3 = "onTop(o" + str(i) + ", o" + str(j) +")." + "\n"			
						top.append(appstr3)

		with open (asp_fact_file, 'a') as fp:
			for i in above:
				fp.write(i)
			for i in left:
				fp.write(i)
			for i in top:
				fp.write(i)

		figlist = "object(" + figlist + ")."
		figlist = figlist.replace(";).", ").")
		figlist = figlist + "\n\n"

		with open (asp_rule_file, 'w') as fp: 
			fp.write(figlist)

		cv2.imshow("output2", output2_img)
		cv2.waitKey()

		