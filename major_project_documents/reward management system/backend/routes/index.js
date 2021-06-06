var express = require('express');
var router = express.Router();
var db = require('../connection.js');
var bodyParser = require('body-parser')
var jsonParser = bodyParser.json();
const { wrap } = require('co');
const { join } = require('path');
const moment = require('moment');
const pdf = require('html-pdf');
const thunkify = require('thunkify');
const read = thunkify(require('fs').readFile);
const handlebars = require('handlebars');
var path = "../certificateddocs/";
const pdf_options = { format: 'A4', quality: 150, orientation: "landscape", zoomFactor: "0.5" };
var async = require('asyncawait/async');
var await = require('asyncawait/await');
var fs = require('fs');
var nodemailer = require('nodemailer');
var directoryPath = require("path");


//web3 configuration
var Web3 = require('web3');
// var web3 = new Web3();
var web3 = new Web3(
  new Web3.providers.HttpProvider('https://rinkeby.infura.io/v3/01430c533dcd4c42bd9cc98cff3eb0a4')
);
var tx = require('ethereumjs-tx');
var lightwallet = require('eth-lightwallet');
var txutils = lightwallet.txutils;
var account = "0xabe93970e0f305142629d40e49797b6894d03cba";
web3.eth.defaultAccount = account;
var ABI = [{ "constant": false, "inputs": [{ "name": "n", "type": "string" }], "name": "set", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": true, "inputs": [], "name": "get", "outputs": [{ "name": "", "type": "string" }], "payable": false, "stateMutability": "view", "type": "function" }]
var address = '0xaBe93970E0F305142629D40e49797b6894d03CbA';
var key = 'df83bc5744bf6d7ec9f5dc716c7f2123041b871126109d59a95d90a7a4699ebc';
var contract = web3.eth.contract(ABI);
var contractAddress = '0x03a067144f4a15ddede58f412c60e6ab0c017d42';
var instance = contract.at('0x03a067144f4a15ddede58f412c60e6ab0c017d42');


//Input Decoder
const InputDataDecoder = require('ethereum-input-data-decoder');
const decoder = new InputDataDecoder(ABI);

//crypto
var sha256 = require('sha256');
var Cryptr = require('cryptr'),
  cryptr = new Cryptr('myTotalySecretKey');

//mail
var nodemailer = require('nodemailer');
var transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: 'saivamsi.n@gmail.com',
    pass: 'srikarharsha'
  }
})

//lodash

var lodash = require('lodash');

//multer configuration
var name_file;
var multer = require('multer');
var storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, __dirname + './../verificationdocs/')
  },
  filename: function (req, file, cb) {

    time = Date.now();
    cb(null, file.fieldname + '-' + time)
    name_file = file.fieldname + '-' + time;
  }
})

const upload = multer({ storage: storage });


//transaction sending method
var tx = require('ethereumjs-tx');
var r;
function sendRaw(rawTx, callback) {
  var privateKey = new Buffer(key, 'hex');
  var transaction = new tx(rawTx);
  transaction.sign(privateKey);
  var serializedTx = transaction.serialize().toString('hex');
  web3.eth.sendRawTransaction(
    '0x' + serializedTx, async (err, result) => {
      if (err) {
        console.log(err);
      } else {
        console.log(result);
        callback(result);

      }
    });
}


//transaction options

var txOptions = {
  nonce: web3.toHex(web3.eth.getTransactionCount(address)),
  gasLimit: web3.toHex(800000),
  gasPrice: web3.toHex(20000000000),
  to: contractAddress
}




router.post('/createcertificate', async (req, res) => {

  //Generating PDF
  const generatePDF = wrap(function* () {

    const data = {
      student: {
        name: req.body.name,
        course: req.body.branch,
        year: req.body.year,
        Degree: req.body.Degree
      }
    };

    const source = yield read(join(`${__dirname}/certificate.html`), 'utf-8');
    const template = handlebars.compile(source);
    const html = template(data);
    const p = pdf.create(html, pdf_options);
    p.toFile = thunkify(p.toFile);
    var pa = '../certificateddocs/' + req.body.Debtor_Mailing_Address + '.pdf';
    yield p.toFile(`${join(__dirname, '../certificatedocs/' + req.body.email + '.pdf')}`);
  });

  await generatePDF();


  var filepath = '../certificateddocs/' + req.body.email + 'document.pdf';
  //Saving Record
  var ID = req.body.collegeID;
  var txID = "0zd32dsdsd2ff"+req.body.email;

  await db.query('insert into certificates.Docs values("' + ID + '","' + req.body.email + '","' + req.body.name + '","' + req.body.branch + '","' + req.body.year + '","' + req.body.Degree + '","' + req.body.collegeID + '","' + txID + '","' + filepath + '","0","","");', function (err, result) {
    if (err) throw err;
    else
      console.log(result);
    res.send(result);
  });


});

