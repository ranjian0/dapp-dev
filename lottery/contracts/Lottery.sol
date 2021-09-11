// SPDX-License-Identifier: MIT
pragma solidity ^0.8.3;

contract Lottery {
    address public manager;
    address[] public players;

    constructor() {
        manager = msg.sender;
    }

    function enter() public payable {
        // require(msg.value > .01 ether, "Not enough ether provided");
        players.push(msg.sender);
    }

    function random() private view returns (uint) {
        return uint(keccak256(abi.encodePacked(block.difficulty, block.timestamp, players)));
    }

    function pick_winner() public restricted {
        uint index = random() % players.length;

        address payable p = payable(players[index]);
        p.transfer(address(this).balance);

        players = new address[](0);
    }

    function get_players() public view returns (address[] memory) {
        return players;
    }

    function get_balance() public view returns (uint) {
        return address(this).balance;
    }

    modifier restricted() {
        require(msg.sender == manager);
        _;
    }
}