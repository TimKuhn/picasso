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
