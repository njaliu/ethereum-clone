contract EtherBank {
    mapping(address => uint) balances;
    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw(uint amount) public {
        if (balances[msg.sender] >= amount) {
        msg.sender.call.value(amount)();
        balances[msg.sender] -= amount;
        }
    }
}
