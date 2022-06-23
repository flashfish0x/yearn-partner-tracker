from web3._utils.events import construct_event_topic_set
from brownie import YearnPartnerTracker, web3, chain, interface
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
    partners = []
    depositers = []
    
    for log in referrals:
        partId = log["args"]["partnerId"]
        if partId not in partners:
            partners.append(partId)

        vault = log["args"]["vault"]
        depositer = log["args"]["depositer"]

        if depositer not in depositers:
            depositers.append(depositer)

        txhash = log["transactionHash"]
        
        #we are looking for transfer events of the vault in the same tx
        transfer_event_hash = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
        transaction_logs = chain.get_transaction(txhash).logs
        last_transfer = {}# we only care about the last transfer of vault tokens in the log, where do they end up?

        for logs in transaction_logs:

            if (logs["topics"][0]).hex() == transfer_event_hash and logs["address"] == vault:
                print("transfer_found")
                last_transfer = logs
        
        destination = (last_transfer["topics"][2]).hex() #where to tokens are transfered to

        

    print("partners: ", partners)
    print("depositers: ", depositers)