//college Flag update
router.post('/collegeverify', async (req, res, next) => {

  console.log("here", req.body);


  await db.query('update certificates.Docs set cf="' + req.body.cf + '" where email="' + req.body.ID + '";', function (err, result) {
    if (err) throw err;
    else
      console.log(result);
  });
  console.log("here");



  await db.query('SELECT cf,sf from certificates.Docs where email="' + req.body.ID + '";', function (err, result) {
    console.log("get student details",result,err);
    if (err) throw err;
    else
      console.log(result);
    console.log(result[0].sf);
    if (result[0].sf == 1) {

      console.log("here",__dirname);

      fs.readFile(directoryPath.join(__dirname, '..', 'certificatedocs',   req.body.ID+'.pdf'), async (err, buf) => {

        if (err) {
          console.log(err)
          res.send("error in Reading file" + err);
        }
        else {
          console.log(buf);

          //  await web3.personal.unlockAccount(web3.eth.accounts[0],'hari');
          var d = await sha256(buf);

          //  var rawTx = {
          //       nonce: web3.toHex(web3.eth.getTransactionCount(address)),
          //       gasLimit: web3.toHex(800000),
          //       gasPrice: web3.toHex(20000000000),
          //       data: d
          //                };

          var rawTx = txutils.functionTx(ABI, 'set', [d], txOptions);


          var txhash = await sendRaw(rawTx, async (result) => {
            console.log(result + "*******************************");

            var td = result;


            // var val = await contract_instance.setdata(d,{from:web3.eth.accounts[0],gas:200000},async(error,result) => {
            //   if(error){
            //       console.log(error);
            //   }
            //   else{


            await db.query('update certificates.Docs set Txid="' + td + '" where ID="' + req.body.ID + '";', function (err, result) {
              if (err) {
                res.send("error in updating certificates table" + err);
              }
              else



                var mailoptions = {
                  from: 'saivamsi.n@gmail.com',
                  to: "saivamsi.n@gmail.com",
                  subject: 'Graduation Certificate',
                  text: 'Hi please check your ccertificate Thank you.....!!!!!!! :)   AND your TRANSACTION ID IS  ' + td,
                  attachments: [
                    {

                      'path':directoryPath.join(__dirname, '..', 'certificatedocs',   req.body.ID+'.pdf') // stream this file
                    },
                  ]

                }


              transporter.sendMail(mailoptions, function (err, info) {
                if (err) {
                  console.log(err);
                  res.send({ "status": "0", "message": "failed while creating certificate.....!" });
                }
                else {

                  res.send({ "status": "1", "message": "Certificate Created Successfully" });

                }
              })




            });



            //   }

          });


        }

      });

    }

    else {
      //  console.log(result);
      res.send({ "msg": "Student need to approve certificate" });
    }


  });


});

