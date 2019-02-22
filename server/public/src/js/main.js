import IconService, { IconAmount, IconConverter, HttpProvider, IconWallet, IconBuilder, SignedTransaction } from 'icon-sdk-js';

// httpProvider = new HttpProvider();
const httpProvider = new HttpProvider('http://127.0.0.1:9000/api/v3');
const iconService = new IconService(httpProvider);

const CallBuilder = IconService.IconBuilder.CallBuilder;

// 커스텀 변수
var score_to = 'cxdacd3169934b4da8ab0141c5f6c2b74ce320fd67';
var addr_to = 'hxc22ae778606f626c03815a5adc41da4a1dad6b4f';
var address = getParameterByAddress('address');

myCard();
// var cardCount = myCard();
// console.log("cardCount: "+cardCount);
// images(cardCount);

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
        console.log(card.replace(/\'/gi, "\""));
        var card_str = card.replace(/\'/gi, "\"");

        console.log(typeof(card_str));
        card_property = JSON.parse(card_str);
        console.log(typeof(card_property));
        console.log(card_property.player);

        if(card_property.run >= 300) {
            grade = 'S';
        } else if ( card_property.run >= 200) {
            grade = "R";
        } else {
            grade = 'N';
        }

        ㄴ

        $('.front').append('<img src="../../img/player/Curry_N.png">');
        $('.back').append('<img src="../../img/player/Curry_N_back.png">');

        $('.wrap').append('<img src="../../img/player/'+card_property.player+'_'+grade+'.png">');

        $('.front').append('<img src="../../img/player/'+card_property.player+'_'+grade+'.png">');
        $('.back').append('<img src="../../img/player/'+card_property.player+'_'+grade+'_back.png">');

        console.log(card_property.run);
        console.log(card_property.power);

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
