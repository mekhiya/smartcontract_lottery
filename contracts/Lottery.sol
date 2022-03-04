// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract Lottery {
    address payable[] public players;
    uint256 public usdEntryFee;
    AggregatorV3Interface internal ethUsdpriceFeed;

    constructor(address _priceFeed) public {
        usdEntryFee = 50 * (10**18);
        ethUsdpriceFeed = AggregatorV3Interface(_priceFeed);
    }

    function enter() public payable {
        require(msg.value >= getEntranceFee(), "Not enought ETH!");
        players.push(msg.sender);
    }

    function startLottery() public {}

    function endLottery() public {}

    function getEntranceFee() public view returns (uint256) {
        (, int256 price, , , ) = ethUsdpriceFeed.latestRoundData();
        uint256 adjustedPrice = uint256(price) * 10**10;
        uint256 costToEnter = (usdEntryFee * 10**18) / adjustedPrice;
        return costToEnter;
    }
}
