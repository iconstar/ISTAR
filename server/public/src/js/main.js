import IconService, { IconAmount, IconConverter, HttpProvider, IconWallet, IconBuilder, SignedTransaction } from 'icon-sdk-js';
// import cheerio from 'cheerio';
const cheerio = require('cheerio');


// console.log("cheerio: "+cheerio);
// httpProvider = new HttpProvider();
const httpProvider = new HttpProvider('http://127.0.0.1:9000/api/v3');
const iconService = new IconService(httpProvider);
const CallBuilder = IconService.IconBuilder.CallBuilder;

// service 
// const IcxTransactionBuilder = IconService.IconBuilder.IcxTransactionBuilder;
// const signedTransaction = IconService.SignedTransaction;
// const iconWallet = IconService.IconWallet;

// 커스텀 변수
var score_to = 'cx6b8f1ba9aecf43bf3df46bf81e20a4fa048ee975';
var address = getParameterByAddress('address');


// 이벤트 핸들러
window.addEventListener("ICONEX_RELAY_RESPONSE", eventHandler, false);


let current = '';
var full_html = "";
var clickGame = false;
var clickSell = false;

// 로딩바 바로 사라지게하기 위해
$('#loading').hide();  


// 소유자의 카드 보여줌
myCard();
// getApprove();
// getApprove();

