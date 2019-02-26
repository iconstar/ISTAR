"""
Programmer    : 김승규, 정해민 - pair programming
description   : IRC3 - NFT IMPLEMENTATION
Update Date   : 2019.02.27
Update        : IRC3 (name, symbol, balanceOf, ownerOf, getApproved, approve, transfer, transferFrom)
"""

from iconservice import *

TAG = 'IRC3'

class IRC3(IconScoreBase):
    @eventlog(indexed=3)
    def Transfer(self, _from: Address, _to: Address, _tokenId: int):
        pass

    @eventlog(indexed=3)
    def Approval(self, _owner: Address, _approved: Address, _tokenId: int):
        pass

    def __init__(self, db: IconScoreDatabase) -> None:
        super().__init__(db)
        # 모든 토큰
        self._total_token = VarDB("TOTALTOKEN", db, value_type=int)
        # 토큰[토큰id] 로 토큰 소유자 계정 받음
        self._token_owner = DictDB("TOKEN_OWNER", db, value_type=Address)
        # approve address를 받음
        self._approve_address = DictDB("APPROVED_ADDRESS", db, value_type=Address)
        ## token 저장하는 DB - 이거는 에러 처리를 위해 생성! 과연 이게 필요한가?
        self._token = DictDB("TOKEN", db, value_type=str)

    def on_install(self) -> None:
        super().on_install()
        self._total_token.set(0)
        # self._total_token.set(3)

    def on_update(self) -> None:
        super().on_update()

    # ******************* NFT *******************
    @external(readonly=True)
    def name(self) -> str:
        return "ISTAR"

    @external(readonly=True)
    def symbol(self) -> str:
        return "ISX"

    @external(readonly=True)
    def balanceOf(self, _owner: Address) -> int:
        count = 0

        totalCount = self._total_token.get()

        for i in range(totalCount):
            if self._token_owner[i] == _owner:
                count = count + 1
        return count

    @external(readonly=True)
    def ownerOf(self, _tokenId: int) -> Address:
        return self._token_owner[_tokenId]

    @external
    def getApproved(self, _tokenId: int) -> Address:
        return self._approve_address[_tokenId]

    @external
    def approve(self, _to: Address, _tokenId: int):
        # my address -> _to address -> tokenid
        # approve_address = _to

        # 호출한 사람이 토큰을 가지고 잇는지 확인
        if self.msg.sender != self._token_owner[_tokenId]:
            # 에러 처리
            raise IconScoreException("approve : 너 이거 못보내(너 이 토큰 없잖아!~~) ")

        # 내가 나한테 approve를 못함
        if self.msg.sender == _to:
            raise IconScoreException("approve : 너가 너한테 이거 못보내지롱~~ (너 이 토큰 없잖아!~~) ")
            # pass

        # _to 이미 토큰을 가지고 있는지 확인
        if _to == self._token_owner[_tokenId] :
            raise IconScoreException("approve : to가 이미 소유 중 (니꺼잖아!! 자신의 토큰을 자신에게 approve할 필요 없습니다.")
             # 에러 처리
        Logger.warning(f"self._approve_address[_tokenId]: {self._approve_address[_tokenId]}")
        # token의 소유자를 approve 실행
        self._approve_address[_tokenId] = _to
        Logger.warning(f"self._approve_address[_tokenId]: {self._approve_address[_tokenId]}")

    @external
    def transfer(self, _to: Address, _tokenId: int):
        # 에러처리 1 - Throws unless self.msg.sender is the current owner.
        if self.msg.sender != self._token_owner[_tokenId]:
            raise IconScoreException("transfer: self.msg.sender 소유권 없음")

        ##### Throws if _to is the zero address !!!!!!! 추가 필요, 질문하기
        # 에러처리 2 - Throws if _tokenId is not a valid NFT
        if _to == "cx"+str(0)*40 or _to == "hx"+str(0)*40:
            raise IconScoreException("transfer: ", "_to는 ZERO ADDRESS 가 될 수 없습니다.")

        # 에러처리 3 - Throws if _tokenId is not a valid NFT
        total_token = self._total_token.get()  # 2
        if _tokenId > total_token:
            raise IconScoreException("transfer: ", "올바른 토큰이 아닙니다.")

        # 에러처리 4 - approve 확인
        if self._approve_address[_tokenId] != _to:
            raise IconScoreException("transfer: approve의 계정이 아닙니다.")

        # 실제적인 transfer 실행
        self._token_owner[_tokenId] = _to
        del self._approve_address[_tokenId]
        self.Transfer(self.msg.sender, _to, _tokenId)

    @external
    def transferFrom(self, _from: Address, _to: Address, _tokenId: int):
        ## 오류 1 - Throws unless self.msg.sender is the current owner or the approved address for the NFT
        # -> self.msg.sender가 소유자거나 approve를 받은 계정이면 안됨


        Logger.warning(f"self.msg.sender: {self.msg.sender}", TAG)
        Logger.warning(f"self._token_owner[_tokenId]: {self._token_owner[_tokenId]}",TAG)
        Logger.warning(f"_from: {_from}", TAG)
        # Logger.warning(f"self.getApproved[_tokenId]: {self.getApproved[_tokenId]}")

        # if self.msg.sender == self._token_owner[_tokenId] or self.msg.sender == self.getApproved[_tokenId]:
        if self.msg.sender == self._token_owner[_tokenId] or self.msg.sender != self._approve_address[_tokenId]:
            raise IconScoreException("transferFrom: ", "self.msg.sender가 소유자거나 approve를 받은 계정이면 안됩니다.")

        Logger.warning(f"_from: {type(_from)}", TAG)
        Logger.warning(f"self._token_owner[_tokenId]: {type(self._token_owner[_tokenId])}", TAG)
        ## 오류 2 -  Throws if _from is not the current owner.
        if _from != self._token_owner[_tokenId]:
            raise IconScoreException("transferFrom: _from 이 토큰의 소유자가 아닙니다.")

        ## 오류 3 - Throws if _to is the zero address.
        if _to == "cx"+str(0)*40 or _to == "hx"+str(0)*40:
            raise IconScoreException("transferFrom: ", "_to는 ZERO ADDRESS 가 될 수 없습니다.")

        ## 오류 4 -  Throws if _tokenId is not a valid NFT.
        total_token = self._total_token.get()  # 2
        if _tokenId > total_token:
            raise IconScoreException("transferFrom: ", "올바른 토큰이 아닙니다.")

        # 실제적인 트랜스퍼
        self._token_owner[_tokenId] = _to
        del self._approve_address[_tokenId]
        self.Transfer(_from, _to, _tokenId)

    # ******************* CUSTOM *******************

    @external
    def setToken(self, _tokenId:int, _property:str):
        self._token[_tokenId] = _property

    @external
    def setTokenOwner(self, _tokenId:int, address:Address):
        self._token_owner[_tokenId] = address

    @external
    def setTotalToken(self, _totalToken: int):
        self._total_token.set(_totalToken)

    @external
    def setApproveAddress(self, _to:Address, _tokenId:int):
        Logger.warning(f"1 self._approve_address[_tokenId]: {self._approve_address[_tokenId]}",TAG)
        self._approve_address[_tokenId] = _to
        Logger.warning(f"2 self._approve_address[_tokenId]: {self._approve_address[_tokenId]}", TAG)


    @external
    def getTotalToken(self):
        return self._total_token.get()

    @external
    def getToken(self, _tokenId:int):
        return self._token[_tokenId]

    @external
    def getTokenOwner(self, _tokenId: int):
        return self._token_owner[_tokenId]

    @external
    def getApproveAddress(self, _tokenId: int):
        return self._approve_address[_tokenId]