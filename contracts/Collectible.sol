// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract Collectible is ERC721, VRFConsumerBase {
    uint256 public tokenCounter;
    bytes32 public keyhash;
    uint256 public fee;

    enum Girl {
        GIRL1,
        GIRL2,
        GIRL3
    }

    mapping(uint256 => Girl) public tokenIdToGirl;
    mapping(bytes32 => address) public requestIdtoSender;

    event requestedCollectible(bytes32 indexed requestId, address requester);
    event girlAssigned(uint256 indexed tokenId, Girl girl);

    constructor(
        address _vrfCoordinator,
        address _linkToken,
        bytes32 _keyhash,
        uint256 _fee,
        string memory _name,
        string memory _symbol
    )
        public
        ERC721(_name, _symbol)
        VRFConsumerBase(_vrfCoordinator, _linkToken)
    {
        tokenCounter = 0;
        keyhash = _keyhash;
        fee = _fee;
    }

    function createCollectible() public returns (bytes32) {
        bytes32 requestId = requestRandomness(keyhash, fee);
        requestIdtoSender[requestId] = msg.sender;
        emit requestedCollectible(requestId, msg.sender);
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomNumber)
        internal
        override
    {
        Girl girl = Girl(randomNumber % 3);
        uint256 newTokenId = tokenCounter;
        tokenIdToGirl[newTokenId] = girl;
        emit girlAssigned(newTokenId, girl);
        address owner = requestIdtoSender[requestId];
        _safeMint(owner, newTokenId);
        tokenCounter = tokenCounter + 1;
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "ERC721: caller is not owner no approved"
        );
        _setTokenURI(tokenId, _tokenURI);
    }
}
