pragma solidity ^0.4.0;

contract Wallet {
    address owner;

    function Wallet() payable {}

    function initContract() {
        owner = msg.sender;
    }

    function setOwner(address _owner) {
        if (msg.sender == owner) {
            owner = _owner;
        }
    }

    function transferEther(uint _value) {
        if(msg.sender == owner) {
            msg.sender.call.value(_value)();
        }
    }
}

