
pragma solidity 0.8.4;

import { ERC20 } from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import { Ownable } from "@openzeppelin/contracts/access/Ownable.sol";
import { ReentrancyGuard } from "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract BollyToken is Ownable, ReentrancyGuard, ERC20 {

    uint256 constant public MAX_SUPPLY = 100 ether;
    uint32 constant private MULTIPLIER = 1e9;   // in gwei

    /* Eth share of each token in gwei */
    uint256 dividendPerToken;
    mapping(address => uint256) xDividendPerToken;

    /* Amount credited to account address for withdraw*/
    mapping (address => uint256) credit;

    /* variable representing amount withdrawn by account in ETH */
    mapping (address => uint256) debt;

    /* If 'locked' is true, users prohibited from withdrawing funds */
    bool public locked;

    event FundsReceived(uint256 amount, uint256 dividendPerToken);

    modifier mintable(uint256 amount) {
        require(amount + totalSupply() <= MAX_SUPPLY, "amount surpasses max supply");
        _;
    }
    modifier isUnlocked() {
        require(!locked, "contract is currently locked");
        _;
    }

    receive() external payable {
        require(totalSupply() != 0, "No BollyTokens minted");
        dividendPerToken += msg.value * MULTIPLIER / totalSupply(); 

        // gwei Multiplier decreases impact of remaining tokens */
        emit FundsReceived(msg.value, dividendPerToken);
    }

    constructor(string memory name_, string memory symbol_) ERC20(name_, symbol_) {
        locked = true;
    }

    function mint(address to_, uint256 amount_) public onlyOwner mintable(amount_) {
        _withdrawToCredit(to_);
        _mint(to_, amount_);
    }

    function toggleLock() external onlyOwner {
        locked = !locked;
    }

    /* Withdraw `Eth` from contract onto the caller w.r.t balance of token held by caller */
    /* Reentrancy Guard modifier from line8 is to protect the transaction from reentrancy attack */
    function withdraw() external nonReentrant isUnlocked {
        uint256 holderBalance = balanceOf(_msgSender());
        require(holderBalance != 0, "BollyToken: caller possesses no BOLY");

        uint256 amount = ( (dividendPerToken - xDividendPerToken[_msgSender()]) * holderBalance / MULTIPLIER);
        amount += credit[_msgSender()];
        credit[_msgSender()] = 0;
        xDividendPerToken[_msgSender()] = dividendPerToken;

        (bool success, ) = payable(_msgSender()).call{value: amount}("");
        require(success, "BollyToken: Could not withdraw eth");
    }

    /* for extraordinary cases (i.e.lost tokens) leads to unaccessed funds, owner can use this function
    // this function requires trust from the community; hence, requires discussion for agreement */
    function emergencyWithdraw() external onlyOwner {
        (bool success, ) = payable(owner()).call{value: address(this).balance}("");
        require(success, "DToken: Could not withdraw eth");

    }


    //=================================== INTERNAL ============================================== 
    function _beforeTokenTransfer(
        address from,
        address to,
        uint256 amount
    ) internal override {
        if(from == address (0) || to == address(0)) return;
        // receiver first withdraw funds to credit
        _withdrawToCredit(to);
        _withdrawToCredit(from);
    }

    //=================================== PRIVATE ============================================== 

    function _withdrawToCredit(
        address to_
    ) private
    {
        uint256 recipientBalance = balanceOf(to_);
        if(recipientBalance != 0) {
            uint256 amount = ( (dividendPerToken - xDividendPerToken[to_]) * recipientBalance / MULTIPLIER);
            credit[to_] += amount;
        }
        xDividendPerToken[to_] = dividendPerToken;
    }

}