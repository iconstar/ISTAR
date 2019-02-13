from iconservice import *

TAG = 'IStarIRC3'

class IStarIRC3(IconScoreBase):

    def __init__(self, db: IconScoreDatabase) -> None:
        super().__init__(db)
        # 모든 토큰
        self._total_token = VarDB("TOKENID", db, value_type=int)
        # 토큰[토큰id] 로 토큰 소유자 계정 받음
        self._token_owner = DictDB("TOKEN_OWNER", db, value_type=Address)



    def on_install(self) -> None:
        super().on_install()
        # 맨 처음은 토큰을 0 개로 지정
        self._total_token.set(0)

    def on_update(self) -> None:
        super().on_update()

    @external(readonly=True)
    def name(self) -> str:
        return "ISTAR"

    @external(readonly=True)
    def symbol(self) -> str:
        return "ISX"

    @external(readonly=True)
    def balanceOf(self, _owner: Address) -> int:
        count = 0
        index = 0
        totalCount = self.get_total_token()

        for i in range(totalCount):
            if self._token_owner[i] == _owner:
                count = count + 1

        # while index <= totalCount:
        #     if self._token_owner[index] == _owner:
        #         count = count + 1
        #     index = index + 1

        return count

        # 소유자의 주소를 받고 토큰을 몇개 갖고 있는지 확인해야함
        # total_token = self.get_total_token()
        # balance_count = 0
        #
        # for i in range(total_token):
        #     if self._token_owner[_token_id] == _owner:
        #         balance_count += 1
        #
        # return balance_count


    # ******************* Customer Function *******************
    @external
    def add(self, _token_id:int):
        self._token_owner[_token_id] = self.msg.sender
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

    @external
    def get_token_owner(self, _token_id: int):
        return self._token_owner[_token_id]
















