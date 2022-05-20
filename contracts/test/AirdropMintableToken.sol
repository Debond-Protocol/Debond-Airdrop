// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "../interfaces/IAirdropMintableToken.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";


contract AirdropMintableToken is ERC20, AccessControl, IAirdropMintableToken {

    bytes32 public constant ISSUER_ROLE = keccak256("ISSUER_ROLE");

    constructor() ERC20("DBIT", "DBIT"){
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
    }

    function mintAirdroppedSupply(address _to, uint _amount) external onlyRole(ISSUER_ROLE) {
        _mint(_to, _amount);
    }
}
