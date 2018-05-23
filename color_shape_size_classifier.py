# import necessary packages
from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np
import cv2
 
# class ShapeDetector  
class ShapeDetector:
	# initialization method - do nothing
	def __init__(self):
		pass
 
 	# shape detection method detect()
	def detect(self, c):

		# initialize shape and size 
		shape = "unidentified"
		size = ""

		# approximate perimeter and contour
		perimeter = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.04 * perimeter, True)

		# size classification
		# shape with predefined perimeter threshold is classified as different sizes 	
		if perimeter <= 55:
			size = "sml"
		elif (perimeter >= 60 and perimeter <= 105):
			size = "med"
		elif perimeter >= 110:
			size = "lrg"
		else:
			print "perimeter not identified correctly"

		# shape classification
		# shape with 3 vertices is a triangle, 4 vertices is a square or else circle 	
		if len(approx) == 3: 
			shape = "tri"
		elif len(approx) == 4: 
			shape = "sqr"
		else: 
			shape = "cir"
		
		# return name of the shape
		return size + " " + shape
 
# class ColorLabeler   
class ColorLabeler:

	# initialization method 
	def __init__(self):

		# initialize colors dictionary as color name, RGB tuple value
		colors = OrderedDict({
			"red": (255, 0, 0),
			"yel": (255, 255, 0),
			"blu": (30, 144, 255) })
 
		# initialize the color names list
		self.lab = np.zeros((len(colors), 1, 3), dtype="uint8")
		self.colorNames = []
 
		# loop over the colors dictionary
		for (i, (name, rgb)) in enumerate(colors.items()):

			# update the Lab array and the color names list
			self.lab[i] = rgb
			self.colorNames.append(name)
 
		# convert from the RGB color space to Lab
		self.lab = cv2.cvtColor(self.lab, cv2.COLOR_RGB2LAB)

	 # color detection method label()
	def label(self, image, c):

		# construct mask for contour, and compute average Lab value 
		mask = np.zeros(image.shape[:2], dtype="uint8")
		cv2.drawContours(mask, [c], -1, 255, -1)
		mask = cv2.erode(mask, None, iterations=2)
		mean = cv2.mean(image, mask=mask)[:3]
 
		# initialize the minimum distance 
		minDist = (np.inf, None)
 
		# loop over known Lab color values
		for (i, row) in enumerate(self.lab):
			
			# compute distance for Lab colors and mean of the image
			d = dist.euclidean(row[0], mean)
 
			# if distance is smaller than current, update minDist
			if d < minDist[0]:
				minDist = (d, i)
 
		# return name of the color with smallest distance
		return self.colorNames[minDist[1]]

# Reference: https://www.pyimagesearch.com/2016/02/15/determining-object-color-with-opencv/