"""
Programmer    : 김승규, 정해민 - pair programming
description   : ISTAR SCORE of ICON
Update Date   : 2018.02.14
Update        : ADD TEST_FUNCTION, function(balanceOf, getApproved, approve, transfer, )
"""


from iconservice import *

TAG = 'IStarIRC3'

class IStarIRC3(IconScoreBase):

    @eventlog(indexed=3)
    def Transfer(self, _from: Address, _to: Address, _tokenId: int):
        pass


    def __init__(self, db: IconScoreDatabase) -> None:
        super().__init__(db)
        # 모든 토큰
        self._total_token = VarDB("TOKENID", db, value_type=int)
        # 토큰[토큰id] 로 토큰 소유자 계정 받음
        self._token_owner = DictDB("TOKEN_OWNER", db, value_type=Address)
        # approve address를 받음
        self._approve_address = DictDB("APPROVED_ADDRESS", db, value_type=Address)

        # token 저장하는 DB
        self._token = DictDB("TOKEN", db, value_type=int)

    def on_install(self) -> None:
        super().on_install()
        # 맨 처음은 토큰을 0 개로 지정

        # test init total_token = 3
        self._total_token.set(3)


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
        totalCount = self.get_total_token()

        for i in range(totalCount):
            if self._token_owner[i] == _owner:
                count = count + 1
        return count

    @external(readonly=True)
    def ownerOf(self, _tokenId: int) -> Address:
        return self._token_owner[_tokenId]

    @external(readonly=True)
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
            raise IconScoreException("approve : 너 이거 못보내(너 이 토큰 없잖아!~~) ")
            # pass

        # _to 이미 토큰을 가지고 있는지 확인
        if _to == self._token_owner[_tokenId] :
            raise IconScoreException("approve : to가 이미 소유 중 (니꺼잖아!! 자신의 토큰을 자신에게 approve할 필요 없습니다.")
             # 에러 처리
            pass

        # token의 소유자를 approve 실행
        self._approve_address[_tokenId] = _to

    @external
    def transfer(self, _to: Address, _tokenId: int):
        # 에러처리 1 - Throws unless self.msg.sender is the current owner.
        # if self.msg.sender != self._token_owner[_tokenId]:
        #     raise IconScoreException("transfer : 소유권 없음")

        ##### Throws if _to is the zero address !!!!!!! 추가 필요, 질문하기
        # 에러처리 2 - Throws if _tokenId is not a valid NFT
        ## 1. total_token을 다 확인해서 있으면 참
        ## 없으면 에러 처리
        # 2.
        # if self._token_owner[_tokenId] == None:
        #     raise IconScoreException("transfer: 토큰이 없어!!")

        # 에러처리 3 - Throws if _tokenId is not a valid NFT
        # if self._token[_tokenId] == 0:
        #     raise IconScoreException("transfer: 토큰이 아닙니다.!!")

        # 에러처리 4 - approve 확인
        if self._approve_address[_tokenId] != _to:
            raise IconScoreException("transfer: approve의 계정이 아닙니다.")

        # 실제적인 transfer 실행
        self._token_owner[_tokenId] = _to
        del self._approve_address[_tokenId]
        self.Transfer(self.msg.sender, _to, _tokenId)

    @external
    def transferFrom(self, _from: Address, _to: Address, _tokenId: int):
        # Throws unless self.msg.sender is the current owner or the approved address for the NFT
        if self.msg.sender != self._token_owner[_tokenId]:
            raise IconScoreException("transferFrom: 소유권 없음")

        if self._approve_address[_tokenId] != _to:
            raise IconScoreException("transferFrom: to는 approve 계정이 아닙니다.")

        # Throws if _from is not the current owner.
        if _from == self._token_owner[_tokenId]:
            raise IconScoreException("transferFrom: from 이 토큰의 소유자가 아닙니다.")

        # Throws if _to is the zero address.
        ### ??? - 물어보기

        # Throws if _tokenId is not a valid NFT.
        # if self._token[_tokenId] == 0:
        #     raise IconScoreException("transfer: 토큰이 아닙니다.!!")

        # 실제적인 트랜스퍼
        self._token_owner[_tokenId] = _to
        del self._approve_address[_tokenId]
        self.Transfer(_from, _to, _tokenId)

    # 테스트 코드로 검증해야함!!!!!!!!!

    # ******************* Customer Function *******************

    @external
    def init_add(self):
        # string -> address type change
        self._token_owner[0] = Address.from_string("hxe7af5fcfd8dfc67530a01a0e403882687528dfcb")
        self._token_owner[1] = Address.from_string("hxe7af5fcfd8dfc67530a01a0e403882687528dfcb")
        self._token_owner[2] = Address.from_string("hx08711b77e894c3509c78efbf9b62a85a4354c8df")

        self._token[0] = 0
        self._token[1] = 1
        self._token[2] = 2

    @external
    def add(self, _tokenId:int):
        self._token_owner[_tokenId] = self.msg.sender
        # !!!!! 보안생각하기 - add를 실행하면 무조건 token을 가질 수 있음

        #
        token_count = self._total_token.get()
        self._total_token.set(token_count+1)

        # return self._token_owner[_token_id]
        # return token_count

        # self._token_owner[token_id] = self.msg.sender

    @external
    def get_total_token(self):
        return self._total_token.get()

















