import os

from iconsdk.builder.transaction_builder import DeployTransactionBuilder, CallTransactionBuilder
from iconsdk.builder.call_builder import CallBuilder
from iconsdk.icon_service import IconService
from iconsdk.libs.in_memory_zip import gen_deploy_data_content
from iconsdk.providers.http_provider import HTTPProvider
from iconsdk.signed_transaction import SignedTransaction

from tbears.libs.icon_integrate_test import IconIntegrateTestBase, SCORE_INSTALL_ADDRESS

DIR_PATH = os.path.abspath(os.path.dirname(__file__))


class TestIStarIRC3(IconIntegrateTestBase):
    TEST_HTTP_ENDPOINT_URI_V3 = "http://127.0.0.1:9000/api/v3"
    SCORE_PROJECT= os.path.abspath(os.path.join(DIR_PATH, '..'))

    def setUp(self):
        super().setUp()

        self.icon_service = None
        # if you want to send request to network, uncomment next line and set self.TEST_HTTP_ENDPOINT_URI_V3
        # self.icon_service = IconService(HTTPProvider(self.TEST_HTTP_ENDPOINT_URI_V3))

        # install SCORE
        self._score_address = self._deploy_score()['scoreAddress']

    def _deploy_score(self, to: str = SCORE_INSTALL_ADDRESS) -> dict:
        # Generates an instance of transaction for deploying SCORE.
        transaction = DeployTransactionBuilder() \
            .from_(self._test1.get_address()) \
            .to(to) \
            .step_limit(100_000_000_000) \
            .nid(3) \
            .nonce(100) \
            .content_type("application/zip") \
            .content(gen_deploy_data_content(self.SCORE_PROJECT)) \
            .build()

        # Returns the signed transaction object having a signature
        signed_transaction = SignedTransaction(transaction, self._test1)

        # process the transaction in local
        tx_result = self.process_transaction(signed_transaction, self.icon_service)

        self.assertTrue('status' in tx_result)
        self.assertEqual(1, tx_result['status'])
        self.assertTrue('scoreAddress' in tx_result)

        return tx_result

    def test_score_update(self):
        # update SCORE
        tx_result = self._deploy_score(self._score_address)

        self.assertEqual(self._score_address, tx_result['scoreAddress'])

    def test_name(self):
        call_name = CallBuilder()\
            .from_(self._test1.get_address())\
            .to(self._score_address)\
            .method("name")\
            .build()

        response = self.process_call(call_name, self.icon_service)
        print("call_name: ", response)

    def test_symbol(self):
        call_symbol = CallBuilder() \
            .from_(self._test1.get_address()) \
            .to(self._score_address) \
            .method("symbol") \
            .build()

        response = self.process_call(call_symbol, self.icon_service)
        print("call_symbol: ", response)
        # self.assertEqual("Hello", response)

    def test_balanceOf(self):

        param = {
            "_owner":self._test1.get_address()
        }

        # print("param: ", param)
        call_balanceOf = CallBuilder() \
            .from_(self._test1.get_address()) \
            .to(self._score_address) \
            .method("balanceOf") \
            .params(param) \
            .build()

        response = self.process_call(call_balanceOf, self.icon_service)
        print("call_balanceOf: ", response)

    def test_add(self):

        params = {
            "_token_id": 0
        }
        ################### add / _test1 ###################
        transaction = CallTransactionBuilder() \
                    .from_(self._test1.get_address()) \
                    .to(self._score_address) \
                    .step_limit(10_000_000) \
                    .nid(3) \
                    .nonce(100) \
                    .method("add") \
                    .params(params)\
                    .build()

        # Returns the signed transaction object having a signature
        signed_transaction = SignedTransaction(transaction, self._test1)
        # print("signed_transaction: ", signed_transaction)
        self.process_transaction(signed_transaction, self.icon_service)

        ################### add / _test1 ###################
        params = {
            "_token_id": 1
        }

        transaction = CallTransactionBuilder() \
            .from_(self._test1.get_address()) \
            .to(self._score_address) \
            .step_limit(10_000_000) \
            .nid(3) \
            .nonce(100) \
            .method("add") \
            .params(params) \
            .build()

        # Returns the signed transaction object having a signature
        signed_transaction = SignedTransaction(transaction, self._test1)
        # print("signed_transaction: ", signed_transaction)
        self.process_transaction(signed_transaction, self.icon_service)
        # 1를 2개 추가

        ################### add / hx08711b77e894c3509c78efbf9b62a85a4354c8df ###################
        params = {
            "_token_id": 2
        }

        transaction = CallTransactionBuilder() \
            .from_("hx08711b77e894c3509c78efbf9b62a85a4354c8df") \
            .to(self._score_address) \
            .step_limit(10_000_000) \
            .nid(3) \
            .nonce(100) \
            .method("add") \
            .params(params) \
            .build()
        signed_transaction = SignedTransaction(transaction, self._test1)
        # print("signed_transaction: ", signed_transaction)
        self.process_transaction(signed_transaction, self.icon_service)
        # hx08711b77e894c3509c78efbf9b62a85a4354c8df  하나 추가



        ################### 토큰 총 갯수 확인 ###################
        # call_get_total_token = CallBuilder() \
        #     .from_(self._test1.get_address()) \
        #     .to(self._score_address) \
        #     .method("get_total_token") \
        #     .build()
        #
        # response = self.process_call(call_get_total_token, self.icon_service)
        # print("call_get_total_token: ", response)


        ################### get_token_owner ###################
        # params = {
        #     "_token_id": 1
        # }
        #
        # call_get_token_owner = CallBuilder() \
        #     .from_(self._test1.get_address()) \
        #     .to(self._score_address) \
        #     .method("get_token_owner") \
        #     .params(params)\
        #     .build()
        #
        # response = self.process_call(call_get_token_owner, self.icon_service)
        # print("1: ", response)
        #
        # params = {
        #     "_token_id": 2
        # }
        #
        # call_get_token_owner = CallBuilder() \
        #     .from_(self._test1.get_address()) \
        #     .to(self._score_address) \
        #     .method("get_token_owner") \
        #     .params(params) \
        #     .build()
        #
        # response = self.process_call(call_get_token_owner, self.icon_service)
        # print("2: ", response)


        ################### _test1 / balanceOf ###################
        params = {
            "_owner" : "hx08711b77e894c3509c78efbf9b62a85a4354c8df",
            # "_owner" : self._test1.get_address(),
        }

        call_balanceOf = CallBuilder() \
            .from_(self._test1.get_address()) \
            .to(self._score_address) \
            .method("balanceOf") \
            .params(params)\
            .build()

        response = self.process_call(call_balanceOf, self.icon_service)
        print("balanceOf : ", response)



