// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

import "@openzeppelin/contracts@4.7.3/token/ERC1155/ERC1155.sol";
import "@openzeppelin/contracts@4.7.3/access/AccessControl.sol";
import "@openzeppelin/contracts@4.7.3/token/ERC1155/extensions/ERC1155Supply.sol";


contract Bolly_ft_and_nft is ERC1155, AccessControl, ERC1155Supply {
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");

    uint256 public rate;

    constructor(uint exchangeRate) ERC1155("") {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(MINTER_ROLE, msg.sender);

        rate = exchangeRate; //wei to token unit
    }

// NftMetaData for NFT assigned to n investor
    struct tokenInfo {
        address owner; //who owns it
        uint256 value;  //price for this one
        uint256 amount; //how many of this nft
        string uri;  //uri of the. token
        string file_hash;

    }

    //Map token id to TokenInfo
    mapping(uint256 => tokenInfo) public tokenCollection;

    uint256 tokenId; //number of tokens registered

// Map tokenId to TokenBalance,i.e. what's left after a sale
    mapping (uint256 => uint256) public tokenBalance;

    mapping (uint256 => string) private _uris;
    mapping (string => uint256) private _idOfUris;

    struct buyer {
        string  name;
        uint256 tokenId;
        uint256 numberOfTokensToBuy;
        uint256 purchasePrice;
    }

// Buyers list is accumulated until the time the campaign is SUCCESSFULLY over, when the tokens are minted,
// transferred to the buyers and money transferred to the issuer. SUCCESS is if the amount raised  = fundsToRaise

    mapping (address => buyer) public buyersList;

    function updateBuyersList( 
                    address buyerAddress,
                    string memory buyersName,
                    uint256 tokenPurchased,
                    uint256 numOfTokens,
                    uint256 pricePaid
                    ) public {
        buyersList[buyerAddress] = buyer(buyersName,
                    tokenPurchased,
                    numOfTokens,
                    pricePaid);
    }

    uint256 public fundsToRaise; // wei
    uint256 public timeTarget; //in seconds

    function setCampaignTarget(uint256 ethToRaise, uint256 timeInSeconds) public {
        fundsToRaise = ethToRaise * rate * 1000000000000000000;
        timeTarget = timeInSeconds;
    }


    function mint(address account, uint256 id, uint256 amount, bytes memory data)
        public
        onlyRole(MINTER_ROLE)
    {
        _mint(account, id, amount, data);
    }

    function mintBatch(address to, uint256[] memory ids, uint256[] memory amounts, bytes memory data)
        public
        onlyRole(MINTER_ROLE)
    {
        _mintBatch(to, ids, amounts, data);
    }

    // The following functions are overrides required by Solidity.

    function _beforeTokenTransfer(address operator, address from, address to, uint256[] memory ids, uint256[] memory amounts, bytes memory data)
        internal
        override(ERC1155, ERC1155Supply)
    {
        super._beforeTokenTransfer(operator, from, to, ids, amounts, data);
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC1155, AccessControl)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }



    function registerToken(
        address owner,  //who owns
        // the below two items not needed as we r handling it in the streamlit interface
        //string memory filmName, //film name 
       // string memory nftItem,  //nftitem name
        uint256 initialPrice, //price
        uint256 howMany,  //how many
        string memory nftURI,  //uri of the nft
        string memory file_hash, // hash of nft on ipfs
        bytes memory data //associated data if any. 0x0000 if not
    ) public returns (uint256) {
        //uint256 tokenId;

        tokenId +=1; 

         _mint(owner, tokenId, howMany, data);
         //_setURI(nftURI);

        tokenCollection[tokenId] = tokenInfo(owner, initialPrice, howMany, nftURI, file_hash);
        tokenBalance[tokenId] = howMany; //initialize the totalcount of this token
        _uris[tokenId] = nftURI;  // uri of the token  mapped to tokenID
        _idOfUris[nftURI] = tokenId;  // tokenId mapped to Uri
  
        return tokenId;
    }
 
 // get Uri from the Id of the token
    function getUri( uint256 tokenId) public view returns (string memory) {
        return _uris[tokenId];
    }

// get TokenId from the Uri of the token

    function getIdFromUri(string memory uri) public view returns (uint256) {
        return _idOfUris[uri];
    }

// token count per tokenId available for sale
    function tokenCount(uint256 Id) public view returns (uint256) {
        return tokenBalance[Id];
    }

// upon a sale, reduce the token balance for that token

    function updateTokenCount(uint256 Id, uint256 count) public {
        // While selling the token, it shd be checked if there is enough to sell
        // Here we assume that there was enough to sell, so balance will NOT be negative

        tokenBalance[Id] -= count;

    }
// number of types of tokens available for sale. For each token there is ONE item in case of a NFT
// and in case of FT (fungible token) there are generally MORE than ONE copies of the same item for that TOKEN
// do not confuse this numberOfTokens from total number of items for sale, which could be significantly large
// for example - you may have 3 NFTs (one item) for special edition picture of MonaLisa, RobertDeniro, Amitabh Bacchan
// while, you may 100 of copies of the poster of BOBBY film. This poster would be one token, but it will have 100 copies.
// so, in this case total numberOfTokens would return 4.

    function numberOfTokens() public view returns (uint256) {
        return tokenId;
    }



}
