const AirdropMintableToken = artifacts.require("AirdropMintableToken");

module.exports = async function (deployer, network, accounts) {
    await deployer.deploy(AirdropMintableToken);
  };
