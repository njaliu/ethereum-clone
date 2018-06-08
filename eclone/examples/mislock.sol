contract EtherBank4 {
  mapping(address => uint) balances;
  bool locked;
  function deposit() public payable {
    balances[msg.sender] += msg.value;
  }
  function withdraw(uint amount) public {
    lock();
    if (balances[msg.sender] >= amount) {
      if (!msg.sender.call.value(amount)()) revert();
          balances[msg.sender] -= amount;
        }
        unlock();
  }
  function lock() {
    if (!locked)
      locked = true;
    else
        revert();
    }
    function unlock() {
      locked = false;
    }
}
