#############################################################
#                                                           #
#           Vertical & Horizontal Line Detection            #
#                                                           #
#############################################################

class Lines:
    '''
    Class that detects horizontal and vertical lines from 
    an image 
    '''
    def __init__(self, img):
        self.img = img
        self.horizontal = None
        self.vertical = None

    def pre_process(self):
        # Convert to grayscale
        img_gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

        # Gray to Binary - this works really good for line detection
        img_bin = cv2.bitwise_not(img_gray)
        img_bw = cv2.adaptiveThreshold(img_bin, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, -2)

        # Edge Detection
        edges = cv2.Canny(img_bw, 100, 100, apertureSize = 3)

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
        horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontal_size, 1))

        # Apply morphology operations
        self.horizontal = cv2.erode(self.horizontal, horizontalStructure)
        self.horizontal = cv2.dilate(self.horizontal, horizontalStructure)

    def _pre_process_vertical_lines(self):
        # Specify size on vertical axis
        rows = self.vertical.shape[0]
        verticalsize = int(rows / 5)

        # Create structure element for extracting vertical lines through morphology operations
        verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, verticalsize))

        # Apply morphology operations
        self.vertical = cv2.erode(self.vertical, verticalStructure)
        self.vertical = cv2.dilate(self.vertical, verticalStructure)



#############################################################
#                                                           #
#           Table Classifier Functions                      #
#                                                           #
#############################################################


def table_classifier(block) -> float:
    '''
    Returns probability of a block being a table
    '''

    # Image Features:
    # - Vertical Lines
    # - Horizontal Lines
    # - Number of small Rectangles
    # Text Features:
    # - Number to Char Ratio
    # - Newlines 
    # - Whitespace (more than one)
    # Layout Features:
    # - Where is it in the document

def text_classifier(block) -> float:
    '''
    Returns probability of a block being normal text 
    '''
    
    # Image Features:
    # - Vertical Lines
    # - Horizontal Lines
    # - Number of small Rectangles
    # Text Features:
    # - Number to Char Ratio
    # - Newlines
    # - Whitespace (more than one)
    # - Number of "real" sentences
    # Layout Features:
    # - Where is it in the document



def page_classifier(block) -> float:
    '''
    Returns probability of a block being the page number
    '''

    # Image Features:
    # 
    # Text Features:
    # - Contains only Numbers
    # - Length of text
    # Layout Features:
    # - in 10% top or 10% bottom
