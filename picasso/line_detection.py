import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

#############################################################
#                                                           #
#           Vertical & Horizontal Line Detection            #
#                                                           #
#############################################################

class Lines:
    '''
    Class that detects horizontal and vertical lines from 
    an image 

    param threshold: default 2, specifies the vertical or horizontal straightness 
    of a line. A threshold of 0 means that a line must be perfectly horizontal or vertical.
    '''
    def __init__(self, img, threshold=2):
        # Original Image and Image with lines
        self.img = img
        self.img_with_lines = img.copy()

        # Stores Horizontal and Vertical Lines as Numpy Arrays
        self.vertical_lines = []
        self.horizontal_lines = []

        # Image size
        self.y = self.img.shape[0]
        self.x = self.img.shape[1]
    
        # Parameter for HoughLines
        self.min_line_length_h = 100
        self.min_line_length_v = 100
        self.rho_h = 10
        self.rho_v = 50
        self.max_line_gap_h = 10
        self.max_line_gap_v = 10  
        self.thresh_h = 100
        self.thresh_v = 100
        self.theta_degree_h = 180
        self.theta_degree_v = 180

        # Threshold that filters non-straight lines
        self.threshold = threshold

        # Image Pre-processing Attributes
        self.horizontal = None
        self.vertical = None

    def __repr__(self):
        return f'Lines(\n\tvertical_lines={len(self.vertical_lines)},\n\thorizontal_lines={len(self.horizontal_lines)},\n\tthreshold={self.threshold})'

    def show_original(self):
        plt.imshow(self.img)

    def show_lines(self):
        plt.imshow(self.img_with_lines)

    def find_lines(self):
        self._pre_process()
        self.vertical_lines = self._detect_vertical_lines()
        self.horizontal_lines = self._detect_horizontal_lines()

    def _detect_vertical_lines(self):
        v_lines = self._vertical_line_detection()
        v_lines_truly = []
        try:
            for line in v_lines:
                for x1,y1,x2,y2 in line:
                    # Not all lines are perfectly vertical
                    # We calculate from the points if a line is truly vertical
                    if self._is_truly_straight_line(x1, x2):
                        v_lines_truly.append((x1,y1,x2,y2))
                        # Draw line on image
                        cv2.line(self.img_with_lines,(x1,y1),(x2,y2),(0,255,0),2) # green

        except TypeError as e:
            pass # no lines found
        
        finally:
            return v_lines_truly

    def _detect_horizontal_lines(self):
        h_lines = self._horizontal_line_detection()
        h_lines_truly = []
        try:
            for line in h_lines:
                for x1,y1,x2,y2 in line:
                    # Not all lines are perfectly vertical
                    # We calculate from the points if a line is truly vertical
                    if self._is_truly_straight_line(y1, y2):
                        h_lines_truly.append((x1,y1,x2,y2))
                        # Draw line on image
                        cv2.line(self.img_with_lines,(x1,y1),(x2,y2),(0,0,255),2) # blue

        except TypeError as e:
            pass # no lines found

        finally:
            return h_lines_truly

    def _pre_process(self):
        # Convert to grayscale
        img_gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

        # Gray to Binary - this works really good for line detection
        img_bin = cv2.bitwise_not(img_gray)
        img_bw = cv2.adaptiveThreshold(img_bin,\
                                        255,\
                                        cv2.ADAPTIVE_THRESH_MEAN_C,\
                                        cv2.THRESH_BINARY,\
                                        15,\
                                        -2)

        # Edge Detection
        # edges = cv2.Canny(img_bw, 100, 100, apertureSize = 3)

        # horizontal and vertical lines need different representations
        img_bw_inv = cv2.bitwise_not(img_bw)
        self.horizontal = np.copy(img_bw)
        self.vertical = np.copy(img_bw_inv)
        self._pre_process_horizontal_lines()
        self._pre_process_vertical_lines()

    def _pre_process_horizontal_lines(self):
        # Specify size on horizontal axis
        cols = self.horizontal.shape[1]
        horizontal_size = int(cols / 30)

        # Create structure element for extracting horizontal lines through morphology operations
        horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT,\
                                                        (horizontal_size, 1))

        # Apply morphology operations
        self.horizontal = cv2.erode(self.horizontal, horizontalStructure)
        self.horizontal = cv2.dilate(self.horizontal, horizontalStructure)

    def _pre_process_vertical_lines(self):
        # Specify size on vertical axis
        rows = self.vertical.shape[0]
        verticalsize = int(rows / 5)

        # Create structure element for extracting vertical lines through morphology operations
        verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT,\
                                                      (1, verticalsize))

        # Apply morphology operations
        self.vertical = cv2.erode(self.vertical, verticalStructure)
        self.vertical = cv2.dilate(self.vertical, verticalStructure)

    def _horizontal_line_detection(self):
        # Detects Lines on the pre-processed Image (Horizontally)
        return cv2.HoughLinesP(image=self.horizontal,\
                rho=self.rho_h,\
                theta=np.pi/self.theta_degree_h,\
                threshold=self.thresh_h,\
                maxLineGap=self.max_line_gap_h,\
                minLineLength=self.min_line_length_h)

    def _vertical_line_detection(self):
        # Detects Lines on the pre-processed Image (Vertically)
        return cv2.HoughLinesP(image=self.vertical,\
                rho=self.rho_v,\
                theta=np.pi/self.theta_degree_v,\
                threshold=self.thresh_v,\
                maxLineGap=self.max_line_gap_v,\
                minLineLength=self.min_line_length_v)

    def _is_truly_straight_line(self, p1, p2):
        """
        Returns true if two points are truly vertical or horizontal
        For the assessment of vertical lines please provide: x1 and x2
        For the assessment of horizontal lines please provide: y1 and y2
        """
        # if r == 0, the line is perfectly vertical/horizontal
        r = abs(p1 - p2)
            
        is_truly_straight_line = False
        if r <= self.threshold:
            is_truly_straight_line = True
                                        
        return is_truly_straight_line


