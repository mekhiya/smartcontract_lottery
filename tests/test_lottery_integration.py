from operator import index
from brownie import Lottery, accounts, network, config, exceptions
from scripts.deploy_lottery import deploy_lottery
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    fund_contract_with_Link,
    get_account,
    get_contract,
)
from web3 import Web3
import pytest
import time


def test_can_pick_correct_winner_integration():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    fund_contract_with_Link(lottery)
    lottery.endLottery({"from": account})
    time.sleep(120)
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
