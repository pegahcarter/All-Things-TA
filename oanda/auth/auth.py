
def Auth():
    accountID, token = None, None
    with open("/home/carter/peter-signal/oanda/auth/account.txt") as I:
        accountID = I.read().strip()
    with open("/home/carter/peter-signal/oanda/auth/token.txt") as I:
        token = I.read().strip()
    return accountID, token
