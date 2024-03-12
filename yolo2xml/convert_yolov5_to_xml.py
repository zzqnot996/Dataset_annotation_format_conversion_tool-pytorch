import xml.etree.ElementTree as ET
import os
import cv2

'''
该文件夹用于将yolov5的格式文件夹转换为voc格式
此处的 label格式为 class xmin ymin xmax ymax 的归一化格式 
与真正的yolov5的class xcenter ycenter bboxwidth bboxgeight 的格式有所区别 只要更改 xmin ymin xmax ymax 的计算方式即可

yolov5
    |____data
            |__images
            |__labels

'''

def convert_yolov5_to_xml(yolov5_txt_file, xml_output_dir, image_width, image_height):
    with open(yolov5_txt_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        if line:
            elements = line.split()
            class_id = elements[0]
            x_center, y_center, bbox_width, bbox_height = map(float, elements[1:])
            
            # Assuming you have image filename without extension
            image_filename = os.path.basename(yolov5_txt_file).split(".")[0]
            print("image_filename" ,image_filename )
            create_xml_file(xml_output_dir, image_filename, class_id, x_center, y_center, bbox_width, bbox_height, image_width, image_height)


def create_xml_file(xml_output_dir, image_filename, class_id, x_center, y_center, bbox_width, bbox_height, image_width, image_height):
    root = ET.Element("annotation")

    folder = ET.SubElement(root, "folder")
    folder.text = "images"

    filename = ET.SubElement(root, "filename")
    filename.text = f"{image_filename}.jpg"

    size = ET.SubElement(root, "size")
    width = ET.SubElement(size, "width")
    height = ET.SubElement(size, "height")
    depth = ET.SubElement(size, "depth")

    width.text = str(image_width)
    height.text = str(image_height)
    depth.text = "3"  # Assuming RGB images

    object_elem = ET.SubElement(root, "object")
    name = ET.SubElement(object_elem, "name")
    pose = ET.SubElement(object_elem, "pose")
    truncated = ET.SubElement(object_elem, "truncated")
    difficult = ET.SubElement(object_elem, "difficult")
    bndbox = ET.SubElement(object_elem, "bndbox")

    name.text = str(class_id)
    pose.text = "Unspecified"
    truncated.text = "0"
    difficult.text = "0"

    #----------------------------------------------------------------------------------------------
    # 更改 xmin ymin xmax ymax 的计算方式 
    xmin = ET.SubElement(bndbox, "xmin")
    ymin = ET.SubElement(bndbox, "ymin")
    xmax = ET.SubElement(bndbox, "xmax")
    ymax = ET.SubElement(bndbox, "ymax")

    '''     
    xmin_val = int((x_center - bbox_width / 2) * image_width)
    ymin_val = int((y_center - bbox_height / 2) * image_height)
    xmax_val = int((x_center + bbox_width / 2) * image_width)
    ymax_val = int((y_center + bbox_height / 2) * image_height)
    '''
    #----------------------------------------------------------------------------------------------
    xmin_val = int((x_center) * image_width)
    ymin_val = int((y_center) * image_height)
    xmax_val = int((bbox_width) * image_width)
    ymax_val = int((bbox_height) * image_height)  
   

    print(xmin_val, ymin_val,xmax_val,ymax_val)

    xmin.text = str(max(0, xmin_val))
    ymin.text = str(max(0, ymin_val))
    xmax.text = str(min(image_width, xmax_val))
    ymax.text = str(min(image_height, ymax_val))

    tree = ET.ElementTree(root)
    xml_filename = os.path.join(xml_output_dir, f"{image_filename}.xml")
    tree.write(xml_filename, encoding="utf-8")


def main(path,xml_output_directory,yolov5_images_path):

    '''
    path   ---> yolov5格式 label文件夹内存有txt文件  此处为label文件夹的路径
    xml_output_directory  --> 需要保存到xml文件夹的路径
    yolov5_images_path  ----> yolov5格式 image文件夹内存有与txt文件同名的图片文件  此处为image文件夹的路径
    '''

    for label_filename in os.listdir(path):
        print(label_filename)
        yolov5_txt_path = os.path.join(path,label_filename) 

        # Get the corresponding image filename
        img_filename = label_filename.split(".")[0] + ".jpg"
        image_filepath = os.path.join(yolov5_images_path, img_filename) 
        
        # Read the image to obtain its width and height
        image = cv2.imread(image_filepath)
        image_height,image_width , _ = image.shape
        print(image_height, image_width, _ )

        # Now you have the image width and height, and you can use them in your XML generation code
        convert_yolov5_to_xml(yolov5_txt_path, xml_output_directory, image_width, image_height)    


if __name__ == '__main__':

    # yolov5格式 label文件夹内存有txt文件  此处为label文件夹的路径
    path = r"H:\yolov5-Whole-sticky-board-identification\yolov5\paper_data\labels"
    # 需要保存到xml文件夹的路径
    xml_output_directory = r"H:\yolov5-Whole-sticky-board-identification\yolov5\paper_data\xml"
    # yolov5格式 image文件夹内存有与txt文件同名的图片文件  此处为image文件夹的路径
    yolov5_images_path =  r"H:\yolov5-Whole-sticky-board-identification\yolov5\paper_data\images"


    main(path,xml_output_directory,yolov5_images_path)





