from brownie import Collectible
from scripts.helpful_scripts import fund_with_link, get_account
from web3 import Web3


def main():
    account = get_account()
    collectible = Collectible[-1]
    fund_with_link(collectible.address, amount=Web3.toWei(0.1, "ether"))
    tx = collectible.createCollectible({"from": account})
    tx.wait(1)
    print("Collectible created")


# def main():
#     create_new_collectible()
