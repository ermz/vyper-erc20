# @version ^0.2.0

owner: address
MAX_SUPPLY: constant(uint256) = 1000000000
distributed_supply: uint256
ledger: HashMap[address, uint256]
allowances: HashMap[address, HashMap[address, uint256]]

@external
def __init__():
    self.owner = msg.sender


@external
@view
def addr_amount() -> uint256:
    return self.ledger[msg.sender]


@external
@view
def supply_left() -> uint256:
    return MAX_SUPPLY - self.distributed_supply

@external
@view
def view_allowance(_from: address) -> uint256:
    return self.allowances[_from][msg.sender]


@external
def distribute_token(amount: uint256, to: address) -> uint256:
    # Assert that only the sender can distribute tookens and that there are enough to distribute
    assert msg.sender == self.owner, "Only the owner can distribute tokens"
    assert amount <= (MAX_SUPPLY - self.distributed_supply), "There's not enough tokens to distribute"

    # Add the amount to the corresponding address, we add the distribute_supply var to keep track
    self.ledger[to] += amount
    self.distributed_supply += amount

    # We return the current token amount to the address owner
    return self.ledger[to]


@external
def transfer_token(amount: uint256, to: address) -> uint256:
    assert msg.sender != self.owner, "Owner can only initially distribute, it should not transfer on their own accord"
    assert amount <= self.ledger[msg.sender], "Sender of funds must have enough tokens to transfer"

    # We substract amount from the sender and add that same amount to the receiver
    self.ledger[msg.sender] -= amount
    self.ledger[to] += amount

    # We return the current amount of the sendee
    return self.ledger[msg.sender]


@external
def transfer_from(amount: uint256, _from: address, _to: address) -> bool:
    # Check the amount that is allowed, also checks that sender has been approved
    # Assert that the address isn't a zero address
    assert self.allowances[_from][msg.sender] >= amount, "The amount is higher than what's permissible"
    assert _to != ZERO_ADDRESS

    # Move amount from the Seding address to the Receiving address
    self.ledger[_from] -= amount
    self.ledger[_to] += amount

    # Reduce allowance permission by the amount that was used
    self.allowances[_from][msg.sender] -= amount
    return True

# Could potentially return the amount of the address that received and then be called later on increase/decrease allowance functions
@internal
def approve(_from: address, amount: uint256, to: address):
    assert _from != ZERO_ADDRESS
    assert to != ZERO_ADDRESS
    # assert amount <= self.ledger[_from], "You can't give allowance at an amount of which you don't have"

    self.allowances[_from][to] = amount


@external
def increase_allowance(amount: uint256, to: address) -> bool:
    self.approve(msg.sender, (self.allowances[msg.sender][to] + amount), to)
    return True


@external
def decrease_allowance(amount: uint256, to: address) -> bool:
    self.approve(msg.sender, (self.allowances[msg.sender][to] - amount), to)
    return True

