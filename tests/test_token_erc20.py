import pytest
from brownie import Wei, accounts, token_erc20

@pytest.fixture
def _token_erc20():
    _token_erc20 = token_erc20.deploy({'from':accounts[0]})
    return _token_erc20

# Made sure that tokens were in fact distributed
def test_distribute_token(_token_erc20):
    pre_current_supply = _token_erc20.supply_left()
    _token_erc20.distribute_token(100, accounts[1], {'from': accounts[0]})
    assert _token_erc20.supply_left() < pre_current_supply

# Made sure I could transfer tokens correctly
def test_transfer_token(_token_erc20):
    _token_erc20.distribute_token(200, accounts[1], {'from': accounts[0]})
    pre_current_supply = _token_erc20.addr_amount({'from': accounts[1]})
    assert pre_current_supply == 200
    _token_erc20.transfer_token(100, accounts[2], {'from': accounts[1]})
    assert pre_current_supply > _token_erc20.addr_amount({'from': accounts[1]})
    assert _token_erc20.addr_amount({'from': accounts[2]}) == 100

# Make sure you can approve correctly, show difference between pre/post allowance
def test_token_approval(_token_erc20):
    _token_erc20.distribute_token(300, accounts[1], {'from': accounts[0]})
    pre_allowance = _token_erc20.view_allowance(accounts[1], {'from': accounts[2]})
    assert pre_allowance == 0
    _token_erc20.increase_allowance(150, accounts[2], {'from': accounts[1]})
    assert _token_erc20.view_allowance(accounts[1], {'from': accounts[2]}) - pre_allowance == 150

# Make sure supply is displayed correctly
def test_token_supply(_token_erc20):
    initial_supply = _token_erc20.supply_left({'from': accounts[0]})
    _token_erc20.distribute_token(400, accounts[3], {'from': accounts[0]})
    assert initial_supply - 400 == _token_erc20.supply_left({'from': accounts[0]})

# Make sure increase/decrease allowance works
def test_approval_change(_token_erc20):
    _token_erc20.distribute_token(500, accounts[1], {'from': accounts[0]})
    _token_erc20.increase_allowance(220, accounts[2], {'from': accounts[1]})
    assert _token_erc20.view_allowance(accounts[1], {'from': accounts[2]}) == 220
    _token_erc20.decrease_allowance(120, accounts[2], {'from': accounts[1]})
    assert _token_erc20.view_allowance(accounts[1], {'from': accounts[2]}) == 100

# Make sure transfer from works
def test_transfer_from(_token_erc20):
    _token_erc20.distribute_token(600, accounts[1], {'from': accounts[0]})
    _token_erc20.increase_allowance(300, accounts[2], {'from': accounts[1]})
    pre_transfer = _token_erc20.addr_amount({'from': accounts[1]})
    assert pre_transfer == 600
    _token_erc20.transfer_from(250, accounts[1], accounts[3], {'from': accounts[2]})
    assert _token_erc20.addr_amount({'from': accounts[1]}) == pre_transfer - 250
    assert _token_erc20.view_allowance(accounts[1], {'from': accounts[2]}) == 50
    assert _token_erc20.addr_amount({'from': accounts[3]}) == 250

    