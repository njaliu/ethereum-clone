contract Coin {
  mapping (address=>uint) public balances;

  function send (address recv, uint amount) {
    if(balances[msg.sender] < amount) throw;
    balances[msg.sender] -= amount;
    balances[recv] += amount;
    recv.call.value(amount)();
  }
}
