'''

Takes a Page Object and Transforms it into 
a YOLO v2 ready format. Script generates XML Files and
stores the images to folder

'''

import os
import cv2
from lxml import etree
import xml.etree.cElementTree as ET


def write_xml(page, filename, folder, savedir='annotations'):
    '''
    param folder: image location
    param img: image object (cv2)
    param objects: Block Objects in a page

    '''
    if not os.path.isdir(savedir):
        os.mkdir(savedir)

    if not os.path.isdir(folder):
        os.mkdir(folder)

    height, width, depth = page.img.shape

    annotation = ET.Element('annotation')
    ET.SubElement(annotation, 'folder').text = folder
    ET.SubElement(annotation, 'filename').text = filename
    ET.SubElement(annotation, 'segmented').text = '0'
    size = ET.SubElement(annotation, 'size')
    ET.SubElement(size, 'width').text = str(width)
    ET.SubElement(size, 'height').text = str(height)
    ET.SubElement(size, 'depth').text = str(depth)
    
    for obj in page.blocks:
        xmin = obj.x
        ymin = obj.y
        xmax = obj.x + obj.w
        ymax = obj.y + obj.h

        ob = ET.SubElement(annotation, 'object')
        ET.SubElement(ob, 'name').text = 'box' # name of the detected object
        ET.SubElement(ob, 'pose').text = 'Unspecified'
        ET.SubElement(ob, 'truncated').text = '0'
        ET.SubElement(ob, 'difficult').text = '0'
        
        bbox = ET.SubElement(ob, 'bndbox')
        ET.SubElement(bbox, 'xmin').text = str(xmin) 
        ET.SubElement(bbox, 'ymin').text = str(ymin)
        ET.SubElement(bbox, 'xmax').text = str(xmax)
        ET.SubElement(bbox, 'ymax').text = str(ymax)
    
    xml_str = ET.tostring(annotation)
    root = etree.fromstring(xml_str)
    xml_str = etree.tostring(root, pretty_print=True)
    save_path = os.path.join(savedir, filename.replace('png', 'xml'))
    with open(save_path, 'wb') as temp_xml:
        temp_xml.write(xml_str)

