# Debond-Airdrop: 

- This repo consist of Airdrop contract that allows to  allot the fixed airdropSupply of DBIT/DGOV tokens to the whitelisted users with fixed quantity. 

- Also its one time claimable contract  with efficient implementation.

- It can be thoretically scalable to large scale airdrop addresses as the signature generation and storage is offchain, but the verification is onchain.

## Deployment steps: 

- First the token to be airdropped is deployed from Debond-Token repo.
- Then using the address of token as constructor parameter, we deploy the Airdrop token with the parameter as the token address that needs to be airdropped.
-  Then the DebondToken.setAirdropAddress(...) needs to be initialized in order to permit the Airdrop contract to call the `mintAirdropToken(...)` method.
- Create the signature of the whitelisted address offline (by the deployer), this will be including the address , their quantities and their amount. put all of these details in the airdropTokenGenerator address.
- Then  each of the whitelist users  can then claim from the contract by calling claimAirdrop(...) method with their address
- whenever the duration of the airdrop needs to be closed, the airdropOff can be called by the owner of the contract (which is the governance contract for Debond protocol).
