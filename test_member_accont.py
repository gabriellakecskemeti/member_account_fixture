from member_account import MemberAccount
import pytest


# Arrange
@pytest.fixture()       #define fixture
def confirmed_account():
    account = MemberAccount()
    account.register()
    account.confirm()
    return account


def test_member_account_start_state():
    account = MemberAccount()
    assert account.get_state() == MemberAccount.START


def test_fail_when_cancelling_in_registered_state():
    # Arrange
    account = MemberAccount()
    account.register()

    # Act
    with pytest.raises(RuntimeError):
        account.cancel()


def test_fail_when_cancelling_in_start_state():
    # Arrange
    account = MemberAccount()

    # Act
    with pytest.raises(RuntimeError):
        account.cancel()


def test_member_account_register():
    account = MemberAccount()
    account.register()

    assert account.get_state() == MemberAccount.REGISTERED


def test_member_account_active(confirmed_account):

    assert confirmed_account.get_state() == MemberAccount.ACTIVE   #using fixture confirmed_account()


def test_creation_and_cancellation(confirmed_account):
    # Act
    confirmed_account.cancel()  #using fixture confirmed_account()

    # Assert
    assert confirmed_account.get_state() == MemberAccount.END


def test_creation_and_change(confirmed_account):
    # Act
    confirmed_account.change()  #using fixture confirmed_account()

    # Assert
    assert confirmed_account.get_state() == MemberAccount.ACTIVE


def test_member_account_feedue(confirmed_account):
    confirmed_account.fee_due()

    assert confirmed_account.get_state() == MemberAccount.INACTIVE


def test_member_account_suspend(confirmed_account):
    confirmed_account.suspend()

    assert confirmed_account.get_state() == MemberAccount.DORMANT


def test_member_account_transfer_of_inactive(confirmed_account):
    confirmed_account.fee_due()
    confirmed_account.transfer()
    assert confirmed_account.get_state() == MemberAccount.ACTIVE


def test_member_account_dormant_reactivate(confirmed_account):

    confirmed_account.reactivate()
    assert confirmed_account.get_state() == MemberAccount.ACTIVE

def test_fail_when_inactive_reactivate(confirmed_account):
    # Arrange
    confirmed_account.fee_due()

    # Act
    with pytest.raises(RuntimeError):
        confirmed_account.reactivate()