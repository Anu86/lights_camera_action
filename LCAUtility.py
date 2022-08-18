# Import required libraries and dependencies
import pandas as pd
import streamlit as st
from pathlib import Path
import numpy as np
from PIL import Image
import base64

############Streamlit Code #########################

##Function to set up background image 
@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file) 
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: scroll; # doesn't work
    }
    </style>
    ''' % bin_str
    
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

## SEt up Background Image 
set_png_as_page_bg('image_2.png')

##Function to display PDF
def show_pdf(file_path):
    with open(file_path,"rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


# Load the data into a Pandas DataFrame
df_movie_data = pd.read_csv(
    Path("Movie-Projects.csv"), index_col = 'Name')

## Set up the title in black
st.markdown(f'<h1 style="color:#f7d0cb;font-size:40px;">{"Lights Camera Action"}</h1>', unsafe_allow_html=True)
## Set up the subtitle in black
st.markdown(f'<h2 style="color:#f7d0cb;font-size:24px;">{"Democratizing funding movies"}</h2>', unsafe_allow_html=True)

## Set up image for movie 1
image_1 = Image.open('film_projects/bgro/bgro.png')
st.image(image_1, width=400)

st.markdown(f'<p style="color:#c5b9cd;font-size:20px;">{"Bach Gaye Re Obama (BGRO) is a sequel to the hit film Phas Gaye Re Obama (PGRO). BGRO is a fast paced, fun-filled , hilarious gangster based satirical comedy, larger in scale and scope than its prequel. The story deals with the problems faced by a maid who is ‘used’ by the powerful diplomats abroad and how her challenging their might shakes the corridors of power both in India and the US."}</p>', unsafe_allow_html=True)

## Table with artist details for Movie-1
st.table(df_movie_data.iloc[0])
                  
## More details - Display PDF                  
if st.button('Get Details on Movie-1 >>'):
    show_pdf('film_projects/bgro/synopsis.pdf')

## Contribute as USD or ETH
def collectinfo():
    with st.form ("Collecting User Information", clear_on_submit= True):
        full_name= st.text_input("Full Name")
        wallet_address= st.text_input("Ethereum wallet address")
        cash_amount= st.text_input("USD")
        submit = st.form_submit_button("submit")
    
if st.button('Contribute to Movie1'):
    collectinfo()
    
## Set up image for Movie 2
image_2 = Image.open('film_projects/pgro/pgro.png')
st.image(image_2, width=400)

st.markdown(f'<p style="color:#c5b9cd;font-size:20px;">{"The movie is a comedy with satire on recession. The story revolves around a Non-resident- Indian (NRI), Om Shashtri, who lived the American dream and made it big in the US. Then one day, as it happened in America, US economy went into recession and overnight big businesses, banks, and financial institutions crashed."}</p>', unsafe_allow_html=True)

## Table with artist details for Movie-2
st.table(df_movie_data.iloc[1])

if st.button('Get Details on Movie-2 >>'):
   show_pdf('film_projects/pgro/synopsis.pdf')

## Contribute as USD or ETH
if st.button('Contribute to Movie-2'):
        collectinfo()
        
## Set up image for movie 3
image_3 = Image.open('film_projects/sjsm/sjsm.png')
st.image(image_3, width=400)

st.markdown(f'<p style="color:#c5b9cd;font-size:20px;">{"The story is a hilarious and satirical take on Mehngai( (inflation) through a middle class family from a small North Indian City. The family, crushed under the burden of Mehngai. tries to deal with it through an ingenious idea, not realizing the problems they would get tangled into as a result of this idea. It is a hillarious journey of this family battling these issues culminating into a climax that brings tears into your eyes."}</p>', unsafe_allow_html=True)

## Table with artist details for Movie-3
st.table(df_movie_data.iloc[2])

if st.button('Get Details on Movie-3 >>'):
 show_pdf('film_projects/sjsm/synopsis.pdf')

## Contribute as USD or ETH
if st.button('Contribute to Movie-3'):
    collectinfo()

    
  

        
