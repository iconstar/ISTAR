images();

function images() {
    // return "제발유";
    for (var i = 1; i <= 4; i++) {
        // append 메소드를 사용해서 이미지 추가 이름은 bg_01.jpg 같은 숫자 증가 형태
        /* $('.wrap').append('<img src="https://biketago.com/img/bg_thumb/bg_' + zeroFill(i, 2) + '.jpg">');--> */
        $('.wrap').append('<img src="../../img/card1.png">');
    }

    // wrap 클래스안의 모든 이미지가 로딩되면 masonry 적용
    $imgs = $('.wrap').imagesLoaded(function () {
        $imgs.masonry({
            itemSelector: 'img', // img 태그를 대상으로 masonry 적용
            fitWidth: true,
            columnWidth: 10

        });
    });

}