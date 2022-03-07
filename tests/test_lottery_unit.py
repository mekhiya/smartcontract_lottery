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


def test_get_entrance_fee():
    # account = accounts[0]
    # print("Deploying Lottery contract...")
    # lottery = Lottery.deploy(
    #     config["networks"][network.show_active()]["eth_usd_price_feed"],
    #     {"from": account},
    # )
    # print("Lottery contract deployed...")
    # print(f"lottery.getEntranceFee is {lottery.getEntranceFee()}")
    # assert lottery.getEntranceFee() > Web3.toWei(0.017, "ether")
    # assert lottery.getEntranceFee() < Web3.toWei(0.020, "ether")
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    # Act
    expected_entrance_fee = Web3.toWei(0.025, "ether")
    entrance_fee = lottery.getEntranceFee()
    # Assert
    assert expected_entrance_fee == entrance_fee


def test_cant_enter_unless_started():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({"from": get_account(), "value": lottery.getEntranceFee()})


def test_can_start_and_enter_lottery():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    # Act
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    # Assert
    assert lottery.players(0) == account


def test_can_end_lottery():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    xx = lottery.startLottery({"from": account})
    xx.wait(1)
    # Act
    lx = lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lx.wait(1)
    txx = fund_contract_with_Link(lottery.address)
    txx.wait(1)
    tx = lottery.endLottery({"from": account})
    tx.wait(1)
    # Assert
    assert lottery.lottery_state() == 2


def test_can_pick_correct_winner():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    xx = lottery.startLottery({"from": account})
    xx.wait(1)
    # Act
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": get_account(index=1), "value": lottery.getEntranceFee()})
    lottery.enter({"from": get_account(index=1), "value": lottery.getEntranceFee()})

    fund_contract_with_Link(lottery.address)
    tx = lottery.endLottery({"from": account})
    request_Id = tx.events["RequestedRandomness"]["requestId"]
    STATIC_RNG = 777
    get_contract("vrf_coordinator").callBackWithRandomness(
        request_Id, STATIC_RNG, lottery.address, {"from": account}
    )
    starting_balance_of_account = account.balance()
    balance_of_lottery = lottery.balance()
    # Assert
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
    assert account.balance() == starting_balance_of_account + balance_of_lottery
