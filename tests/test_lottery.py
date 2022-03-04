from brownie import Lottery, accounts, network, config
from web3 import Web3


def test_get_entrance_fee():
    account = accounts[0]
    print("Deploying Lottery contract...")
    lottery = Lottery.deploy(
        config["networks"][network.show_active()]["eth_usd_price_feed"],
        {"from": account},
    )
    print("Lottery contract deployed...")
    print(f"lottery.getEntranceFee is {lottery.getEntranceFee()}")
    assert lottery.getEntranceFee() > Web3.toWei(0.017, "ether")
    assert lottery.getEntranceFee() < Web3.toWei(0.020, "ether")
