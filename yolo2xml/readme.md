
## convert_yolov5_to_xml.py


该文件夹用于将yolov5的格式文件夹转换为voc格式

此处的 label格式为 class xmin ymin xmax ymax 的归一化格式

与真正的yolov5的class xcenter ycenter bboxwidth bboxgeight 的格式有所区别 

具体是哪一种 只要更改 xmin ymin xmax ymax 的计算方式即可

'''
    # 更改 xmin ymin xmax ymax 的计算方式 
    xmin = ET.SubElement(bndbox, "xmin")
    ymin = ET.SubElement(bndbox, "ymin")
    xmax = ET.SubElement(bndbox, "xmax")
    ymax = ET.SubElement(bndbox, "ymax")

    
    xmin_val = int((x_center - bbox_width / 2) * image_width)
    ymin_val = int((y_center - bbox_height / 2) * image_height)
    xmax_val = int((x_center + bbox_width / 2) * image_width)
    ymax_val = int((y_center + bbox_height / 2) * image_height)
   

    xmin_val = int((x_center) * image_width)
    ymin_val = int((y_center) * image_height)
    xmax_val = int((bbox_width) * image_width)
    ymax_val = int((bbox_height) * image_height)  
'''

'''
yolov5
    |____data
            |__images
            |__labels
'''
            
## check_convert_yolov5_to_xml.py


用于检测convert_yolov5_to_xml.py文件中生成的xml是否正确  

可视化bbox

