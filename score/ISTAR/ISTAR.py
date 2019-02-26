"""
Programmer    : 김승규, 정해민 - pair programming
description   : ISTAR SCORE of ICON
Update Date   : 2019.02.27
Update        : ISTAR (createCard, startGame, auctionSell, auctionBuy)
"""

# IRC3 = cx557e488ea593c9c71afad8d04a1fec38b3a44d5c
# ISTAR = cx6b8f1ba9aecf43bf3df46bf81e20a4fa048ee975

# tbears deploy -m update -o cx557e488ea593c9c71afad8d04a1fec38b3a44d5c ../IRC3
# tbears deploy -m update -o cx6b8f1ba9aecf43bf3df46bf81e20a4fa048ee975 ../ISTAR

from iconservice import *

TAG = 'ISTAR'

class IRC3Interface(InterfaceScore):
    @interface
    def name(self):
        pass

    @interface
    def symbol(self):
        pass

    @interface
    def balanceOf(self, _owner: Address):
        pass

    @interface
    def ownerOf(self, _tokenId: int):
        pass

    @interface
    def ownerOf(self):
        pass

    @interface
    def getApproved(self, _tokenId: int):
        pass

    @interface
    def approve(self, _to: Address, _tokenId: int):
        pass

    @interface
    def transfer(self, _to: Address, _tokenId: int):
        pass

    @interface
    def transferFrom(self, _from: Address, _to: Address, _tokenId: int):
        pass

    # ****************** CUSTOM ******************

    @interface
    def setToken(self, _tokenId: int, _property: str):
        pass

    @interface
    def setTokenOwner(self, _tokenId: int, address: Address):
        pass

    @interface
    def setTotalToken(self, _totalToken:int):
        pass

    @interface
    def setApproveAddress(self, _to: Address, _tokenId: int):
        pass

    @interface
    def getToken(self, _tokenId: int):
        pass

    @interface
    def getTokenOwner(self, _tokenId: int):
        pass

    @interface
    def getTotalToken(self):
        pass

    @interface
    def getApproveAddress(self, _tokenId: int):
        pass



