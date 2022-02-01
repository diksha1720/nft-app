from brownie import Collectible, network
from scripts.helpful_scripts import get_nft
from metadata.template import metadata_template
from pathlib import Path
import requests
import os
import json


TOKEN_TO_IMGURI = {}
TOKEN_TO_URI = {}


def create_new_metadata():
    collectible = Collectible[-1]
    no_of_tokens = collectible.tokenCounter()
    print(f"You have {no_of_tokens} tokens")
    for token_id in range(no_of_tokens):
        token_type = get_nft(collectible.tokenIdToGirl(token_id))
        metadata_file_name = f"./metadata/{network.show_active()}/{token_type}.json"
        # print(metadata_file_name)
        collectible_metadata = metadata_template
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists! Delete it to overwrite")
        else:
            print(f"Creating Metadata file: {metadata_file_name}")
            collectible_metadata["name"] = token_type
            collectible_metadata["description"] = f"An example of women empowerment"
            img_path = f"./img/{token_type.lower()}.png"
            # print(img_path)
            image_uri = upload_to_pinata(img_path)
            TOKEN_TO_IMGURI[token_type] = image_uri
            collectible_metadata["image"] = image_uri
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)
            token_uri = upload_to_pinata(metadata_file_name)
            TOKEN_TO_URI[token_type] = token_uri
    with open("./tokensToImageURIs.json", "w") as file:
        json.dump(TOKEN_TO_IMGURI, file)
    with open("./tokensURIs.json", "w") as file:
        json.dump(TOKEN_TO_URI, file)


def upload_to_ipfs(filepath):
    with open(filepath, "rb") as file:
        binary = file.read()
        ipfs_url = "http://127.0.0.1:5001/api/v0/add"
        response = requests.post(ipfs_url, files={"file": binary})
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1:][0]
        file_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(file_uri)
        return file_uri


def upload_to_pinata(filepath):
    pinata_url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    filename = filepath.split("/")[-1:][0]
    headers = {
        "pinata_api_key": os.getenv("PINATA_API_KEY"),
        "pinata_secret_api_key": os.getenv("PINATA_API_SECRET"),
    }
    with open(filepath, "rb") as file:
        binary = file.read()
        response = requests.post(
            pinata_url, files={"file": (filename, binary)}, headers=headers
        )
        ipfs_hash = response.json()["IpfsHash"]
        file_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(file_uri)
        return file_uri


def main():
    create_new_metadata()
