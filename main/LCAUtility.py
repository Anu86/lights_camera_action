# Import required libraries and dependencies
import pandas as pd
import streamlit as st
from pathlib import Path
import numpy as np
from PIL import Image
import base64
from web3 import Web3
from dotenv import load_dotenv
from pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json
import os
import json
import token
import csv

############Streamlit Code ##################################################


load_dotenv('my.env')

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

# Contract Helper function:
# 1. Loads the contract once using cache
# 2. Connects to the contract using the contract address and ABI
################################################################################



@st.cache(allow_output_mutation=True)
def load_contract():

    # Load the contract ABI
    with open(Path('./contracts/compiled/tokens_abi.json')) as f:
        contract_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )

    return contract

##Function to set up background image 

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

## Set up Background Image 
set_png_as_page_bg('films_4.png')

# Load the contract
contract = load_contract()

## Set up the title 
st.markdown(f'<h1 style="color:#FF5733;font-size:40px;">{"Lights Camera Action"}</h1>', unsafe_allow_html=True)
    ## Set up the subtitle 
st.markdown(f'<h2 style="color:#F78066;font-size:24px;">{"Movie funding made easy!"}</h2>', unsafe_allow_html=True)

#######################################################################################

#create a tab for registering NFT for each film that is available

tabs = st.tabs(["Register NFT","Make Investment"])

with tabs[0]:
    st.markdown(f'<h2 style="color:#F78066;font-size:24px;">{"NFT Registration"}</h2>', unsafe_allow_html=True)
    ################################################################################
    # Helper functions to pin files and json to Pinata
    ################################################################################


    def pin_artwork(owner,film,filmItem,price,issueQty,availableNow,commission, artwork_file):
        # Pin the file to IPFS with Pinata
        ipfs_file_hash = pin_file_to_ipfs(artwork_file.getvalue())
        

        # Build a token metadata file for the artwork
        token_json = {
            "owner": owner,    #address of who owns it, initially the film company
            "film": film,       #film name
            "filmItem": filmItem, #item of the film that is NFTd
            "price" : price,    #price for this one
            "issueQuantity": issueQty, #how many of this nft issued at the beginning
            "amtAvailableNow": availableNow, # howmany available now
            "commission": commission,  #seller fee or commission
            "image": ipfs_file_hash
            }
        json_data = convert_data_to_json(token_json)

        # Pin the json to IPFS with Pinata
        json_ipfs_hash = pin_json_to_ipfs(json_data)

        return json_ipfs_hash, ipfs_file_hash
    
    # In production version, the user would have logged in and his/her associated account will be used
    # Here we are asking for a User Account from Ganache to work with
    st.write("Choose an account to get started")
    accounts = w3.eth.accounts
    owner = st.selectbox("Select Account", options=accounts)
    st.markdown("---")
    ################################################################################
    # Register NFT Item
    ################################################################################
    st.markdown(f'<h2 style="color:#F78066;font-size:24px;">{"Register NFT Item"}</h2>', unsafe_allow_html=True)
    film = st.text_input("Enter the name of the Movie/ Web-Series")
    film_item = st.text_input("Enter the name for the Item from this Movie/Series")
    initial_price = st.text_input("Enter the Initial Price")
    issueQty = st.text_input("How many NFT Tokens for this item")  #amt is uint256
    commission = st.number_input("Commission in percent- Enter 5 for 5 percent ")
    
    artwork_file = st.file_uploader("Upload Artwork", type=["jpg", "jpeg", "png"])
    
    data = 0x0000  #data is bytes data, if any
    
    availableNow = issueQty

    if st.button("Register with IPFS"):
    # Use the `pin_artwork` helper function to pin the file to IPFS

        artwork_ipfs_hash, file_hash =  pin_artwork(owner,
                                                    film,filmItem,
                                                    initial_price,
                                                    issueQty,availableNow,
                                                    commission, artwork_file) 
        

        artwork_uri = f"ipfs://{artwork_ipfs_hash}"

        tx_hash = contract.functions.registerToken(
            owner,
            film,
            filmItem,
            int(initial_price),
            int(issueQty),
            int(availableNow),
            int(commission*100),  # commission multiplied by hundred bec of Solidity 
            artwork_uri,
            file_hash,
            bytes(0x0000)
            ).transact({'from': owner, 'gas': 1000000})
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    #st.write("Transaction receipt mined:")
    # st.write(dict(receipt))
    # st.write("You can view the pinned metadata file with the following IPFS Gateway Link")
    #st.markdown(f"[Artwork IPFS Gateway Link](https://ipfs.io/ipfs/{artwork_ipfs_hash})")
        st.markdown(f"[Click to see the NFT just added](https://gateway.pinata.cloud/ipfs/{file_hash})")
        st.write(file_hash)
        st.markdown("---")
        
    st.markdown(f'<h2 style="color:#F78066;font-size:24px;">{"Campaign Setup for Film Funding"}</h2>',unsafe_allow_html=True)
    fundsTarget = st.number_input("Target Amount to Raise")
    timeLimit =  st.number_input("How long for the Campaign, enter in SECONDS..(sorry!)")
    st.button("Set Targets")


    contract.functions.setCampaignTarget(int(fundsTarget), int(timeLimit)).transact({'from': owner, 'gas': 1000000})


    # RETRIEVE THE TARGETS
    fundsToRaise = contract.functions.fundsToRaise().call()
    timeTarget = contract.functions.timeTarget().call()

    st.write("FUNDS TO RAISE-> ", fundsToRaise)
    st.write("TIME TARGET-> ", timeTarget)        
        
    st.markdown("---")
    
#########################################################################################################
#########################################################################################################





