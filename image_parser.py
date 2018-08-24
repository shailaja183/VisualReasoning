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
	def image_processing(self, imagepath, asp_rule_file, asp_fact_file, flag):

		image = cv2.imread(imagepath)
		#cv2.imshow("Image", image)
		#cv2.waitKey(0)

		image[np.where((image == [128,128,128]).all(axis = 2))] = [211,211,211]
		image[np.where((image != [211,211,211]).all(axis = 2))] = [255,255,255]
		image[np.where((image != [255,255,255]).all(axis = 2))] = [0,0,0]

		resized = imutils.resize(image, width=1000)
		ratio = image.shape[0] / float(resized.shape[0])
		gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
		lab = cv2.cvtColor(resized, cv2.COLOR_BGR2LAB)

		if flag==True:
			blurred = cv2.GaussianBlur(gray, (5, 5), 0)
			thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
			cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		elif flag==False:
			thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)[1]
			cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

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

		#for c in cnts:
		for i, c in enumerate(cnts):
			M = cv2.moments(c)
			cX = int((M["m10"] / M["m00"]) * ratio)
			cY = int((M["m01"] / M["m00"]) * ratio)
			shape, halfside = sd.detect(c)
			if shape=="rect":
				preprocess(imagepath,False)
				break
			color = cl.label(lab, c)
			c = c.astype("float")
			c *= ratio
			c = c.astype("int")
			text = "{} {}".format(color, shape)
			cv2.drawContours(image, [c], -1, (0, 255, 0), 1)
			cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

			cv2.imshow("Image", image)
			cv2.waitKey(0)

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
