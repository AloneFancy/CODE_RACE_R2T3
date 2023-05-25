from bs4 import BeautifulSoup
def output_html_code(html):
    return BeautifulSoup(html,features="lxml").get_text()

def RSTfile(data):
    Raw_file="\n"
    Raw_file+="="*len(data["Module Name"]) + "\n"
    Raw_file+=data["Module Name"] + "\n"
    Raw_file+="="*len(data["Module Name"]) + "\n"
    
    for scope in data["List Artifact Info"]:
        pass
        #Raw_file+="\n" +data["Title"] + '\n' + len(data["Title"])*'*'
        #Raw_file += str(scope["ReqIF.Name"])  +"\n"
    return Raw_file

def return_key(long_name):
    if long_name=='ReqIF.ForeignModifiedBy':
        return 'Contributor'
    elif long_name =='ReqIF.ForeignCreatedBy':
        return 'Creator'
    elif long_name =='ReqIF.ForeignCreatedOn':
        return 'Created On'
    elif long_name =='ReqIF.ForeignID':
        return 'Identifier'
    elif long_name =='ReqIF.Name':
        return 'Title'
    elif long_name =="ReqIF.Description":return None
    elif long_name=="Artifact Format":return None
    elif long_name=="ReqIF.ForeignModifiedOn":return None
    elif long_name=="ReqIF.ChapterName":return None
    return long_name

def process_value(key,value):
    if key=='Identifier':
        return int(value)
    elif key=='Title':
        return output_html_code(value)
    elif key==None:
        pass
    return value