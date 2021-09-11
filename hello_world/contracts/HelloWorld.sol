// SPDX-License-Identifier: MIT
pragma solidity ^0.8.3;

contract HelloWorld {
    string public greeting = "Hello, World";

    function get_greeting() public view returns (string memory) {
        return greeting;
    }

    function set_greeting(string memory _greeting) public {
        greeting = _greeting;
    }
}