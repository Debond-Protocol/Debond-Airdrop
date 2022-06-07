import {ethers} from "ethers";
import {default as keys} from "./_keys.json";
import {AirdropInstance, AirdropMintableTokenInstance} from "../types/truffle-contracts";

export interface AirdropModel {
    address: string,
    quantity: string,
    signature: string,
}

const Airdrop = artifacts.require("Airdrop");
const AirdropMintableToken = artifacts.require("AirdropMintableToken");


/*
 INIT GANACHE WITH : ganache-cli -m "stereo consider quality wild fat farm symptom bundle laundry side one lemon" --account_keys_path test/_keys.json
 */

contract('Airdrop', async (accounts: string[]) => {
    let airdropInstance: AirdropInstance;
    let airdropMintableTokenInstance: AirdropMintableTokenInstance;

    const [owner, claimer1, claimer2, claimer3, claimer4, claimerNotAuth]: string[] = accounts

    console.log(keys.private_keys);
    const privateKey = Object.values(keys.private_keys)[0] as string
    const wallet = new ethers.Wallet(privateKey);

    const amount = "4000"

    let airdrops: AirdropModel[];


    it('Initialisation', async () => {
        airdropInstance = await Airdrop.deployed();
        airdropMintableTokenInstance = await AirdropMintableToken.deployed();

        const airdropAddress = airdropInstance.address;
        airdrops = [
            {address: claimer1, quantity: amount, signature: ""},
            {address: claimer2, quantity: amount, signature: ""},
            {address: claimer3, quantity: amount, signature: ""},
            {address: claimer4, quantity: amount, signature: ""},
        ]

        airdrops = await Promise.all(airdrops.map(async (airdrop) => {
            const messageHash = ethers.utils.solidityKeccak256(
                ["address", "address", "uint256"],
                [airdropAddress, airdrop.address, ethers.utils.parseEther(airdrop.quantity)]
            )
            let messageHashBytes = ethers.utils.arrayify(messageHash)
            airdrop.signature = await wallet.signMessage(messageHashBytes);
            return airdrop
        }))

        console.log(airdrops);

        // Setting airdrop On
        await airdropInstance.setAirdropOn();
    })

    it('should airdrop successfully', async () => {
        await airdropInstance.claimAirdrop(ethers.utils.parseEther(amount).toString(), airdrops.filter(airdrop => airdrop.address == claimer1)[0].signature, {from: claimer1})

        const claimerBalance = await airdropMintableTokenInstance.balanceOf(claimer1)
        assert.equal(claimerBalance.toString(), ethers.utils.parseEther(amount).toString())
    })
})
