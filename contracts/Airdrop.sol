pragma solidity ^0.8.0;

// SPDX-License-Identifier: apache 2.0
/*
    Copyright 2022 Debond Protocol <info@debond.org>
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
*/

import "./interfaces/IAirdropMintableToken.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";


contract Airdrop is Ownable {

    using ECDSA for bytes32;


    address airdropMintableTokenAddress;
    bool public airdropOn = false;
    mapping(address => bool) public withdrawClaimed;

    constructor(
        address _airdropMintableTokenAddress
    ) {
        airdropMintableTokenAddress = _airdropMintableTokenAddress;
    }


    modifier isClaimedAuthorized(uint256 quantity, bytes memory signature) {
        require(verifySignature(quantity, signature) == owner(), "caller not authorized to get airdrop");
        _;
    }

    function claimAirdrop(uint256 _amount, bytes memory _signature) external isClaimedAuthorized(_amount, _signature) {
        require(airdropOn == true, "Airdrop is Off");
        require(!withdrawClaimed[msg.sender], "caller already got airdropped");
        IAirdropMintableToken(airdropMintableTokenAddress).mintAirdroppedSupply(msg.sender, _amount);
        withdrawClaimed[msg.sender] = true;
    }

    function verifySignature(uint256 quantity, bytes memory signature) internal view returns (address) {
        return keccak256(abi.encodePacked(address(this), msg.sender, quantity))
        .toEthSignedMessageHash()
        .recover(signature);
    }


    function setAirdropOn() external onlyOwner {
        require(airdropOn == false, "Airdrop already On.");
        airdropOn = true;
    }

    function setAirdropOff() external onlyOwner {
        require(airdropOn == true, "Airdrop already Off.");
        airdropOn = false;
    }
}
