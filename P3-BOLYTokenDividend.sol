/* DividendTokens for smartContracts 

Dividends are a form of distribution of a company's earnings to its shareholders and is determined by 
the company's board of directors. Coorespondingly, cryptoCurrency tokens can payout profits to its investor as 
dividends is a dividend token. 
For Lights_Camera_Action dividends are also royalties from NFTs, which we will call `RoyalDivs` as a way to send
 royalties from intellectual property returns from videos, music, games, and creative returns from the metaverse.
There are multiple ways to pay the dividend in the token economy. 
Dividends are standard practice to distribute earnings to investors. Dividends also create a passive income 
    source for your investors. This will attract long-term investors and create incentives for holding tokens. */

pragma solidity ^0.5.0;

import "github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/math/SafeMath.sol"; 


contract DividendToken{
 
    using SafeMath for uint256;

    string public name = "Dividend Token";
    string public symbol = "DIV";
    uint8 public decimals = 0;  
    uint256 public totalSupply_ = 1000000;           /* Total token supply */
    uint256 totalDividendPoints = 0;                 /* Total dividend which is given till now */
    uint256 unclaimedDividends = 0;                  /* balance of unclaimed dividends. */ 
    uint256 pointMultiplier = 1000000000000000000;   /* 10¹⁸ as wei multiplier to tackle rounding errors */ 
    address owner;                                   /* owner address of the smart contract */

    
    struct account{
         uint256 balance;
         uint256 lastDividendPoints;
     }

    mapping(address => account) public balanceOf;
    
    event Transfer(
        address indexed from,
        address indexed to,
        uint256 value
    );


    event Approval(
    address indexed owner,
    address indexed spender,
    uint256 value
    );

    modifier onlyOwner() {
    require(msg.sender == owner);
    _;
    }

    modifier updateDividend(address investor) {
    uint256 owing = dividendsOwing(investor);
    if(owing > 0) {
        unclaimedDividends = unclaimedDividends.sub(owing);
        balanceOf[investor].balance = balanceOf[investor].balance.add(owing);
        balanceOf[investor].lastDividendPoints = totalDividendPoints;
        }
     _;
    }

    constructor () public {
        // Initially assign all tokens to the contract's creator.
        balanceOf[msg.sender].balance = totalSupply_;
        owner = msg.sender;
        emit Transfer(address(0), msg.sender, totalSupply_);
    }
    
    /**
    This is the main logic to calculate dividends and will only be called by the contract owner. It will calculate
    dividends owed by an account and calls the `dividendsOwing` method, after finding out what dividends are 
    owed to an account updates are madde to `unclaimedDividends` variable and then will update investor’s account
    balance and `lastDividendPoints`.
     new dividend = totalDividendPoints - investor's lastDividnedPoint
     ( balance * new dividend ) / points multiplier
    **/

    function dividendsOwing(address investor) internal returns(uint256) {
        uint256 newDividendPoints = totalDividendPoints.sub(balanceOf[investor].lastDividendPoints);
        return (balanceOf[investor].balance.mul(newDividendPoints)).div(pointMultiplier);
    }

    /**
    The `disburse` function will be called to pay dividends to the contract which will increase `totalDividendPoints`, 
    `totalSupply_` and `unclaimedDividends`.
    totalDividendPoints += (amount * pointMultiplier ) / totalSupply_
    **/
    function disburse(uint256 amount)  onlyOwner public{
    totalDividendPoints = totalDividendPoints.add((amount.mul(pointMultiplier)).div(totalSupply_));
    totalSupply_ = totalSupply_.add(amount);
    unclaimedDividends =  unclaimedDividends.add(amount);
    }

    function totalSupply() public view returns (uint256) {
    return totalSupply_;
    }
/* transfer of token royaldivs to investor account aaddress*/
   function transfer(address _to, uint256 _value) updateDividend(msg.sender) updateDividend(_to) public returns (bool) {
    require(msg.sender != _to);
    require(_to != address(0));
    require(_value <= balanceOf[msg.sender].balance);
    balanceOf[msg.sender].balance = (balanceOf[msg.sender].balance).sub(_value);
    balanceOf[_to].balance = (balanceOf[_to].balance).add(_value);
    emit Transfer(msg.sender, _to, _value);
    return true;
  }
 
  function balanceOf_(address _owner) public view returns (uint256) {
    return balanceOf[_owner].balance;
  }


   mapping (address => mapping (address => account)) internal allowed;


 
  function transferFrom(
    address _from,
    address _to,
    uint256 _value
  )
    updateDividend(_from)
    updateDividend(_to)
    public
    returns (bool)
  {
    require(_to != _from);
    require(_to != address(0));
    require(_value <= balanceOf[_from].balance);
    require(_value <= (allowed[_from][msg.sender]).balance);

    balanceOf[_from].balance = (balanceOf[_from].balance).sub(_value);
    balanceOf[_to].balance = (balanceOf[_to].balance).add(_value);
    (allowed[_from][msg.sender]).balance = (allowed[_from][msg.sender]).balance.sub(_value);
    emit Transfer(_from, _to, _value);
    return true;
  }
/* owner approval for royaldiv disbursement */
  function approve(address _spender, uint256 _value) public returns (bool) {
    (allowed[msg.sender][_spender]).balance = _value;
    emit Approval(msg.sender, _spender, _value);
    return true;
  }

  
  function allowance(
    address _owner,
    address _spender
   )
    public
    view
    returns (uint256)
  {
    return (allowed[_owner][_spender]).balance;
  }

 
  function increaseApproval(
    address _spender,
    uint _addedValue
  )
    public
    returns (bool)
  {
    (allowed[msg.sender][_spender]).balance = (
      (allowed[msg.sender][_spender]).balance.add(_addedValue));
    emit Approval(msg.sender, _spender, (allowed[msg.sender][_spender]).balance);
    return true;
  }

  
  function decreaseApproval(
    address _spender,
    uint _subtractedValue
  )
    public
    returns (bool)
  {
    uint oldValue = (allowed[msg.sender][_spender]).balance;
    if (_subtractedValue > oldValue) {
      (allowed[msg.sender][_spender]).balance = 0;
    } else {
      (allowed[msg.sender][_spender]).balance = oldValue.sub(_subtractedValue);
    }
    emit Approval(msg.sender, _spender, (allowed[msg.sender][_spender]).balance);
    return true;
  }


}