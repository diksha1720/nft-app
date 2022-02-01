from brownie import Collectible, config, network
from scripts.helpful_scripts import (
    get_account,
    get_contract,
    get_contract,
    fund_with_link,
    NAME,
    SYMBOL,
)


def deploy_and_create():
    account = get_account()
    collectible = Collectible.deploy(
        get_contract("vrf_coordinator"),
        get_contract("link_token"),
        config["networks"][network.show_active()]["keyhash"],
        config["networks"][network.show_active()]["fee"],
        NAME,
        SYMBOL,
        {"from": account},
    )
    fund_with_link(collectible.address)
    tx = collectible.createCollectible({"from": account})
    tx.wait(1)
    print("New token created")
    print(f"token counter  = {collectible.tokenCounter()}")
    return collectible, tx


def main():
    deploy_and_create()
