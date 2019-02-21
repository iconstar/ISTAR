// 실제 파일

// import IconService from 'icon-sdk-js';
// import 'babel-polyfill';
import IconService, { IconAmount, IconConverter, HttpProvider, IconWallet, IconBuilder, SignedTransaction } from 'icon-sdk-js';

// httpProvider = new HttpProvider();
const httpProvider = new HttpProvider('http://127.0.0.1:9000/api/v3');
const iconService = new IconService(httpProvider);

const CallBuilder = IconService.IconBuilder.CallBuilder;

// cx37d5799e548048ba19566e3d018e77a9392b1cc2
// cx6ad3a41000e745a811132501dbc9cc96c67ac6dc


var address = getParameterByName('address');


async function myCard() {
    var call = new CallBuilder()
        .from(address)
        .to('cx37d5799e548048ba19566e3d018e77a9392b1cc2')
        .method('balanceOf')
        .params({ 
            "_owner":address
        })
        .build()

    let balanceOf = await iconService.call(call).execute(); 
    console.log("balanceOf: "+balanceOf);
    return balanceOf;
}

images();
function images() {

    for (var i = 1; i <= 10; i++) {
        // append 메소드를 사용해서 이미지 추가 이름은 bg_01.jpg 같은 숫자 증가 형태
        $('.wrap').append('<img src="../../img/1.jpg">');
    }
    

    // // wrap 클래스안의 모든 이미지가 로딩되면 masonry 적용
    // images = $('.wrap').imagesLoaded(function () {
    //     images.masonry({
    //         itemSelector: 'img', // img 태그를 대상으로 masonry 적용
    //         fitWidth: true,
    //         columnWidth: 10
    //     });
    // });
}

function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}