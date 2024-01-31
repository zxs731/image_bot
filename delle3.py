import requests
import json
import streamlit as st
import os


key = st.sidebar.text_input("Your key", type="password")
 
if not key:
    st.info("Please add your key to continue.")
    st.stop()
else:
    if "key" not in st.session_state:
        st.session_state.key = None
    st.session_state.key=key    



    

if "messages" not in st.session_state:
    st.session_state.messages = []    
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"]=="assistant":
            st.image(message["content"])
        else:
            st.markdown(message["content"])    

def getAnswer(prompt,feedback):
    url = "https://aoa1108.openai.azure.com/openai/deployments/Dalle3/images/generations?api-version=2023-12-01-preview"
    payload = json.dumps({
      "prompt": prompt,
      "n": 1,
      "size": "1792x1024"
    })
    headers = {
      'api-key': st.session_state.key,
      'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    image_url= response.json()["data"][0]["url"]
    feedback(image_url)    
    return image_url

def writeReply(cont,msg):
    #cont.write(msg)
    cont.image(msg)
    
if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("assistant"):
        p=st.empty()
        p.write("Waiting...")
        re = getAnswer(prompt,lambda x:writeReply(p,x))
        print(re)
        st.session_state.messages.append({"role": "assistant", "content": re})