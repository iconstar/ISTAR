import IconService, { IconAmount, IconConverter, HttpProvider, IconWallet, IconBuilder, SignedTransaction } from 'icon-sdk-js';
// // cx37d5799e548048ba19566e3d018e77a9392b1cc2
// // cx6ad3a41000e745a811132501dbc9cc96c67ac6dc

// default 
const httpProvider = new HttpProvider('http://127.0.0.1:9000/api/v3');
const iconService = new IconService(httpProvider);

// builder
const CallBuilder = IconService.IconBuilder.CallBuilder;
const IcxTransactionBuilder = IconService.IconBuilder.IcxTransactionBuilder;

// service 
const iconWallet = IconService.IconWallet;
const signedTransaction = IconService.SignedTransaction;


// document.getElementById("normalCard").onclick = transaction(1);
var nomalCard = document.getElementById("normalCard");
var rareCard = document.getElementById("rareCard");
var UniqueCard = document.getElementById("UniqueCard");

window.addEventListener("ICONEX_RELAY_RESPONSE", eventHandler, false);
// type and payload are in event.detail

var grade = 0;

function eventHandler(event) {
    var type = event.detail.type;
    var payload = event.detail.payload;

    switch (type) {
        case "RESPONSE_HAS_ACCOUNT":
            console.log("> Result : " + payload.hasAccount + " (" + typeof payload.hasAccount + ")");
            break;
        case "RESPONSE_HAS_ADDRESS":
            console.log("2");
            break;
        case "RESPONSE_ADDRESS":
            console.log("> Selected ICX Address : " + payload);
            fromAddress = payload;
            break;
        case "RESPONSE_JSON-RPC":
            console.log("카드 1강: "+JSON.stringify(payload));

            // 카드 등급 정하기
            if(grade===0) {
                console.log("error grade is 0"+grade);
                alert("error")
            } else {
                console.log("grade is: "+grade);
                myCard(grade);
            }

            break;
        case "CANCEL_JSON-RPC":
            console.log("CANCEL_JSON-RPC");
            break;
        case "RESPONSE_SIGNING":
            console.log("RESPONSE_SIGNING6");
            break;
        case "CANCEL_SIGNING":
            console.log("CANCEL_SIGNING");
            break;
        default:
    }
}


nomalCard.onclick = function() {
    grade = String(1);
    var icxTransactionBuilder = new IconBuilder.IcxTransactionBuilder;
    var icxTransferData = icxTransactionBuilder
        .from("hx08711b77e894c3509c78efbf9b62a85a4354c8df")
        .to("hx79e7f88e6186e72d86a1b3f1c4e29bd4ae00ff53")
        .nid(IconConverter.toBigNumber(3))
        .value(IconAmount.of(1, IconAmount.Unit.ICX).toLoop())
        .timestamp((new Date()).getTime() * 1000)
        .version(IconConverter.toBigNumber(3))
        .stepLimit(IconConverter.toBigNumber(1000000))
        .build();
    
    var score_sdk = JSON.stringify( {
        "jsonrpc":"2.0",
        "method":"icx_sendTransaction",
        "params":IconConverter.toRawTransaction(icxTransferData),
        "id":50889
    })

    var parsed = JSON.parse(score_sdk)

    window.dispatchEvent(new CustomEvent('ICONEX_RELAY_REQUEST', {
        detail: {
            type: 'REQUEST_JSON-RPC',
            payload: parsed,
        }
    })); 
   


   
    
    // console.log("score_sdk: "+score_sdk)

    // var parsed = {"jsonrpc":"2.0","method":"icx_sendTransaction","params":
    // {"to":"hx79e7f88e6186e72d86a1b3f1c4e29bd4ae00ff53","from":"hx08711b77e894c3509c78efbf9b62a85a4354c8df",
    // "stepLimit":"0x186a0","nid":"0x3","version":"0x3","timestamp":"0x5824e2938f1b8","value":"0xde0b6b3a7640000"},
    // "id":50889}

    // window.dispatchEvent(new CustomEvent('ICONEX_RELAY_REQUEST', {
    //     detail: {
    //         type: 'REQUEST_JSON-RPC',
    //         payload: parsed
    //     }
    // }))

    // console.log("test");
    // transaction(1);
    // myCard("1")
}