##Function to display PDF
def show_pdf(file_path):
    with open(file_path,"rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="500" height="500" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


# Load the data into a Pandas DataFrame
df_movie_data = pd.read_csv(
    Path("Movie-Projects.csv"), index_col = 'Name')
    
#########################################################################################################################
#########################################################################################################################

# CREATE A TAB FOR THE INVESTORS

with tabs[1]:
    st.markdown(f'<h2 style="color:#F78066;font-size:24px;">{"LCA Possible Invesmtments"}</h2>', unsafe_allow_html=True)
    ## Set up image for movie 1 - bgro
    
    with st.expander("PGRO"):
        image_1 = Image.open('film_projects/pgro/pgro.png')
        st.image(image_1, width=400)
    
        st.markdown(f'<p style="color:#F05C30;font-size:20px;">{"Phas Gaye Re Obama (PGRO) is a sequel to the hit film Bach Gaye Re Obama (BGRO). PGRO is a fast paced, fun-filled , hilarious gangster based satirical comedy, larger in scale and scope than its prequel. The story deals with the problems faced by a maid who is ‘used’ by the powerful diplomats abroad and how her challenging their might shakes the corridors of power both in India and the US."}</p>', unsafe_allow_html=True)
    
        ## Table with artist details for Movie-1 - bgro
        st.table(df_movie_data.iloc[0])

    
        ## More details - Display PDF
        if st.button('Get Details on PGRO >>'):
            show_pdf('film_projects/pgro/synopsis.pdf')
    
   


        ## Contribute as USD or ETH as well as providing token/nft options
        def providetokenoptions():
            st.write("Price of this Token is; ", tokenPrice)
            st.write("Maximum count available for this item: ", availableNow)
            
            if tokensAvailable > 0:
                tokenList = []
                for item in range (1,tokensAvailable+1):
                    tokenData = contract.functions.tokenCollection(item).call()
                    tokenList.append(tokenData)
                    tokenSelected=st.sidebar.selectbox("Select Option", tokenList)
                    availableNow = tokenSelected[5]

                if tokenSelected and int(availableNow) > 0:
                    st.write("Selected Token Data")
                    tokenPrice=tokenSelected[3]
                    maxTokens = tokenSelected[4]
                    tokenId = tokenSelected[10]
                    tokenOwner=tokenSelected[0]
                    
                    st.write("token Id=>", type(tokenId), type(tokenPrice), tokenId)
                    st.write(tokenOwner, maxTokens, tokenPrice, availableNow)
                
                    st.markdown(f"[Click to see the Token you selected](https://gateway.pinata.cloud/ipfs/{tokenSelected[4]})")
                
        ## function to confirm transaction & update buyer list        
        def confirmtransaction():
            buyerlist = contract.functions.updateBuyersList(addr,name,tokenId,
                                                int(amt),tokenPrice).transact({'from': addr})
            contract.functions.updateTokenCount(int(tokenId), int(amt)).transact({'from': addr})
            
            buyerlist_df = pd.Dataframe(buyerlist)
            buyerlist_df.to_csv("buyer_list.csv")
            
        ## collect investor data
        def collectinfo():
            with st.form("Collecting User Information", clear_on_submit= True):
                full_name= st.text_input("Full Name")
                wallet_address= st.text_input("Ethereum wallet address")
                st.write("Price of this Token is; ", tokenPrice)
                st.write("Maximum count available for this item: ", availableNow)
                amt= st.number_input("How many do you want", min_value=1, max_value=int(availableNow))
                st.write("Your order will be executed upon the closing date of this campaign")
                cash_amount= st.text_input("USD")
                submit = st.form_submit_button("submit", on_click=confirmtransaction())
    
        if st.button('Contribute to PGRO'):
            providetokenoptions()
            collectinfo()
            
            
    
    ## Set up image for Movie 2
    with st.expander("BGRO"):
        image_2 = Image.open('film_projects/bgro/bgro.png')
        st.image(image_2, width=400)
        st.markdown(f'<p style="color:#F05C30;font-size:20px;">{"The movie is a comedy with satire on recession. The story revolves around a Non-resident- Indian (NRI), Om Shashtri, who lived the American dream and made it big in the US. Then one day, as it happened in America, US economy went into recession and overnight big businesses, banks, and financial institutions crashed."}</p>', unsafe_allow_html=True)


        ## Table with artist details for Movie-2
        st.table(df_movie_data.iloc[1])
    
        if st.button('Get Details on BGRO >>'):
            show_pdf('film_projects/pgro/synopsis.pdf')

## Contribute as USD or ETH
        if st.button('Contribute to PGRO'):
            providetokenoptions()
            collectinfo()
        
    ## Set up image for movie 3
    with st.expander("SJSM"):
        image_3 = Image.open('film_projects/sjsm/sjsm.png')
        st.image(image_3, width=400)
    
        st.markdown(f'<p style="color:#F05C30;font-size:20px;">{"The story is a hilarious and satirical take on Mehngai( (inflation) through a middle class family from a small North Indian City. The family, crushed under the burden of Mehngai. tries to deal with it through an ingenious idea, not realizing the problems they would get tangled into as a result of this idea. It is a hillarious journey of this family battling these issues culminating into a climax that brings tears into your eyes."}</p>', unsafe_allow_html=True)

    
        ## Table with artist details for Movie-3
        st.table(df_movie_data.iloc[2])
    
        if st.button('Get Details on SJSM >>'):
            show_pdf('film_projects/sjsm/synopsis.pdf')

        
        ## Contribute as USD or ETH
        if st.button('Contribute to SJSM'):
            providetokenoptions()
            collectinfo()

        
        
        


        
