const Airdrop = artifacts.require("Airdrop");
const AirdropMintableToken = artifacts.require("AirdropMintableToken");


module.exports = async function (deployer, network, accounts) {
    const airdropMintableToken = await AirdropMintableToken.deployed();
    await deployer.deploy(Airdrop, airdropMintableToken.address);

    const airdropContract = await Airdrop.deployed();
    const ISSUER_ROLE = await airdropMintableToken.ISSUER_ROLE();
    await airdropMintableToken.grantRole(ISSUER_ROLE, airdropContract.address);
};
