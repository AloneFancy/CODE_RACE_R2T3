from bs4 import BeautifulSoup
def output_html_code(html):
    return BeautifulSoup(html).get_text()

def RSTfile(data):
    Raw_file="\n"
    Raw_file+="="*len(data["Module Name"]) + "\n"
    Raw_file+=data["Module Name"] + "\n"
    Raw_file+="="*len(data["Module Name"]) + "\n"
    for scope in data["List Artifact Info"]:
        Raw_file +=  output_html_code(scope["ReqIF.Text"])  +"\n"
    return Raw_file

def return_key(long_name):
    if long_name=='ReqIF.ForeignModifiedBy':
        return 'Contributor'
    elif long_name =='ReqIF.ForeignCreatedBy':
        return 'Creator'
    elif long_name =='ReqIF.ForeignID':
        return 'Identifier'
    elif long_name =='ReqIF.ChapterName':
        return 'Title'
    return long_name

def process_value(key,value):
    if key=='Identifier':
        return int(value)
    elif key=='ReqIF.ChapterName':
        return output_html_code(value)
    return value