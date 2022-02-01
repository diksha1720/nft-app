from brownie import network, Collectible
from numpy import number
from scripts.helpful_scripts import OPENSEA_URL, get_account, get_nft
import json


def main():

    print(f"Working on {network.show_active()}")
    collectible = Collectible[-1]
    number_of_collectibles = collectible.tokenCounter()
    print(f"You have {number_of_collectibles} tokenIds")
    for token_id in range(number_of_collectibles):
        girl = get_nft(collectible.tokenIdToGirl(token_id))
        if not collectible.tokenURI(token_id).startswith("https://"):
            print(f"Setting tokenURI of {token_id}")
            set_tokenURI(token_id, collectible, girl)


def set_tokenURI(token_id, nft_contract, girl):
    account = get_account()
    with open("./tokensURIs.json", "r") as file:
        nftTotokenURI = json.load(file)
        tokenURI = nftTotokenURI[girl]
    tx = nft_contract.setTokenURI(token_id, tokenURI, {"from": account})
    tx.wait(1)
    print(
        f"Awesome! You can view your NFT at {OPENSEA_URL.format(nft_contract.address, token_id)}"
    )
    print("Please wait up to 20 minutes, and hit the refresh metadata button")
