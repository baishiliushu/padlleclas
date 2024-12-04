'''
author: lxy
func:
1. 获取 路径1 下的所有xml文件列表f1
2. 路径2 和 路径1 中的xml（文件名相同的）取交集u1
3. 遍历u1，将路径2中的新类别 合并到路径1中对应的xml中
'''

#['shoes', 'bin', 'pedestal', 'wire', 'socket','cat','dog','desk_rect','desk_circle','weighing-scale', 'key', 'person','chair', 'couch', 'bed', 'tvCabinet', 'fridge', 'television', 'washingMachine', 'electricFan', 'remoteControl', 'shoeCabinet']

import glob
import os
import shutil
# from xml.etree import ElementTree
from lxml import etree as ET


def combine(files):
    xml_files = glob.glob(files +"/*.xml")
    xml_element_tree = None
    for xml_file in xml_files:
        # get root
        data = ElementTree.parse(xml_file).getroot()
        print(data)
        # print ElementTree.tostring(data)
        for result in data.iter('testsuites'):
            if xml_element_tree is None:
                xml_element_tree = data
            else:
                xml_element_tree.extend(result)
 
    if xml_element_tree is not None:
        out = open("combined.xml", "wb")
        #print >> out,ElementTree.tostring(xml_element_tree)
        #print ElementTree.tostring(xml_element_tree)
 

def change_one_xml(xml_path,all_time,all_tests,all_errors,all_disabled,all_failures): 
    doc = ElementTree.parse(xml_path)



"""
<object>
		<name>shoes</name>
		<pose>Unspecified</pose>
		<truncated>1</truncated>
		<difficult>0</difficult>
		<distance>0</distance>
		<score>0.0</score>
		<bndbox>
			<xmin>1</xmin>
			<ymin>286</ymin>
			<xmax>819</xmax>
			<ymax>1139</ymax>
		</bndbox>
</object>
"""
def got_xml_root(xml_path):
    root = None
    tree = None
    #tree = ElementTree.parse(xml_path)
    #root = tree.getroot()

    parser = ET.XMLParser(remove_blank_text=True)
    tree = ET.parse(xml_path, parser)
    root = tree.getroot()
    return root, tree

def get_annotations(xml_path, classes):
    annotations = []
    if not os.path.exists(xml_path):
        print("xml not exists: {}".format(xml_path))
        return annotations
    
    root, _ = got_xml_root(xml_path)
    
    for obj in root.findall('object'):
        obj_name = obj.find('name').text
        if obj_name in classes:
            pose = obj.find('pose').text
            truncated = int(obj.find('truncated').text)
            difficult = int(obj.find('difficult').text)
            distance = int(obj.find('distance').text)
            score = float(obj.find('score').text)

            xmin = int(obj.find('bndbox').find('xmin').text)
            ymin = int(obj.find('bndbox').find('ymin').text)
            xmax = int(obj.find('bndbox').find('xmax').text)
            ymax = int(obj.find('bndbox').find('ymax').text)
            
            annotations.append({'name': obj_name, 'pose' : pose, 'truncated' :truncated,'difficult':difficult, 'distance':distance, 'score':score, 'bndbox':{'xmin': xmin, 'ymin': ymin, 'xmax': xmax, 'ymax': ymax}})
    print("got need add nodes {} AT {}".format(len(annotations), xml_path))
    return annotations


def appedn_write_xml(xml_path, anno_objects):
    added_obj_node_counter = 0
    if not os.path.exists(xml_path):
        print("xml not exists: {}".format(xml_path))
        return added_obj_node_counter
    # 加载XML文件
    root, tree = got_xml_root(xml_path)
    
    for sub_context_pairs in anno_objects:
        new_object = ET.Element('object')
        
        for _key in sub_context_pairs:
            tmp_sub = ET.SubElement(new_object, _key)
            if _key != "bndbox":
                tmp_sub.text = '{}'.format(sub_context_pairs[_key])
            else:
                for v in sub_context_pairs[_key]:
                    box_sub = ET.SubElement(tmp_sub, v)
                    box_sub.text = '{}'.format(sub_context_pairs[_key][v])
        
        
        #new_object.set('name', obj_contexts['name'])         
        #bndbox = ElementTree.SubElement(new_object, 'bndbox')
        #xmin = ElementTree.SubElement(bndbox, 'xmin')
        #xmin.text = '100'  
        #ET.tostring
        
        # 将新的object元素追加到根元素中
        root.append(new_object)
        added_obj_node_counter = added_obj_node_counter + 1
    
    # 保存修改后的XML文件
    tree.write(xml_path, encoding='utf-8', xml_declaration=False, pretty_print=True)
    
    info_judgement = "?="
    if added_obj_node_counter == len(anno_objects):
        info_judgement = "=="
    print("{} {} {} AT {}".format(added_obj_node_counter, info_judgement, len(anno_objects), xml_path))
    return added_obj_node_counter


def get_xmls(top_path):
    files_and_dirs = os.listdir(top_path)
    xmls = [f for f in files_and_dirs if f.endswith('.xml')]
    return xmls

def found_under_all_dirs(x, y):
    xml_names_todo = []
    set1 = set(x)
    set2 = set(y)
    intersection = set1 & set2
    xml_names_todo = list(intersection)
    return xml_names_todo


if __name__ == '__main__':
    
    NEW_CLASSES = ['remoteControl', 'electricFan']

    NEW_CLASSES_XML_PATH = "/home/leon/mount_point_c/yolo_datas_waicai/xml/test/new_one"
    WAIT_UPDATE_XML_PATH = "/home/leon/mount_point_c/yolo_datas_waicai/xml/test/wait_add"
    
    if not os.path.exists(NEW_CLASSES_XML_PATH):
        print("new classed path not exists: {}".format(NEW_CLASSES_XML_PATH))
        exit(-1)
    if not os.path.exists(WAIT_UPDATE_XML_PATH):
        print("wait add path not exists: {}".format(WAIT_UPDATE_XML_PATH))
        exit(-1)
    xmls_under_new = get_xmls(NEW_CLASSES_XML_PATH)
    xmls_under_wait = get_xmls(WAIT_UPDATE_XML_PATH)
    
    xmls_todo = found_under_all_dirs(xmls_under_new, xmls_under_wait)
    
    for x in xmls_todo:
        current_xml_annos = get_annotations(os.path.join(NEW_CLASSES_XML_PATH, x), NEW_CLASSES)
        if len(current_xml_annos) > 0:
            appedn_write_xml(os.path.join(WAIT_UPDATE_XML_PATH, x), current_xml_annos)
            
    print("Finished:{}({} done {})".format(WAIT_UPDATE_XML_PATH, len(xmls_under_wait), len(xmls_todo)))
    