rareCard.onclick = function() {
    grade = String(2);

    var icxTransactionBuilder = new IconBuilder.IcxTransactionBuilder;
    var icxTransferData = icxTransactionBuilder
        .from("hx08711b77e894c3509c78efbf9b62a85a4354c8df")
        .to("hx79e7f88e6186e72d86a1b3f1c4e29bd4ae00ff53")
        .nid(IconConverter.toBigNumber(3))
        .value(IconAmount.of(2, IconAmount.Unit.ICX).toLoop())
        .timestamp((new Date()).getTime() * 1000)
        .version(IconConverter.toBigNumber(3))
        .stepLimit(IconConverter.toBigNumber(1000000))
        .build();
    
    var score_sdk = JSON.stringify( {
        "jsonrpc":"2.0",
        "method":"icx_sendTransaction",
        "params":IconConverter.toRawTransaction(icxTransferData),
        "id":50889
    })

    var parsed = JSON.parse(score_sdk)

    window.dispatchEvent(new CustomEvent('ICONEX_RELAY_REQUEST', {
        detail: {
            type: 'REQUEST_JSON-RPC',
            payload: parsed
        }
    })); 
}

UniqueCard.onclick = function() {
    grade = String(3);

    var icxTransactionBuilder = new IconBuilder.IcxTransactionBuilder;
    var icxTransferData = icxTransactionBuilder
        .from("hx08711b77e894c3509c78efbf9b62a85a4354c8df")
        .to("hx79e7f88e6186e72d86a1b3f1c4e29bd4ae00ff53")
        .nid(IconConverter.toBigNumber(3))
        .value(IconAmount.of(3, IconAmount.Unit.ICX).toLoop())
        .timestamp((new Date()).getTime() * 1000)
        .version(IconConverter.toBigNumber(3))
        .stepLimit(IconConverter.toBigNumber(1000000))
        .build();
    
    var score_sdk = JSON.stringify( {
        "jsonrpc":"2.0",
        "method":"icx_sendTransaction",
        "params":IconConverter.toRawTransaction(icxTransferData),
        "id":50889
    })

    var parsed = JSON.parse(score_sdk)

    window.dispatchEvent(new CustomEvent('ICONEX_RELAY_REQUEST', {
        detail: {
            type: 'REQUEST_JSON-RPC',
            payload: parsed,
        }
    })); 
    // transaction(3);
    // myCard("3")
}

async function myCard(_grade) {
    var call = new CallBuilder()
        .from("hx08711b77e894c3509c78efbf9b62a85a4354c8df")
        .to('cx37d5799e548048ba19566e3d018e77a9392b1cc2')
        .method('createCard')
        .params({ 
            "_grade":_grade
        })
        .build()

    let card = await iconService.call(call).execute(); 
    console.log("card: "+card);
}




// async function transaction(cardPrice) {
//     console.log("cardPrice: "+cardPrice);
//     const txObj = new IcxTransactionBuilder()
//         .from('hx08711b77e894c3509c78efbf9b62a85a4354c8df')
//         .to('cx37d5799e548048ba19566e3d018e77a9392b1cc2')
//         .value(IconAmount.of(cardPrice, IconAmount.Unit.ICX).toLoop())
//         .stepLimit(IconConverter.toBigNumber(10000000))
//         .nid(IconConverter.toBigNumber(3))
//         .nonce(IconConverter.toBigNumber(1))
//         .version(IconConverter.toBigNumber(3))
//         .timestamp((new Date()).getTime() * 1000)
//         .build()
//     // Returns raw transaction object
//     // const rawTxObj = IconConverter.toRawTransaction(txObj)
//     const SignedTransaction = new signedTransaction(txObj, iconWallet.loadPrivateKey("5c2e41d402a9b5c8c468d5c309129cd48a07abf3be8c4d8ee9f9e71f29c4d040"));
//     const txHash = await iconService.sendTransaction(SignedTransaction).execute();
//     console.log(txHash)
// }