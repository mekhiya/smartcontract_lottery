import time
from brownie import Lottery, accounts, network, config
from scripts.helpful_scripts import fund_contract_with_Link, get_account, get_contract


def deploy_lottery():
    print("deploying lottery started...")
    account = get_account()
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print("Deployed lottery!")
    return lottery


def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    starting_tx = lottery.startLottery({"from": account})
    starting_tx.wait(1)
    print("Lottery started!")


def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    enter_value = lottery.getEntranceFee() + 10000000
    tx = lottery.enter({"from": account, "value": enter_value})
    tx.wait(1)
    print("Entered in to Lottery")


def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    tx = fund_contract_with_Link(lottery.address)
    tx.wait(1)
    ending_tx = lottery.endLottery({"from": account})
    ending_tx.wait(1)
    print("Lottery ended!")
    time.sleep(60)
    print(f"Recent winner is {lottery.recentWinner()}")


def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()
