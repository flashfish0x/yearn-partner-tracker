from web3._utils.events import construct_event_topic_set
from brownie import YearnPartnerTracker, web3
import time

partner_tracker = YearnPartnerTracker.at('0x8ee392a4787397126C163Cb9844d7c447da419D8')


def main():
    print("start")

    ctroller = web3.eth.contract(str(partner_tracker), abi=partner_tracker.abi)
    topics = construct_event_topic_set(
        ctroller.events.ReferredBalanceIncreased().abi,
        web3.codec,
    )
   
    timestam = time.perf_counter()
    logs = web3.eth.get_logs({"address": partner_tracker.address, 'topics': topics, "fromBlock": 14166636})
    lapse = time.perf_counter() - timestam

    print("time taken: ", lapse)

    referrals = [ctroller.events.ReferredBalanceIncreased().processLog(x) for x in logs]
    partners = {}
    for log in referrals:
        partId = log["args"]["partnerId"]
        if partners.get(partId):
            partners.partId.amount += log["args"]["amountAdded"]
        else:
           partners.partId.amount = log["args"]["amountAdded"]

    print(partners)

