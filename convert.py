from bs4 import BeautifulSoup
import re

def resolve_html_code(html):
    """
    Resolve Html code
    """    
    return BeautifulSoup(html,features="html.parser").get_text()

def RSTfile(data):
    """
    Extract data into formatted file
    """
    Raw_file="\n"
    Raw_file+="="*len(data["Module Name"]) + "\n"
    Raw_file+=data["Module Name"] + "\n"
    Raw_file+="="*len(data["Module Name"]) 
    
    for scope in data["List Artifact Info"]:
        if scope["Attribute Type"]=="Heading":
            Raw_file+="\n"*2 +scope["Title"] + '\n' + len(scope["Title"])*'*'
        elif scope["Attribute Type"]=="Information":
            Raw_file+='\n'*2 + '.. sw_req::\n'
            Raw_file+='   :id: '+str(scope["Identifier"]) +'\n'
            Raw_file+='   :artifact_type: Information' + 2*'\n'
            
            substring = scope["ReqIF.Text"].replace("<br","\n|")
            substring = substring.replace("/>","")
            regex = re.compile("xmlns=\".*\"")
            substring = re.sub(regex,'', substring)
            Raw_file+=resolve_html_code(substring)
        else:
            Raw_file+='\n'*2 + '.. sw_req::\n'
            Raw_file+='\t:status: '+str(scope["Status"]) +'\n'
            Raw_file+='\t:id: '+str(scope["Identifier"]) +'\n'            
            Raw_file+='\t:safety_level: '+str(scope["Safety Classification"]) +'\n'
            Raw_file+='\t:artifact_type: '+str(scope["Attribute Type"]) +'\n'
            Raw_file+='\t:crq: '+str(scope["CRQ"]) +'\n'
            Raw_file+= 2*'\n'+'\t'+scope["Title"] + '\n'
            if scope['Attribute Type']=='MO_FUNC_REQ':
                regex = re.compile("xmlns=\".*\"")
                substring = scope['ReqIF.Text'].replace("\u00a0","\n")
                Raw_file+='\n'+ resolve_html_code(substring)
                
            Raw_file+='\n'*2 + '   .. verify::\n\n'
            Raw_file+=         "\t\t"+re.sub('\n','\n\t\t',scope["Verification Criteria"])
    return Raw_file

def return_key(long_name):
    """
    Convert string values to keys
    """
    if long_name == 'ReqIF.ForeignModifiedBy':
        return 'Contributor'
    elif long_name == 'ReqIF.ForeignCreatedBy':
        return 'Creator'
    elif long_name == 'ReqIF.ForeignCreatedOn':
        return 'Created On'
    elif long_name == 'ReqIF.ForeignID':
        return 'Identifier'
    elif long_name == 'ReqIF.Name':
        return 'Title'
    elif long_name == "ReqIF.Description"        :return None
    elif long_name == "Artifact Format"          :return None
    elif long_name == "ReqIF.ForeignModifiedOn"  :return None
    elif long_name == "ReqIF.ChapterName"        :return None    
    
    return long_name

