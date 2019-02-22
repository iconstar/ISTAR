// 아이콘 2초 ㅋㅋㅋㅋ 10초걸리는데??ㅋㅋㅋㅋ  (로컬이라서 그런가?)

import IconService, { IconAmount, IconConverter, HttpProvider, IconWallet, IconBuilder, SignedTransaction } from 'icon-sdk-js';

// httpProvider = new HttpProvider();
const httpProvider = new HttpProvider('http://127.0.0.1:9000/api/v3');
const iconService = new IconService(httpProvider);
const CallBuilder = IconService.IconBuilder.CallBuilder;

// service 
const IcxTransactionBuilder = IconService.IconBuilder.IcxTransactionBuilder;
const signedTransaction = IconService.SignedTransaction;
const iconWallet = IconService.IconWallet;

// 커스텀 변수
var score_to = 'cxdacd3169934b4da8ab0141c5f6c2b74ce320fd67';
var addr_to = 'hxc22ae778606f626c03815a5adc41da4a1dad6b4f';
var address = getParameterByAddress('address');

// var price_value = parseInt(document.getElementById('input_price').value);
// console.log("price_: "+price_value);
// console.log("price_value: "+price_value.value);

// 이벤트 핸들러
window.addEventListener("ICONEX_RELAY_RESPONSE", eventHandler, false);

let current = '';

// 로딩바 바로 사라지게하기 위해
$('#loading').hide();  

// 소유자의 카드 보여줌
myCard();


// 게임 시작 버튼 클릭시
document.getElementById('gameStart').addEventListener('click', async () => {
    $('#modal').hide();
    var date = new Date();
    // currentTime = date.getTime();
    current = String(date.getTime());
    
    // console.log("date.getTime(): "+date.getTime());
    console.log("gameStart()1, current: "+current)
    console.log("gameStart()1, current: "+typeof(current))

    // await this.readFile();
    var price = parseInt(document.getElementById('price_number').value);

    // var price = Number(price_value);
    // console.log("price: "+price);
    console.log("price: "+typeof(price));
    
    var callTransactionBuilder = new IconBuilder.CallTransactionBuilder;
    var callTransactionData = callTransactionBuilder
        .from(address)
        .to(score_to)
        .nid(IconConverter.toBigNumber(3))
        .value(IconAmount.of(Number(price), IconAmount.Unit.ICX).toLoop())
        .timestamp((new Date()).getTime() * 1000)
        .stepLimit(IconConverter.toBigNumber(10000000))
        .version(IconConverter.toBigNumber(3))
        .method('startGame')
        .params({  
            "_time": current
        })
        .build();

    var score_sdk = JSON.stringify( {
        "jsonrpc":"2.0",
        "method":"icx_sendTransaction",
        "params":IconConverter.toRawTransaction(callTransactionData),
        "id":50889
    })

    var parsed = JSON.parse(score_sdk)
    console.log("parsed: "+parsed);
    window.dispatchEvent(new CustomEvent('ICONEX_RELAY_REQUEST', {
        detail: {
            type: 'REQUEST_JSON-RPC',
            payload: parsed,
        }
    })); 

    $('#loading').show();
});

// 게임한 결과를 가져옴
async function gemeResult() {
    current = String(current)
    if(current === '') {
        console.log("에러!!");
    } else {
        var call = new CallBuilder()
        .from(address)
        .to(score_to)
        .method('getGameResult')
        .params({
            "_time":current
        })
        .build()

        var gameResult = await iconService.call(call).execute(); 
        if(gameResult == 1) {
            window.open("../../win.html", "a", "width=500, height=500, left=520, top=100");
            console.log("win, You earned an icx.");
        } else if(gameResult == 0) {
            window.open("../../lose.html", "a", "width=500, height=500, left=520, top=100");
            console.log("lose, At the  time.");
        } else {next
            alert("에러!!")
        }
    }
}

// 이벤트 핸들러 - ICONex
function eventHandler(event) {
    var type = event.detail.type;
    var payload = event.detail.payload;

    switch (type) {
        case "RESPONSE_JSON-RPC":
            console.log("RESPONSE_JSON-RPC: "+JSON.stringify(payload));
            
            sleep(10000);
            gemeResult();
            $('#loading').hide();

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

// SCORE 랑 통신하여 소유자의 카드갯수를 반환
async function myCard() {
    var call = new CallBuilder()
        .from(address)
        .to(score_to)
        .method('showAllCard')
        .build()

    let myCards = await iconService.call(call).execute(); 
    console.log("showAllCard: "+myCards);

    images(myCards)

    // var call = new CallBuilder()
    //     .from(address)
    //     .to('cx37d5799e548048ba19566e3d018e77a9392b1cc2')
    //     .method('showAllCard')
    //     .params({ 
    //         "_owner":address
    //     })
    //     .build()

    // let balanceOf = await iconService.call(call).execute(); 
    // console.log("balanceOf: "+balanceOf);
    

    // images(balanceOf)
}

// 자신이 소유한 카드들을 보여주는 함수
function images(cards) {
    // Bryant_N / Cury_N / Griffin_N / Harden_N / Hayward_N / Irving_N / Jordan_N / Lebron_N
 
    // player = ['Bryant', 'Cury', 'Griffin', 'Harden', 'Hayward', 'Irving', 'Jordan', 'Lebron' ]

    var cardCount = cards.length; 
    var card_property;
    var grade;
    for(var i=0; i<cardCount; i++) {
        var card = cards[i];
        // console.log(card.replace(/\'/gi, "\""));
        var card_str = card.replace(/\'/gi, "\"");

        // console.log(typeof(card_str));
        card_property = JSON.parse(card_str);
        // console.log(typeof(card_property));
        // console.log(card_property.player);

        if(card_property.run >= 300) {
            grade = 'S';
        } else if ( card_property.run >= 200) {
            grade = "R";
        } else {
            grade = 'N';
        }

        // $('.wrap').append('<img src="../../img/player/'+card_property.player+'_'+grade+'.png">');
        $('.wrap').append('<img src="../../img/player/'+card_property.player+'.png">');
        // console.log(card_property.run);
        // console.log(card_property.power);

    }
    // console.log("card_property="+card_property);
}

// get방식으로 넘어온 address 를 리턴함
function getParameterByAddress(address) {
    var address = address.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + address + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}

function sleep (delay) {
    var start = new Date().getTime();
    while (new Date().getTime() < start + delay);
 }
 
 
