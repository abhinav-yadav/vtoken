



// var Web3 = require('web3');
// var web3 = new Web3();
// web3.setProvider(new web3.providers.HttpProvider("https://rinkeby.infura.io/01430c533dcd4c42bd9cc98cff3eb0a4"));
// const contractAbi = [ { "constant": false, "inputs": [ { "name": "ob", "type": "string" } ], "name": "setdata", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": true, "inputs": [], "name": "get", "outputs": [ { "name": "", "type": "string" } ], "payable": false, "stateMutability": "view", "type": "function" } ]
// var contract_addr = "0xb54bE5005FC835332b5d07B00bA899EE31b8FF40";
// var contract_instance = web3.eth.contract(contractAbi).at(contract_addr);

// web3.personal.unlockAccount("0xaBe93970E0F305142629D40e49797b6894d03CbA",'hari',function(err,res){


//     if(err){
//         console.log(err);
//     }

//     else{
//         console.log(res);
//     }
// });

// contract_instance.setdata("hari",{from:"0xaBe93970E0F305142629D40e49797b6894d03CbA",gas:200000},async(error,result) => {
//     if(error){
//         console.log(error);
//     }
//     else{
//      console.log(result);
//     }
// });



// var Web3 = require('web3');
// //var util = require('ethereumjs-util');
// var tx = require('ethereumjs-tx');
// var lightwallet = require('eth-lightwallet');
// //var txutils = lightwallet.txutils;

// var web3 = new Web3(
//     new Web3.providers.HttpProvider('https://rinkeby.infura.io/01430c533dcd4c42bd9cc98cff3eb0a4')
// );

// var address = '0xF8aAaf0bD44EeB305f2CDb73D8d9B616bae6C03e';
// var key = 'dfc048adc6e1dda536a83d518dd0c3c5bb77f99eaadeba334d713350d1a20ea3';

// var bytecode = '608060405234801561001057600080fd5b506102a7806100206000396000f30060806040526004361061004b5763ffffffff7c01000000000000000000000000000000000000000000000000000000006000350416636d4ce63c8114610050578063900cf582146100da575b600080fd5b34801561005c57600080fd5b50610065610135565b6040805160208082528351818301528351919283929083019185019080838360005b8381101561009f578181015183820152602001610087565b50505050905090810190601f1680156100cc5780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b3480156100e657600080fd5b506040805160206004803580820135601f81018490048402850184019095528484526101339436949293602493928401919081908401838280828437509497506101cc9650505050505050565b005b60008054604080516020601f60026000196101006001881615020190951694909404938401819004810282018101909252828152606093909290918301828280156101c15780601f10610196576101008083540402835291602001916101c1565b820191906000526020600020905b8154815290600101906020018083116101a457829003601f168201915b505050505090505b90565b80516101df9060009060208401906101e3565b5050565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f1061022457805160ff1916838001178555610251565b82800160010185558215610251579182015b82811115610251578251825591602001919060010190610236565b5061025d929150610261565b5090565b6101c991905b8082111561025d57600081556001016102675600a165627a7a723058205b6bcd27cf82123e3ba0161350ca807d0ade1d8c5e77907d82cbc69cf39c28420029';
// var interface = [ { "constant": false, "inputs": [ { "name": "ob", "type": "string" } ], "name": "setdata", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": true, "inputs": [], "name": "get", "outputs": [ { "name": "", "type": "string" } ], "payable": false, "stateMutability": "view", "type": "function" } ]

// function sendRaw(rawTx) {
//     var privateKey = new Buffer(key, 'hex');
//     var transaction = new tx(rawTx);
//     transaction.sign(privateKey);
//     var serializedTx = transaction.serialize().toString('hex');
//     web3.eth.sendRawTransaction(
//     '0x' + serializedTx, function(err, result) {
//         if(err) {
//             console.log(err);
//         } else {
//             console.log(result);
//         }
//     });
// }

// var rawTx = {
//     nonce: web3.toHex(web3.eth.getTransactionCount(address)),
//     gasLimit: web3.toHex(800000),
//     gasPrice: web3.toHex(20000000000),
//     data: '0x' + bytecode + '0000000000000000000000000000000000000000000000000000000000000005'
// };

// sendRaw(rawTx);


const Web3 = require('web3');
const web3 = new Web3(new Web3.providers.HttpProvider("https://rinkeby.infura.io/01430c533dcd4c42bd9cc98cff3eb0a4"));
const contractAbi = [ { "constant": false, "inputs": [ { "name": "ob", "type": "string" } ], "name": "setdata", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": true, "inputs": [], "name": "get", "outputs": [ { "name": "", "type": "string" } ], "payable": false, "stateMutability": "view", "type": "function" } ]
var contract_addr = "0xb54bE5005FC835332b5d07B00bA899EE31b8FF40";
var contract_instance = web3.eth.contract(contractAbi).at(contract_addr);
//console.log(contract_instance);
// web3.eth.getBlock("latest", (error, result) => {
//   console.log('error:', error);
//   console.log('results', result);
// });


web3.eth.getTransaction("0x96b74cf61a6a47fd1ad213f44b73285ca20a60a1b5384345a4a5e8e8d84b03b1",function(err,res){
    if(err){
    console.log(err);
    }
    else{
        console.log(res);
    }
})


// web3.eth.getTransactionCount("0xaBe93970E0F305142629D40e49797b6894d03CbA",function(err,result){
//     if(err){
//         console.log(err);
//     }
//     else{
//         console.log("********************************************");
//         console.log(result);
//     }
// })


contract_instance.setdata("hari",{from:"0xaBe93970E0F305142629D40e49797b6894d03CbA",gas:200000},async(error,result) => {
        if(error){
            console.log(error);
        }
        else{
         console.log(result);
        }
    });

// web3.eth.getPastLogs({fromBlock:'0x0',address:'0xb54bE5005FC835332b5d07B00bA899EE31b8FF40'})
// .then(res => {
//   res.forEach(rec => {
//     console.log(rec.blockNumber, rec.transactionHash, rec.topics);
//   });
// }).catch(err => console.log("getPastLogs failed", err));