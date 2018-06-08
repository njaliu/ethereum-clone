
======= examples/Coin.sol:Coin =======
EVM assembly:
    /* "examples/Coin.sol":0:224  contract Coin {... */
  mstore(0x40, 0x60)
  jumpi(tag_1, iszero(callvalue))
  0x0
  dup1
  revert
tag_1:
  dataSize(sub_0)
  dup1
  dataOffset(sub_0)
  0x0
  codecopy
  0x0
  return
stop

sub_0: assembly {
        /* "examples/Coin.sol":0:224  contract Coin {... */
      mstore(0x40, 0x60)
      jumpi(tag_1, lt(calldatasize, 0x4))
      calldataload(0x0)
      0x100000000000000000000000000000000000000000000000000000000
      swap1
      div
      0xffffffff
      and
      dup1
      0x27e235e3
      eq
      tag_2
      jumpi
      dup1
      0xd0679d34
      eq
      tag_3
      jumpi
    tag_1:
      0x0
      dup1
      revert
        /* "examples/Coin.sol":18:59  mapping (address => uint) public balances */
    tag_2:
      jumpi(tag_4, iszero(callvalue))
      0x0
      dup1
      revert
    tag_4:
      tag_5
      0x4
      dup1
      dup1
      calldataload
      0xffffffffffffffffffffffffffffffffffffffff
      and
      swap1
      0x20
      add
      swap1
      swap2
      swap1
      pop
      pop
      jump(tag_6)
    tag_5:
      mload(0x40)
      dup1
      dup3
      dup2
      mstore
      0x20
      add
      swap2
      pop
      pop
      mload(0x40)
      dup1
      swap2
      sub
      swap1
      return
        /* "examples/Coin.sol":64:222  function send (address recv, uint amount) {... */
    tag_3:
      jumpi(tag_7, iszero(callvalue))
      0x0
      dup1
      revert
    tag_7:
      tag_8
      0x4
      dup1
      dup1
      calldataload
      0xffffffffffffffffffffffffffffffffffffffff
      and
      swap1
      0x20
      add
      swap1
      swap2
      swap1
      dup1
      calldataload
      swap1
      0x20
      add
      swap1
      swap2
      swap1
      pop
      pop
      jump(tag_9)
    tag_8:
      stop
        /* "examples/Coin.sol":18:59  mapping (address => uint) public balances */
    tag_6:
      mstore(0x20, 0x0)
      dup1
      0x0
      mstore
      keccak256(0x0, 0x40)
      0x0
      swap2
      pop
      swap1
      pop
      sload
      dup2
      jump	// out
        /* "examples/Coin.sol":64:222  function send (address recv, uint amount) {... */
    tag_9:
        /* "examples/Coin.sol":138:144  amount */
      dup1
        /* "examples/Coin.sol":115:123  balances */
      0x0
        /* "examples/Coin.sol":115:135  balances[msg.sender] */
      dup1
        /* "examples/Coin.sol":124:134  msg.sender */
      caller
        /* "examples/Coin.sol":115:135  balances[msg.sender] */
      0xffffffffffffffffffffffffffffffffffffffff
      and
      0xffffffffffffffffffffffffffffffffffffffff
      and
      dup2
      mstore
      0x20
      add
      swap1
      dup2
      mstore
      0x20
      add
      0x0
      keccak256
      sload
        /* "examples/Coin.sol":115:144  balances[msg.sender] < amount */
      lt
        /* "examples/Coin.sol":112:151  if(balances[msg.sender] < amount) throw */
      iszero
      tag_11
      jumpi
        /* "examples/Coin.sol":146:151  throw */
      0x0
      dup1
      revert
        /* "examples/Coin.sol":112:151  if(balances[msg.sender] < amount) throw */
    tag_11:
        /* "examples/Coin.sol":181:187  amount */
      dup1
        /* "examples/Coin.sol":157:165  balances */
      0x0
        /* "examples/Coin.sol":157:177  balances[msg.sender] */
      dup1
        /* "examples/Coin.sol":166:176  msg.sender */
      caller
        /* "examples/Coin.sol":157:177  balances[msg.sender] */
      0xffffffffffffffffffffffffffffffffffffffff
      and
      0xffffffffffffffffffffffffffffffffffffffff
      and
      dup2
      mstore
      0x20
      add
      swap1
      dup2
      mstore
      0x20
      add
      0x0
      keccak256
      0x0
        /* "examples/Coin.sol":157:187  balances[msg.sender] -= amount */
      dup3
      dup3
      sload
      sub
      swap3
      pop
      pop
      dup2
      swap1
      sstore
      pop
        /* "examples/Coin.sol":211:217  amount */
      dup1
        /* "examples/Coin.sol":193:201  balances */
      0x0
        /* "examples/Coin.sol":193:207  balances[recv] */
      dup1
        /* "examples/Coin.sol":202:206  recv */
      dup5
        /* "examples/Coin.sol":193:207  balances[recv] */
      0xffffffffffffffffffffffffffffffffffffffff
      and
      0xffffffffffffffffffffffffffffffffffffffff
      and
      dup2
      mstore
      0x20
      add
      swap1
      dup2
      mstore
      0x20
      add
      0x0
      keccak256
      0x0
        /* "examples/Coin.sol":193:217  balances[recv] += amount */
      dup3
      dup3
      sload
      add
      swap3
      pop
      pop
      dup2
      swap1
      sstore
      pop
        /* "examples/Coin.sol":64:222  function send (address recv, uint amount) {... */
      pop
      pop
      jump	// out

    auxdata: 0xa165627a7a723058200a40fc051ddc56886cc2d8779d92e6a90788bb3f2c4643ce08d12a0aeb9ba5b70029
}