class ISTAR(IconScoreBase):
    IRC3Address = "cx557e488ea593c9c71afad8d04a1fec38b3a44d5c"

    def __init__(self, db: IconScoreDatabase) -> None:
        super().__init__(db)
        # 게임 결과 저장 변수
        self._game_result = DictDB("GAME_REUSLT", db, value_type=int)
        # 경매 db
        self._auction = DictDB("AUCTION", db, value_type=str)
        # 경매에 올라가 있는 카드 수
        self._total_auction = VarDB("TOTALAUCTION", db, value_type=int)

    def on_install(self) -> None:
        super().on_install()
        self._total_auction.set(0)
        # tokenAddress = "cxcc1775da63f9d844596d769b96b56d71bc8a1ee8"
        # irc3 = self.create_interface_score("", IRC3Interface)

    def on_update(self) -> None:
        super().on_update()

    @external
    @payable
    def createCard(self, _grade: int):
        ####### 토큰 추가 #######
        irc3 = self.create_interface_score(Address.from_string(self.IRC3Address), IRC3Interface)

        total_token = irc3.getTotalToken()
        # Logger.warning(f'totkal_tokne {total_token}', TAG)
        tokenId = total_token  # 3

        Logger.warning(f"totalToken: {total_token}")

        player = ['Bryant', 'Curry', 'Griffin', 'Harden', 'Hayward', 'Irving', 'Jordan', 'Lebron']

        # 속성 변수
        json_property = {}

        ### 속성 정의
        json_property['tokenId'] = tokenId
        json_property['player'] = player[int.from_bytes(sha3_256(
            self.msg.sender.to_bytes() + str(self.block.timestamp).encode() + "run".encode()), 'big') % 8]
        json_property['run'] = int.from_bytes(sha3_256(
            self.msg.sender.to_bytes() + str(self.block.timestamp).encode() + "run".encode()), 'big') % 100
        json_property['power'] = int.from_bytes(sha3_256(
            self.msg.sender.to_bytes() + str(self.block.timestamp).encode() + "power".encode()), 'big') % 100
        json_property['dribble'] = int.from_bytes(sha3_256(
            self.msg.sender.to_bytes() + str(self.block.timestamp).encode() + "dribble".encode()), 'big') % 100

        # 에러 처리
        if _grade == 1:
            # normal grade
            json_property['run'] += 100
            json_property['power'] += 100
            json_property['dribble'] += 100
        elif _grade == 2:
            json_property['run'] += 200
            json_property['power'] += 200
            json_property['dribble'] += 200

        elif _grade == 3:
            json_property['run'] += 300
            json_property['power'] += 300
            json_property['dribble'] += 300
            # rare grade
        else:
            raise IconScoreException("createCard: ", "뒤질래? 누가 해킹하래? 누가 데이터 변조하래 / 이거 블록체인이야!!")

        ## 토큰에다 속성을 정의
        irc3.setToken(tokenId, str(json_property))
        # self._token[tokenId] = str(json_property)

        # 만든 토큰에 소유자를 정의
        # self._token_owner[tokenId] = self.msg.sender
        irc3.setTokenOwner(tokenId, self.msg.sender)

        # 발행된 토큰 수 증가 (+1) - 카드 하나 생성
        total_token += 1
        irc3.setTotalToken(total_token)
        # self._total_token.set(total_token)

    # 소유자의 모든 토큰 보여주기
    @external
    def getMyCard(self):
        irc3 = self.create_interface_score(Address.from_string(self.IRC3Address), IRC3Interface)

        totalToken = irc3.getTotalToken()
        jsonCardList = []

        for i in range(totalToken):
            if irc3.getTokenOwner(i) == self.msg.sender:
                jsonCardList.append(irc3.getToken(i))
                # jsonCardList.append(self._token[i])
        return jsonCardList

    # 게임실행, 카드 등급에 따라 승률 조작
    # &**************** 에러 처리 코드 넣기!!
    @external
    @payable
    def startGame(self, _time: str):
        ##### 주의 !!! 스코어에 돈없으면 그냥 졌다고 나옴!!! 돈 뺐지도 않음 그냥 돈 안빠져나감
        # 에러 처리하기!!

        # 게임결과 키 값 생성
        hash_time = sha3_256(str(_time).encode()+str(self.msg.sender).encode())

        # 게임확률 조작
        game_property = int.from_bytes(sha3_256(
            self.msg.sender.to_bytes() + str(self.block.timestamp).encode() + "run".encode()), 'big') % 100

        # 카드 정보 가져 옴
        cardList = self.getMyCard()
        cardCount = len(cardList)

        # cardList = self.showAllCard()
        # cardCount = len(cardList)

        # 자신이 소유한 카드 속성 중 제일 큰 값 가져오기
        max = 0
        # 카드 속성 정보 가져옴
        for i in range(cardCount):
            cards = eval(cardList[i])
            # print("cards: ", cards)
            # print("player: ", cards['player'])
            property_sum = (cards['run'] + cards['power'] + cards['dribble']) / 3
            # print("property_sum: ", property_sum)

            if max <= (property_sum):
                max = property_sum

        # 이길 확률 조정
        win_probability = 0

        # 값(능력치)에 따라 이길 확률 조정!
        if max >= 100 and max < 200:
            win_probability += 30
            print(f"100 ~ 200: {win_probability}")
        elif max >= 200 and max < 300:
            win_probability += 30 + (max / 10)
            print(f"200 ~ 300: {win_probability}")
        elif max >= 300 and max <= 400:
            win_probability += 30 + (max / 10) + ((max / 10) / 5)
            print(f"300 ~ 400: {win_probability}")
        else:
            raise IconScoreException("max 값 오류 입니다.")

        # 게임 시작
        if win_probability >= game_property:
            # 이김
            self.icx.transfer(self.msg.sender, self.msg.value * 2)
            self._game_result[hash_time] = 1
            Logger.warning(f"win {self._game_result[hash_time]}", TAG)
        else:
            self._game_result[hash_time] = 0
            Logger.warning(f"lose {self._game_result[hash_time]}", TAG)

    # 게임 결과 가져오는 코드
    @external(readonly=True)
    def getGameResult(self, _time: str) -> int:
        # 게임결과 키 값 생성
        hash_time = sha3_256(str(_time).encode() + str(self.msg.sender).encode())

        Logger.warning(f"결과: {self._game_result[hash_time]}", TAG)
        return self._game_result[hash_time]

    @external
    @payable
    def auctionSell(self, _playerId: int, _price: int):
        # auction 저장되어 있는 토큰이 같은 키면 에러 처리
        myCardList = self.getMyCard()

        Logger.warning(f"auctionSell myCardList: {myCardList}", TAG)

        sellCard = eval(myCardList[_playerId - 1])

        Logger.warning(f"auctionSell sellCard: {sellCard}", TAG)

        tokenId = sellCard["tokenId"]
        Logger.warning(f"auctionSell tokenId: {tokenId}", TAG)
        Logger.warning(f"auctionSell self.msg.sender: {self.msg.sender}", TAG)
        Logger.warning(f"auctionSell self.address: {self.address}", TAG)

        json_sell = {}
        json_sell['address'] = str(self.msg.sender)
        # Logger.warning(f"json_sell['address']: {json_sell['address']}", TAG)
        json_sell['property'] = sellCard
        # Logger.warning(f"json_sell['property']: {json_sell['property']}", TAG)
        json_sell['price'] = _price
        # Logger.warning(f"json_sell['_price']: {json_sell['price']}", TAG)

        Logger.warning(f"auctionSell SELL SUCCESS: {str(json_sell)}", TAG)

        totalAuction = self._total_auction.get()
        Logger.warning(f"auctionSell totalAuction: {totalAuction}", TAG)
        self._auction[totalAuction] = str(json_sell)
        Logger.warning(f"auctionSell self._auction[totalAuction]: {self._auction[totalAuction]}", TAG)
        # self._auction.put(str(json_sell))

        # 경매에 올라가져 있어 경매 카드 수 하나 증가
        totalAuction +=1
        self._total_auction.set(totalAuction)
        Logger.warning(f"self._total_auction.get: {self._total_auction.get()}", TAG)

        # approve
        self._approve(self.address, tokenId)
        # self.approve(self.address, tokenId)

    # 경매에 올라온 카드들을 가져옴
    @external
    def getAuctionToken(self):
        totalToken = self._total_auction.get()
        Logger.warning(f" getAuctionToken totalToken: {totalToken}", TAG)
        jsonAuctionList = []

        for i in range(totalToken):
            jsonAuctionList.append(self._auction[i])

        Logger.warning(f" getAuctionToken jsonAuctionList: {jsonAuctionList}", TAG)
        return jsonAuctionList

    @external
    @payable
    def auctionBuy(self, _playerId: int, _price: int):
        irc3 = self.create_interface_score(Address.from_string(self.IRC3Address), IRC3Interface)

        # 경매의 카드들 가져옴
        auctionCardList = self.getAuctionToken()
        Logger.warning(f"auctionBuy auctionCardList: { auctionCardList }", TAG)
        # 구매자가 선택한 카드 정보 가져옴
        cardProperty = eval(auctionCardList[_playerId-1])
        Logger.warning(f"auctionBuy cardProperty: { cardProperty }", TAG)

        # 카드의 소유자 선택
        tokenOwner = Address.from_string(cardProperty["address"])
        Logger.warning(f"auctionBuy tokenOwner: {tokenOwner}", TAG)
        property = cardProperty["property"]
        Logger.warning(f"auctionBuy property: {property}", TAG)

        # 해당 카드의 토큰ID 가져옴
        tokenId = property["tokenId"]
        Logger.warning(f"auctionBuy tokenId: {tokenId}", TAG)

        # approve 함
        self._buyApprove(self.msg.sender, _playerId)
        # Logger.warning("2", TAG)
        # trasnferFrom
        # irc3.transferFrom(tokenOwner, self.msg.sender, tokenId)
        # Logger.warning("3", TAG)

        # 경매장에 있는 정보 삭제
        # self._auction.pop(_playerId-1)
        Logger.warning(f"AC1 {self._auction[_playerId - 1]}")
        del self._auction[_playerId-1]
        Logger.warning(f"AC2 {self._auction[_playerId - 1]}")

        Logger.warning("4", TAG)
        # 1. approve???
        # 2. tranferForm 전달하고
        # 3. owner에게 돈을 전달

        # 경매에 올라가져 있어 경매 카드 수 하나 증가
        totalAuction = self._total_auction.get()
        totalAuction -= 1
        self._total_auction.set(totalAuction)
        Logger.warning(f"self._total_auction: {self._total_auction.get()}", TAG)

        Logger.warning(f"{self.address}", TAG)


        self.icx.transfer(tokenOwner, _price)
        Logger.warning("5", TAG)

    # ---------------------------------------- 필요한 함수

    def _buyApprove(self, _to:Address, _playerId:int):
        irc3 = self.create_interface_score(Address.from_string(self.IRC3Address), IRC3Interface)

        # 경매의 카드들 가져옴
        auctionCardList = self.getAuctionToken()
        # Logger.warning(f"auctionBuy auctionCardList: {auctionCardList}", TAG)
        # 구매자가 선택한 카드 정보 가져옴
        cardProperty = eval(auctionCardList[_playerId - 1])
        # Logger.warning(f"auctionBuy cardProperty: {cardProperty}", TAG)

        # 카드의 소유자 선택
        tokenOwner = Address.from_string(cardProperty["address"])
        Logger.warning(f"auctionBuy tokenOwner: {tokenOwner}", TAG)
        property = cardProperty["property"]
        Logger.warning(f"auctionBuy property: {property}", TAG)
        price = cardProperty["price"]
        Logger.warning(f"price: {price}", TAG)

        # 해당 카드의 토큰ID 가져옴

        tokenId = property["tokenId"]
        # Logger.warning(f"auctionBuy tokenId: {tokenId}", TAG)

        if self.address != self.getApproved(tokenId):
            raise IconScoreException("Approve4 가 일치하지 않습니다.!!")

        Logger.warning("_buyApprove: ㅠㅠ")

        irc3.transferFrom(tokenOwner, self.msg.sender, tokenId)
        Logger.warning("_buyApprove: 2")
        self.icx.transfer(tokenOwner, price)

    def _approve(self, _to: Address, _tokenId: int):
        irc3 = self.create_interface_score(Address.from_string(self.IRC3Address), IRC3Interface)
        # 호출한 사람이 토큰을 가지고 잇는지 확인
        if self.msg.sender != irc3.getTokenOwner(_tokenId):
            # 에러 처리
            raise IconScoreException("approve 1")
            # raise IconScoreException("approve 1: YOU CAN;'너 이거 못보내(너 이 토큰 없잖아!~~) ")

        # 내가 나한테 approve를 못함
        if self.msg.sender == _to:
            raise IconScoreException("approve 2")
            # raise IconScoreException("approve 2: 너가 너한테 이거 못보내지롱~~ (너 이 토큰 없잖아!~~) ")
            # pass

        # _to 이미 토큰을 가지고 있는지 확인
        if _to == irc3.getTokenOwner(_tokenId):
            raise IconScoreException("approve 3")
            # raise IconScoreException("approve 3: to가 이미 소유 중 (니꺼잖아!! 자신의 토큰을 자신에게 approve할 필요 없습니다.")
            # 에러 처리

        # token의 소유자를 approve 실행
        irc3.setApproveAddress(_to, _tokenId)

    # 데이터 확인 코드
    @external
    def getName(self):
        irc3 = self.create_interface_score(Address.from_string(self.IRC3Address), IRC3Interface)
        return irc3.name()

    @external
    def getSymbol(self):
        irc3 = self.create_interface_score(Address.from_string(self.IRC3Address), IRC3Interface)
        return irc3.symbol()

    @external
    def getTotalToken(self):
        irc3 = self.create_interface_score(Address.from_string(self.IRC3Address), IRC3Interface)
        return irc3.getTotalToken()

    # getToken 으로 바꾸기
    @external
    def getToken(self, _tokenId:int):
        irc3 = self.create_interface_score(Address.from_string(self.IRC3Address), IRC3Interface)
        return irc3.getToken(_tokenId)

    @external
    def getTokenOwner(self, _tokenId:int):
        irc3 = self.create_interface_score(Address.from_string(self.IRC3Address), IRC3Interface)
        return irc3.getTokenOwner(_tokenId)

    # ----------------------------------------
    @external
    def getApproved(self, _tokenId:int):
        irc3 = self.create_interface_score(Address.from_string(self.IRC3Address), IRC3Interface)
        return irc3.getApproved(_tokenId)