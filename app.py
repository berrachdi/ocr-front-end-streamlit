import streamlit as st 
import os
from PIL import Image
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import json
import pandas as pd
import numpy as np

def exctract_data(items):
    if items is None:
        return ""
    else:
        return ' '.join([str(item) for item in items])

uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    with open(os.path.join("files",uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())
        
        
    

    url = "http://127.0.0.1:5000/file-upload"

    multipart_data = MultipartEncoder(
    fields={
            # a file upload field
            'file': (uploaded_file.name, open('./files/'+uploaded_file.name, 'rb'), 'application/pdf')
            
           }
    )

    response = requests.post(url, data=multipart_data,
                  headers={'Content-Type': multipart_data.content_type})
    print(response.text)

    if response.status_code == 201:
        json_data = json.loads(response.text)
        print(json_data['mobile_number'])
        df = pd.DataFrame(
             [[ 
                json_data['name'],
                exctract_data(json_data['designation']),
                json_data['email'],
                json_data['mobile_number'],
                exctract_data(json_data['skills']),
                exctract_data(json_data['degree']),
                exctract_data(json_data['experience'])
             ]],
             columns=['FullName','Designation','Email', 'Phone', 'Skills','Degree','Experience']
             )
             
        st.table(df)
    
    st.success("File saved successfully")
   

