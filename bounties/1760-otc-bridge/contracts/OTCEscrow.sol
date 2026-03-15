// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * OTC Escrow Contract for RustChain Bridge
 * Bounty #1760 - OTC Bridge - RTC Swap Page
 */

contract OTCEscrow {
    enum State { Created, Locked, Completed, Cancelled }
    
    struct Order {
        address maker;
        address taker;
        uint256 amount;
        uint256 price;
        State state;
        uint256 createdAt;
    }
    
    mapping(uint256 => Order) public orders;
    uint256 public orderCount;
    address public owner;
    
    event OrderCreated(uint256 indexed orderId, address indexed maker, uint256 amount);
    event OrderFilled(uint256 indexed orderId, address indexed taker);
    event OrderCancelled(uint256 indexed orderId);
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }
    
    modifier validOrder(uint256 _orderId) {
        require(orders[_orderId].state == State.Created, "Invalid order");
        _;
    }
    
    constructor() {
        owner = msg.sender;
    }
    
    function createOrder(uint256 _amount, uint256 _price) external returns (uint256) {
        orders[orderCount] = Order({
            maker: msg.sender,
            taker: address(0),
            amount: _amount,
            price: _price,
            state: State.Created,
            createdAt: block.timestamp
        });
        
        emit OrderCreated(orderCount, msg.sender, _amount);
        return orderCount++;
    }
    
    function fillOrder(uint256 _orderId) external payable validOrder(_orderId) {
        Order storage order = orders[_orderId];
        require(msg.sender != order.maker, "Cannot fill own order");
        require(msg.value >= order.amount * order.price, "Insufficient payment");
        
        order.taker = msg.sender;
        order.state = State.Completed;
        
        emit OrderFilled(_orderId, msg.sender);
        
        // Transfer to maker
        payable(order.maker).transfer(msg.value);
    }
    
    function cancelOrder(uint256 _orderId) external validOrder(_orderId) {
        Order storage order = orders[_orderId];
        require(msg.sender == order.maker, "Only maker can cancel");
        
        order.state = State.Cancelled;
        emit OrderCancelled(_orderId);
    }
    
    function getOrder(uint256 _orderId) external view returns (Order memory) {
        return orders[_orderId];
    }
    
    function withdraw() external onlyOwner {
        payable(owner).transfer(address(this).balance);
    }
}