// 게임 시작 버튼 클릭시
document.getElementById('gameStart').addEventListener('click', async () => {
    clickGame = true;

    $('#modal').hide();
    var date = new Date();
    // currentTime = date.getTime();
    current = String(date.getTime());
    
    // console.log("date.getTime(): "+date.getTime());
    console.log("gameStart()1, current: "+current)
    console.log("gameStart()1, current: "+typeof(current))

    // await this.readFile();
    var price = parseInt(document.getElementById('betting_price').value);

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

document.getElementById('sellCard').addEventListener('click', async () => {
    $('#modal').hide();
    clickSell = true;

    var player_id = document.getElementById('player_id').value;         // 2
    var player_price = document.getElementById('player_price').value;   // 1

    console.log("player_id: "+ player_id);
    console.log("player_price: "+ player_price);
    console.log("player_price: "+ typeof(player_price));

    var callTransactionBuilder = new IconBuilder.CallTransactionBuilder;
    var callTransactionData = callTransactionBuilder
        .from(address)
        .to(score_to)
        .nid(IconConverter.toBigNumber(3))
        .timestamp((new Date()).getTime() * 1000)
        .stepLimit(IconConverter.toBigNumber(10000000))
        .version(IconConverter.toBigNumber(3))
        .method('auctionSell')
        .params({  
            "_playerId":player_id, // 2
            "_price":player_price  // 1 
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
});

// 이벤트 핸들러 - ICONex
function eventHandler(event) {
    var type = event.detail.type;
    var payload = event.detail.payload;

    switch (type) {
        case "RESPONSE_JSON-RPC":
            console.log("RESPONSE_JSON-RPC: "+JSON.stringify(payload));
            if(clickGame===true) {
                sleep(10000);
                gemeResult();
                $('#loading').hide();
                clickGame = false;
            } else if (clickSell === true) {
                console.log("클릭!! 카드 판매");
                // getApprove();
                clickSell = false;
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


async function getApprove() {
    var tokenId = String(10);
    var call = new CallBuilder()
        .from(address)
        .to(score_to)
        .method('getApproved')
        .params({
            "_tokenId":tokenId
        })
        .build()

    var approve = await iconService.call(call).execute(); 
    console.log("10 의 approve: "+approve);
}


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

// SCORE 랑 통신하여 소유자의 카드갯수를 반환
async function myCard() {
    // console.log("exe myCard()");
    var call = new CallBuilder()
        .from(address)
        .to(score_to)
        .method('getMyCard')
        .build()

    let myCards = await iconService.call(call).execute();
    console.log("getMyCard: "+myCards);

    images(myCards)
}

// 자신이 소유한 카드들을 보여주는 함수
async function images(cards) {
    // Bryant_N / Cury_N / Griffin_N / Harden_N / Hayward_N / Irving_N / Jordan_N / Lebron_N
    // player = ['Bryant', 'Cury', 'Griffin', 'Harden', 'Hayward', 'Irving', 'Jordan', 'Lebron' ]

    var cardCount = cards.length;
    var card_property;
    var grade;

    // for(var i=0; i<cardCount; i++) {
    //     $('#basic').html(html);
    // }

    for(var i=0; i<cardCount; i++) {
        var card = cards[i];
        var card_str = card.replace(/\'/gi, "\"");

        card_property = JSON.parse(card_str);
        // console.log(typeof(card_property));
        // console.log(card_property.player);
        // console.log(card_property.dribble);
        // console.log(card_property.power);
        // console.log(card_property.run);
        console.log("tokenID: "+card_property.tokenId);

        if(card_property.run >= 300) {
            grade = 'S';
        } else if ( card_property.run >= 200) {
            grade = "R";
        } else {
            grade = 'N';
        }
        

        var html = "";

        html += '<div class="card card-personal col-xs-3" style="margin-top:40px; height:350px; margin-left:90px;">';
        html += '<div class="card-body">';

        html += '<div class="flip-container" style="margin-bottom:30px; height:100px;">'; 
        html += '<div class="flipper">';
        html += '<div id="front" class="front"> '
            html += '<img src="../../img/player/'+card_property.player+'_'+grade+'.png" style="weight:400px; height:280px;">'
            html += '</div>';  
        html += '<div id="back'+i+'" class="back">'; 
        html += '<span id="cardinfo" class="tableNo" style="margin-left: 45px; margin-top:100px; color: #0b0b0b;">';
        html += '<h6> run:'+card_property.run+' <br>'+'dribble:'+card_property.dribble+' <br>'+'power:'+card_property.power+' <br><br><br>'+card_property.player+'</h6></span>'
        html += '<img src="../../img/player/'+card_property.player+'_'+grade+'_back.png" style="weight:400px; height:280px;">'
        html += '<button type="button" class="btn btn-primary" data-toggle="modal" data-target="#sellModal" style="margin-bottom:100px">sell card </button>';
        html += '</div>';
        html += '</div>';
        html += '</div>';
        html += '</div>';
        html += '</div>';
        html += '</div>';
        
        $('#basic').append(html);

        full_html += html;

        
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

// 아이콘 블록체인에 맞게 설정
function sleep (delay) {
    var start = new Date().getTime();
    while (new Date().getTime() < start + delay);
 }
 
 
// 
// function playerSell(player_id) {
//     //  컴퓨터는 0부터  
//     player_id -= 1;
// //    var playerInfo = "";
// //
// //    var $ = cheerio.load(full_html);
// //
// //    var class_a = $('h6', 'span', $('#back'+player_id));
// //
// //    class_a.each(function () {
// //        playerInfo = $(this).text();
// //        // console.log("선수들 정보: "+$(this).text());
// //    });
// //
// //    // console.log("playerInfo: "+playerInfo);
// //    var splitInfo = playerInfo.split(" ");

//     // console.log("splitInfo: "+splitInfo);
//     // console.log("splitInfo: "+typeof(splitInfo));

//     // for(var i=0; i<splitInfo.length; i++) {
//     //     console.log(" "+splitInfo[i]);
//     // }

//     // console.log(splitInfo[1].split(":"));
//     // console.log(splitInfo[2].split(":"));
//     // console.log(splitInfo[3].split(":"));
//     // console.log(splitInfo[4].split(":"));


//     var run = splitInfo[1].split(":")[1];
//     var dribble = splitInfo[2].split(":")[1];
//     var power = splitInfo[3].split(":")[1];
//     var name = splitInfo[4];

//     console.log("run: "+run);
//     console.log("dribble: "+dribble);
//     console.log("power: "+power);
//     console.log("name: "+name);
   

// }