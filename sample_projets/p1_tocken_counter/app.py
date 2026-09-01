import streamlit as st


# heading 
st.header("Tokenizer")

# input 

input_text = st.text_area("" ,max_chars=500, placeholder="Enter some text")

# output
st.write(input_text)
from main2 import create_token

output = create_token(input_text)

col1, col2 = st.columns(2)

col1.write("Tokens")
col1.write(len(output))

col2.write("Characters")
col2.write(len(input_text))


cont = st.container(border=True, width=800, height=200)
cont.write(", ".join(output)) # type: ignore  


