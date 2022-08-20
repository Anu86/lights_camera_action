// SPDX-License-Identifier: MIT
pragma solidity ^0.5.5;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

contract FilmRegistry is ERC721Full {
    constructor() public ERC721Full("FilmRegistryToken", "FILM") {}

    struct filmWork {
        string name;
        string title;
        uint256 appraisalValue;
    }

    mapping(uint256 => filmWork) public filmCollection;

    event Appraisal(uint256 tokenId, uint256 appraisalValue, string reportURI);

    function registerFilmwork(
        address owner,
        string memory name,
        string memory title,
        uint256 initialAppraisalValue,
        string memory tokenURI
    ) public returns (uint256) {
        uint256 tokenId = totalSupply();

        _mint(owner, tokenId);
        _setTokenURI(tokenId, tokenURI);

        filmCollection[tokenId] = filmWork(name, title, initialAppraisalValue);

        return tokenId;
    }

    function newAppraisal(
        uint256 tokenId,
        uint256 newAppraisalValue,
        string memory reportURI
    ) public returns (uint256) {
        filmCollection[tokenId].appraisalValue = newAppraisalValue;

        emit Appraisal(tokenId, newAppraisalValue, reportURI);

        return filmCollection[tokenId].appraisalValue;
    }
}