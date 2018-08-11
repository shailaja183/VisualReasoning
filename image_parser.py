# import necessary packages
from color_shape_size_classifier import ShapeDetector
from color_shape_size_classifier import ColorLabeler
import numpy as np
import imutils
import cv2
 
# dictionary for mapping full name and short names for attributes  
cfull = {"blk":"black", "yel":"yellow", "blu":"blue" }
shfull = {"tri":"triangle", "sqr":"square", "cir":"circle" }
sifull = {"sml":"small", "med":"medium", "lrg":"large" }

class ProcessedImage:
	# initialization method - do nothing
	def __init__(self):
		pass

	# basic image processing tasks - colorspace conversion, masking, resizing, thresholding and contour approximation
	def image_processing(self, imagepath, asp_rule_file, asp_fact_file):

		# read image at given path and color space conversion RGB to HSV
		img = cv2.imread(imagepath)
		img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

		# define range for black shade
		lower_black = np.array([0,0,0]) 
		upper_black = np.array([40,40,40])
		mask_black = cv2.inRange(img_hsv, lower_black, upper_black)

		# convert black shapes in original image to red
		output1_img = img.copy()
		output1_img[np.where(mask_black==255)] = [0, 0, 255]
		img_hsv2 = cv2.cvtColor(output1_img, cv2.COLOR_BGR2HSV)

		# define range for blue shade
		lower_blue = np.array([0,120,255])
		upper_blue = np.array([130,255,255])
		mask_blue = cv2.inRange(img_hsv2, lower_blue, upper_blue)

		# define range for yellow shade
		lower_yellow = np.array([20,240,240]) 
		upper_yellow = np.array([40,255,255])
		mask_yellow = cv2.inRange(img_hsv2, lower_yellow, upper_yellow)

		# define range for red shade
		lower_red = np.array([144,0,0]) 
		upper_red = np.array([255,0,0])
		mask_red = cv2.inRange(img_hsv2, lower_red, upper_red)

		# mask all portion with black that is not in range of defined blue, yellow and red shades
		mask = mask_blue + mask_yellow + mask_red
		output2_img = output1_img.copy()
		output2_img[np.where(mask==0)] = 0

		# resize image for better detection of small shapes and compute aspect ratio or original and zoomed images 
		resized = imutils.resize(output2_img, width=500) #1000
		ratio = output2_img.shape[0] / float(resized.shape[0])
		 
		# color space conversion RGB to GRAY and RGB to LAB
		gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
		lab = cv2.cvtColor(resized, cv2.COLOR_BGR2LAB)

		# apply thresholding and approximate contours of shapes
		thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)[1]
		cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		cnts = cnts[0] if imutils.is_cv2() else cnts[1]
		 
		# create objects for ShapeDetector and ColorLabeler defined in color_shape_size_classifier
		sd = ShapeDetector()
		cl = ColorLabeler()

		# some temporary variables used for clingo facts generation
		result = []
		asp = ""
		figlist = ""
		xlocdict = {}
		ylocdict = {}
		boxdict = {}		
		above = []
		left = []
		top = []

		# for each contours obtained, identify shape, size and color
		for i, c in enumerate(cnts):

			# obtain image moments to locate center coordinates of a shape
			M = cv2.moments(c)
			cX = int((M["m10"] / M["m00"]) * ratio)
			cY = int((M["m01"] / M["m00"]) * ratio)
		 
		 	# call shape and color recognizers with appropriate arguments 
		 	# show contour boundarues and display attributes (shape, size, color) over them  
			shape, halfside = sd.detect(c)
			color = cl.label(lab, c)
			c = c.astype("float")
			c *= ratio
			c = c.astype("int")
			text = "{} {}".format(color, shape)
			cv2.drawContours(output2_img, [c], -1, (0, 255, 0), 1)
			cv2.putText(output2_img, text, (cX, cY), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, (255, 255, 255), 1)

			closelytouch = []
			touch = []

			boxxbounds = [0,100,150,250,300,400]

			def touchfunc(xllim, xulim):
				if ((cX-xllim)-halfside) < 1:
					touch.append("left")
				elif ((cX-xllim)-halfside) < 4:
					closelytouch.append("left")

				if ((xulim-cX)-halfside) < 1:
					touch.append("right")
				elif ((xulim-cX)-halfside) < 4:
					closelytouch.append("right")

				if ((cY-0)-halfside) < 1:
					touch.append("top")
				elif ((cY-0)-halfside) < 4:
					closelytouch.append("top")

				if ((100-cY)-halfside) < 1:
					touch.append("bottom")
				elif ((100-cY)-halfside) < 4:
					closelytouch.append("bottom")

			# locate in which region of image (box), shape is located
			if cX <= 110:
				box = "1"
				xllim = boxxbounds[0]
				xulim = boxxbounds[1]
				touchfunc(xllim, xulim)
			elif (cX >= 140 and cX <= 260):
				box = "2"
				xllim = boxxbounds[2]
				xulim = boxxbounds[3]
				touchfunc(xllim, xulim)
			elif (cX >= 290 and cX <= 400):
				box = "3"
				xllim = boxxbounds[4]
				xulim = boxxbounds[5]
				touchfunc(xllim, xulim)
			else:
				print "box not identified correctly"
	 
			# get the labels in short form and convert them to full attribute names using dictionaries defined above	
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

			# metadata about shape - unique id, central co-ordinates, box that contains the given shape
			figName = "o" + str(i + 1)
			xlocdict[i+1] = cX
			ylocdict[i+1] = cY	
			boxdict[i+1] = box			 

			# predicates about metadata of identified shapes and write them on file
			figlist += figName+";" 
			asp += ("has(" + figName + ", size, "+ si + ").") + "\n"
			asp += ("has(" + figName + ", shape, "+ sh + ").") + "\n"
			asp += ("has(" + figName + ", color, "+ c + ").") + "\n"
			asp += ("inBox(" + figName + ", "+ box +").") + "\n"

			if closelytouch:
				for i in closelytouch:
					asp += ("touching(" + figName + ", closely, "+ i + ").") + "\n"

			if touch:
				for i in touch:
					asp += ("touching(" + figName + ", wall, "+ i + ").") + "\n"

			asp += "\n"

			with open (asp_fact_file, 'w') as fp: 
				fp.write(asp)

		appstr1 = ""
		appstr2 = ""
		appstr3 = ""

		# predicates about spatial relationships among objects and write them on file
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

		# object listing, write on files 
		figlist = "object(" + figlist + ")."
		figlist = figlist.replace(";).", ").")
		figlist = figlist + "\n\n"

		with open (asp_rule_file, 'w') as fp: 
			fp.write(figlist)

		# show annotated image, wait for user to hit enter
		#cv2.imshow("output2", output2_img)
		#cv2.waitKey()

# Reference: https://www.pyimagesearch.com/2016/02/15/determining-object-color-with-opencv/		