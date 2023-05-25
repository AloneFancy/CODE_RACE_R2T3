from reqif.parser import ReqIFParser
from convert import *
import json

def spec_dictionary():
    global def_dictionary
    def_dictionary = {}
    for i in spec_types:
        try:
            for j in i.attribute_map:                
                def_dictionary[i.attribute_map.get(j).identifier]= i.attribute_map.get(j).long_name
        except:
            pass

def return_list():
    list=[]
    global def_dictionary
    for i in spec_objects:
        obj={}
        b = reqif_bundle.get_spec_object_by_ref(i.identifier)
        obj["Attribute Type"]=reqif_bundle.get_spec_object_type_by_ref(b.spec_object_type).long_name#heading(i.spec_object_type)
        obj["Modified On"]=i.last_change
        obj["Description"]=i.description if i.description else ""
        #print("\n")        
        for key in i.attribute_map:
            def_ref = i.attribute_map.get(key).definition_ref
            obj[return_key(def_dictionary[def_ref])]=process_value(return_key(def_dictionary[def_ref]),i.attribute_map.get(key).value)

        list.append(obj)
    return list

if __name__ == "__main__":

    input_file_path = "Requirements.reqif"
    reqif_bundle = ReqIFParser.parse(input_file_path)

    spec_objects = reqif_bundle.core_content.req_if_content.spec_objects
    spec_types = reqif_bundle.core_content.req_if_content.spec_types
    spec_dictionary()

    data= {}
    data["Module Name"] = reqif_bundle.core_content.req_if_content.specifications[0].long_name
    data["Module Type"] = reqif_bundle.core_content.req_if_content.spec_types[1].long_name
    
    ListArtifactInfo = return_list() 
    data["List Artifact Info"] = ListArtifactInfo
    with open('data.json', 'w') as f:
        json.dump(data, f)
    print(RSTfile(data))