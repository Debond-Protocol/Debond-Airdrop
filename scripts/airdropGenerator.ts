import {ethers} from "ethers";
import fs from "fs";
import path from "path";
require('dotenv').config();


export interface Airdrop {
    address: string,
    quantity: number,
    signature: string,
}
const contractAddress = process.env.CONTRACT_ADDRESS;
let airdrops: Airdrop[] = [
    // {address: "0xC8455Bc3C600a0A79A5c77BdA7d820eA44513845", quantity: 1, signature: ""},
    // {address: "0xc35B4C67bB57D20ba31961c9dce7dFc3FD7deF1c", quantity: 1, signature: ""},
    // {address: "0x45b549dD6ba1647a65bCd3593ecA3dCb12242e16", quantity: 1, signature: ""},
    // {address: "0x10E7F7CECbE3Cc1ecC69ab45Cb5a996a2418a298", quantity: 1, signature: ""},
    // {address: "0x7EbfEE4CE6d2674509be8769EcFFAd37592E4cA4", quantity: 1, signature: ""},
    // {address: "0x9aB76722764aBFAD7dbAc8BF68c9Ef8587C53D86", quantity: 3, signature: ""},
    // {address: "0x00d08633db2c0955a20b0a9ce123d8f354005547", quantity: 1, signature: ""},
    // {address: "0xA706D17E412298b0d363B63285cCe5108517Fea1", quantity: 1, signature: ""},
    // {address: "0xd92954168Ea3382c9f6715B3e9C0169F6Ffd720e", quantity: 3, signature: ""},
    // {address: "0x45fd2300e2Fc589A45c205394Eb48613D22F5D7E", quantity: 1, signature: ""},
    // {address: "0x2e911ea270e5c6f9e2ef7aB10a35eac7D5F73f96", quantity: 1, signature: ""},
]
let wallet = new ethers.Wallet(String(process.env.MAINNET_PRIVATE_KEY));

Promise.all(airdrops.map(async (airdrop) => {
    const messageHash = ethers.utils.solidityKeccak256(
        ["address", "address", "uint256"],
        [contractAddress, airdrop.address, airdrop.quantity]
    )
    let messageHashBytes = ethers.utils.arrayify(messageHash)
// console.log(messageHash)
    airdrop.signature = await wallet.signMessage(messageHashBytes);
    return airdrop
})).then(airdropsWithSign => {
    fs.writeFile(
        path.dirname(__filename) + "/airdrops.json",
        JSON.stringify(airdropsWithSign),
        err => {
            err ? console.log(err) : ""
        }
    )
})
