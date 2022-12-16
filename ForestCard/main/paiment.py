from yoomoney import Authorize
id = '13E66635AD6BFAC21FE1DF88F0ECF46D8A7BA124D99473C4784F8F5778BAF356'
secret = 'A39863EAD45F11BBC72D8572653D5E6F101A2746D69DD582C11B0C51EE4A892117DBC411067FAB9505C91595543DF5212F45BE03330FCBB7276B05857A6D6E15'

# token = Authorize(
# client_id="13E66635AD6BFAC21FE1DF88F0ECF46D8A7BA124D99473C4784F8F5778BAF356",
#       redirect_uri="http://127.0.0.1/",
#       scope=["account-info",
#              "operation-history",
#              "operation-details",
#              "incoming-transfers",
#              "payment-p2p",
#              "payment-shop",
#              ]
# )
#
# from yoomoney import Client
#
# client = Client(secret)
#
# user = client.account_info()
#
# print("Account number:", user.account)
# print("Account balance:", user.balance)
# print("Account currency code in ISO 4217 format:", user.currency)
# print("Account status:", user.account_status)
# print("Account type:", user.account_type)
#
# print("Extended balance information:")
# for pair in vars(user.balance_details):
#     print("\t-->", pair, ":", vars(user.balance_details).get(pair))
#
# print("Information about linked bank cards:")
# cards = user.cards_linked
#
# if len(cards) != 0:
#     for card in cards:
#         print(card.pan_fragment, " - ", card.type)
# else:
#     print("No card is linked to the account")
from yoomoney import Quickpay

def get_payment_link(sum):
    quickpay = Quickpay(
            receiver="410017519577453",
            quickpay_form="shop",
            targets="Sponsor this project",
            paymentType="SB",
            sum=sum,
            )
    return quickpay.base_url