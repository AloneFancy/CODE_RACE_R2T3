from reqif.parser import ReqIFParser
from convert import *
import json

def spec_dictionary():
    '''
    Init def 
    '''
    global def_dictionary
    def_dictionary = {}
    for type in spec_types:
        try:
            for j in type.attribute_map:                
                def_dictionary[type.attribute_map.get(j).identifier]= type.attribute_map.get(j).long_name
        except:
            pass

def enum_dictionary():
    '''
    Init enum dictionary for data types
    '''
    global enum_dictionary
    enum_dictionary={}
    for data_def in reqif_bundle.core_content.req_if_content.data_types:
        if(data_def.long_name=='T_Status'or data_def.long_name=='T_Safety Classification'):            
            for enum in data_def.values:
                enum_dictionary[enum.identifier] = enum.long_name

def extractKeysValues():
    """
    list{'identifier':{obj{}}}
    Output final : [list['identifier']]
    """
    list={}
    global def_dictionary   
    for iterate in spec_objects:
        obj={}
        b = reqif_bundle.get_spec_object_by_ref(iterate.identifier)
        obj["Attribute Type"]=reqif_bundle.get_spec_object_type_by_ref(b.spec_object_type).long_name
        obj["Modified On"]=iterate.last_change
        obj["Description"]=iterate.description if iterate.description else ""
        obj["ReqIF.Text"]=""
        for key in iterate.attribute_map:
            def_ref = iterate.attribute_map.get(key).definition_ref
            obj[return_key(def_dictionary[def_ref])]=process_value(return_key(def_dictionary[def_ref]),iterate.attribute_map.get(key).value)

        obj.pop(None)
        list[iterate.identifier]=obj
    final = []
    for specification in reqif_bundle.core_content.req_if_content.specifications:
        for current_hierarchy in reqif_bundle.iterate_specification_hierarchy(specification):            
            final.append(list[current_hierarchy.spec_object])
    return final

def process_value(key,value):
    """
    Resolve value for each key
    """
    global enum_dictionary
    if key=='Identifier':
        return int(value)
    elif key=='Title':
        return resolve_html_code(value)
    elif key=='Safety Classification':
        return enum_dictionary[value[0]]                      
    elif key=='Status':
        return enum_dictionary[value[0]]
    elif key==None:
        pass
    return value

def init():
    """
    Init spec object data types and values dictionaries
    """
    global spec_types, spec_objects
    spec_objects = reqif_bundle.core_content.req_if_content.spec_objects
    spec_types = reqif_bundle.core_content.req_if_content.spec_types
    spec_dictionary()
    enum_dictionary()

if __name__ == "__main__":
    input_file_path = "Requirements.reqif"
    reqif_bundle = ReqIFParser.parse(input_file_path)
    init()    
    data= {}
    data["Module Name"] = reqif_bundle.core_content.req_if_content.specifications[0].long_name
    data["Module Type"] = reqif_bundle.core_content.req_if_content.spec_types[1].long_name
    
    ListArtifactInfo = extractKeysValues() 
    data["List Artifact Info"] = ListArtifactInfo
    try:
        with open('data.json', 'w') as f:
            json.dump(data, f)
        f.close()
    except:
        Exception("Wrong path")
    try:
        with open('ECU_Req.rst','w')as f:
            f.flush()
            f.write(RSTfile(data))
        f.close()
    except: 
        Exception("Wrong path")#adad
    
    