//Student Flag update
router.post('/studentverify', async (req, res, next) => {
  console.log(req.body);
  await db.query('update certificates.Docs set sf="' + req.body.sf + '"where ID="' + req.body.ID + '";', function (err, result) {
    if (err) {
      res.send("error in updating certificates" + err);
    }
    else
      console.log(result);
    //res.send(result);
  });

  await db.query('SELECT cf,sf from certificates.Docs where email="' + req.body.ID + '";', function (err, result) {
    if (err) {
      res.send("error in getting certificates" + err);
    }
    else
      //console.log(result[0].sf);
      if (result[0].sf == 1 && result[0].cf == 1) {



        fs.readFile('./certificatedocs/' + req.body.email + 'document.pdf', async (err, buf) => {

          if (err) {
            console.log(err);
            res.send("error in reading certificate" + err);
          }
          else {
            console.log(buf);
            //  await web3.personal.unlockAccount(web3.eth.accounts[0],'hari');
            var d = sha256(buf);
            // var rawTx = {
            //   nonce: web3.toHex(web3.eth.getTransactionCount(address)),
            //   gasLimit: web3.toHex(800000),
            //   gasPrice: web3.toHex(20000000000),
            //   data: d
            //            };
            // var txhash = await sendRaw(rawTx,async(result)=>{
            // console.log(result+"*******************************");

            // var td = result;

            console.log(d);
            var rawTx = txutils.functionTx(ABI, 'set', [d], txOptions);


            var txhash = await sendRaw(rawTx, async (result) => {
              console.log(result + "*******************************");

              var td = result;

              await db.query('update certificates.Docs set Txid="' + td + '" where ID="' + req.body.ID + '";', function (err, result) {
                if (err) {
                  res.send(err);
                }
                else



                  var mailoptions = {
                    from: 'dummytest471@gmail.com',
                    to: req.body.email,
                    subject: 'Graduation Certificate',
                    text: 'Hi please check your ccertificate Thank you.....!!!!!!! :)   AND your TRANSACTION ID IS  ' + td,
                    attachments: [
                      {

                        'path': "./certificatedocs/" + req.body.email // stream this file
                      },
                    ]

                  }


                transporter.sendMail(mailoptions, function (err, info) {
                  if (err) {
                    console.log(err);
                    res.send({ "status": "0", "message": "failed while creating certificate.....!" });
                  }
                  else {

                    res.send({ "status": "1", "message": "Certificate Created Successfully" });

                  }
                })

              });
            });
          }
        });
      }
      else {
        res.send("college need to approve certificate");
      }

  });
});

router.post('/validate', upload.single('file-to-upload'), async (req, res, next) => {

  var trid = req.body.transaction_id;
  fs.readFile('./verificationdocs/' + name_file, async (err, buf) => {
    if (err) {
      console.log(err);
      res.send(err);
    }
    else {

      var b = sha256(buf);
      console.log(buf);
      //getting block data
      //console.log(trid);
      var d = await web3.eth.getTransaction(trid);
      //var i = web3.toAscii(d.input);
      console.log(d);
      const rsult = decoder.decodeData(d.input);
      const z = await web3.toAscii(d.input);
      console.log(z + "***********************************");
      const check_value = rsult.inputs[0];

      console.log(b);
      console.log(d.input);
      console.log(rsult);
      console.log(check_value);
      if (lodash.isEqual(b, check_value)) {
        res.send([{ "status": "1", "data": "A valid Document", "id": trid }]);
      } else {
        res.send([{ "status": "0", "data": "Invalid Document or Transaction ID.....!" }]);
      }
    }
  });
});




router.get('/verifiedstudents', async (req, res, next) => {



  await db.query('SELECT * FROM certificates.Docs where UF="1";', function (err, result) {
    if (err) {
      res.send(err);
    } else {
      res.send(result);
    }
  });

});

router.get('/unverifiedstudents', async (req, res, next) => {



  await db.query('SELECT * FROM certificates.Docs where UF="0";', function (err, result) {
    if (err) {
      res.send(err);
    } else {
      res.send(result);
    }
  });

});


router.post('/collegestudents', async (req, res, next) => {



  await db.query('SELECT * FROM certificates.Docs where CollegeID = "' + 'w10084869' + '";', function (err, result) {
    if (err) {
      res.send(err);
    } else {
      res.send(result);
    }
  });

});


router.post('/getstudent', async (req, res, next) => {



  await db.query('SELECT * FROM certificates.Docs where email="' + req.body.email + '";', function (err, result) {
    if (err) {
      res.send(err);
    } else {
      res.send(result);
    }
  });

});


router.post('/universityverify', async (req, res, next) => {

  var obj = req.body;

  var n = obj.length;

  var i;

  for (i = 0; i < n; i++) {

    await db.query("update certificates.Docs set UF='" + 1 + "' where ID ='" + obj[i].ID + "';", function (err, result) {
      if (err) {
        res.send(err);
      }
      else
        console.log(result);

    });


  }




  await db.query('SELECT * FROM certificates.Docs where UF="0";', function (err, result) {
    if (err) {
      res.send(err);
    } else {
      res.send(result);
    }
  });
  // res.send({"msg":"Verified successfully"});


});



module.exports = router;
