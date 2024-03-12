import os
import xml.etree.ElementTree as ET
import cv2

'''
用于检测生成的xml是否正确
'''

def draw_bounding_boxes(xml_dir, image_dir, output_dir):
    for xml_file in os.listdir(xml_dir):
        if xml_file.endswith(".xml"):
            xml_path = os.path.join(xml_dir, xml_file)
            image_filename = os.path.splitext(xml_file)[0] + ".jpg"
            image_path = os.path.join(image_dir, image_filename)

            if os.path.exists(image_path):
                image = cv2.imread(image_path)
                height, width, _ = image.shape

                tree = ET.parse(xml_path)
                root = tree.getroot()

                for obj in root.findall(".//object"):
                    class_name = obj.find("name").text
                    xmin = int(obj.find(".//xmin").text)
                    ymin = int(obj.find(".//ymin").text)
                    xmax = int(obj.find(".//xmax").text)
                    ymax = int(obj.find(".//ymax").text)

                    cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 255, 255), 2)
                    print((xmin, ymin), (xmax, ymax))
                    cv2.putText(image, class_name, (xmin, ymin - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                output_path = os.path.join(output_dir, image_filename)
                cv2.imwrite(output_path, image)


if  __name__ == '__main__':

    xml_directory = r"H:\yolov5-Whole-sticky-board-identification\yolov5\paper_data\xml"
    image_directory = r"H:\yolov5-Whole-sticky-board-identification\yolov5\paper_data\images"
    output_directory = r"H:\yolov5-Whole-sticky-board-identification\yolov5\paper_data\xml_check"
    draw_bounding_boxes(xml_directory, image_directory, output_directory)
    print("done!")
