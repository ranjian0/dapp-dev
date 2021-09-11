// SPDX-License-Identifier: MIT
pragma solidity ^0.8.3;

contract HelloWorld {
    string public greeting = "Hello, World";

    function hello() public view returns (string memory) {
        return greeting;
    }
}