pragma solidity >=0.6.0 <=0.7.0;
//SPDX-License-Identifier: GPL-3.0

contract Record{
    address public owner;
    mapping(address => bool) public doctor; //doctors can view the health records
    struct patient{
        uint256 id;
        string name;
        uint64 age;
        string gender;
        bool testResult; //0: Negative, 1: Positive
    }
    mapping(address => patient) record;
    constructor() public {
        owner=msg.sender;
    }
    
    //create or change Patient record
    function createRecord(uint256 _id, string memory _name,uint64 _age, string memory _gender, uint8 _testResult) public     
    {
        if(_testResult==0)
        {
            record[msg.sender]= patient(_id,_name,_age,_gender,false);
        }
        else
        {
            record[msg.sender]= patient(_id,_name,_age,_gender,true);
        }
    }
    
    //changeRecord function for the owner and the doctor
    function changePatientRecord(uint256 _id, string memory _name,uint64 _age, string memory _gender, bool _testResult) public
    {
        if(msg.sender==owner || doctor[msg.sender]==true)
        {
            record[msg.sender]= patient(_id,_name,_age,_gender,_testResult);
        }
        else
        {
            revert();
        }
    }
    
    //Only the patient, the doctor or the owner can view the patient's record.
    //I am using function overloading: one function for the onwer and doctor and another function for the patient.
    function viewRecord(address _patient) view public returns(uint256 id, string memory name,uint64 age, string memory gender, bool testResult)
    {
        if(doctor[msg.sender]==true || msg.sender==owner)
        {
            return(record[_patient].id,record[_patient].name,record[_patient].age,record[_patient].gender,record[_patient].testResult);
        }
        else
        {
            revert();
        }
    }
    function viewRecord() view public returns(uint256 id, string memory name,uint64 age, string memory gender, bool testResult)
    {
        return(record[msg.sender].id,record[msg.sender].name,record[msg.sender].age,record[msg.sender].gender,record[msg.sender].testResult);
    }
    //only owner can assign doctors.
    function elevatePermission(address _doctor) public
    {
        require(msg.sender==owner,"Only owner can elevate Permission.");
        doctor[_doctor]=true;
    }
}