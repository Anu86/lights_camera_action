# lights_camera_action

LIGHT-CAMERA-ACTION (LCA).
1. Creator Submission:
a.  gets to submit his/her proposal to LCA through a web/streamlit  
interface. The data is vetted by the Creative Team at LCA and if 
approved, then only the data is stored in our system:
b. The data received from the CREATOR is stored in a directory tree
as follows: 
(here pgro is the film acronym for my film Phas Gaye Re Obama, 
as an example)
       app.py
       contracts
bolly.sol
compiled
- bolly.json
      my.env
      film_projects.csv 
( has summary data for all the projects, including budget 
and timeframe- both of which will be used during fund 
raising, profits etc)
      film_projects
- pgro
- pgro.png
- synopsis.pdf
- project.csv. (will contain all the project 
costs,incl profits)
- sjsm
- sjsm.png
- synopsis.pdf
- project.csv
- bgro
- bgro.png
- synopsis.pdf
- project.csv
And so on...
2. The Investors:
a. The stored film files are picked by the streamlit app.py program 
to display the film projects available
b. The investor selects one of these film projects after reviewing the
details.
c. The investor demonstrates his interest in making the investment.
d. He/she is presented with the various options to invest.
e. Investor selects the investment amount and mode of payment.
f. Coin is minted and assigned to him
g. The process repeats itself for other investors until the target is 
reached
h. If the target is not reached
i.  we have the option to extend the deadline
ii. return the funds
iii. have the funds converted to Bollycoin and keep for future 
investment
During Film Production – Certain NFTs will be created which will be sold/ 
awarded at privileged prices to investors along with invitation to certain 
exclusive film events.
3. Award allocation/disbursement : 
The film is produced and after full exploitation, profits are calculated
and shared in a preset tier levels to the investors based upon their 
level of investment –
a. cash/USD
b. ETH
c. BollyCoin
d. Film NFTs
There are three distinct areas of software development tightly connected to 
each other. These are listed as 3 items above, i.e. Creator Submission, 
Investor Action, and Profit/Award dissemination.   
Creator Submission:
Streamlit/ Python based program to accept the proposal in pdf, .png form. 
(we can also ask for the budget in excel or csv form). The app will 
store these in the respective directories as mentioned above.
Investor Action:
This is the main app.py Streamlit program that drives the investment 
process with Solidity contract at the backend. There will be a separate 
contract for each film project. That’s why the director structure is made to 
keep all the film/project material stored in their respective folders. This will 
facilitate ease of automation as well. The details of the flow is mentioned 
above in step 2.
After the investor target is reached, the movie production commences and 
during and until theatrical or net release, certain promotional events will 
initiate creation of NFTs which will be provided to certain investors on either 