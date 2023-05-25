from reqif.parser import ReqIFParser
from convert import *

import xml.etree.ElementTree as ET
input_file_path = "Requirements.reqif"
reqif_bundle = ReqIFParser.parse(input_file_path)
spec_types = [i for i in reqif_bundle.core_content.req_if_content.spec_types]

#print(tree)
data= {}
data["Module Name"] = reqif_bundle.core_content.req_if_content.specifications[0].long_name
data["Module Type"] = reqif_bundle.core_content.req_if_content.spec_types[1].long_name
ListArtifactInfo = []
#print(data["Module Name"])

data["List Artifact Info"] = ListArtifactInfo
print(data)
print(len(reqif_bundle.core_content.req_if_content.spec_objects))

def return_object(objects):
    list =[]    
    
    for i in reqif_bundle.core_content.req_if_content.spec_objects:
        print('\n')
        obj={}
        b = reqif_bundle.get_spec_object_by_ref(i.identifier)
        obj["Attribute Type"]=reqif_bundle.get_spec_object_type_by_ref(b.spec_object_type).long_name#heading(i.spec_object_type)
        obj["Modified On"]=i.last_change
        obj["Description"]=i.description
        
        for key in i.attribute_map:
            temp = i.attribute_map.get(key)
            c = b.attribute_map.get(temp.definition_ref).definition_ref
            for attribute in spec_types:
                print(attribute.attribute_map)        
            
            #print(str(reqif_bundle.core_content.req_if_(temp.definition_ref)))
            #print(temp.value)
        
        list.append(obj)
    return list




data["List Artifact Info"]=return_object(reqif_bundle.core_content.req_if_content.spec_objects)
#print(reqif_bundle.core_content.req_if_content.spec_objects[2].attribute_map)

#print(data)


