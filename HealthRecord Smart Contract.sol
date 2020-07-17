pragma solidity 0.6.10;
//SPDX-License-Identifier: GPL-3.0

contract Record{
    address public owner;
    mapping(address => bool) public doctor; //doctors can view the health records
    struct patient{
        uint256 id;
        string name;
        uint64 age;
        bool gender; //0:Male, 1:Female
        bool testResult; //0: Negative, 1: Positive
    }
    mapping(address => patient) record; //Storing patient records in a mapping of structures
    constructor() public {
        owner=msg.sender;
    }
    
    //create or change Patient record (for the patient)
    function createRecord(uint256 _id, string memory _name,uint64 _age, bool _gender, bool _testResult) public     
    {
        record[msg.sender]= patient(_id,_name,_age,_gender,_testResult);
    }
    
    //changeRecord function for the owner and the doctor
    function changePatientRecord(address _patient,uint256 _id, string memory _name,uint64 _age, bool _gender, bool _testResult) public
    {
        if(msg.sender==owner || doctor[msg.sender]==true) //Only owner or doctor can use this function.
        {
            record[_patient]= patient(_id,_name,_age,_gender,_testResult);
        }
        else
        {
            revert();
        }
    }
    
    //Only the patient, the doctor or the owner can view the patient's record.
    //I am using function overloading: one function for the onwer and doctor and another function for the patient.
    //viewRecord function for the owner and doctor
    function viewRecord(address _patient) view public returns(uint256 id, string memory name,uint64 age, bool gender, bool testResult)
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
    
    //viewRecord function for the patient
    function viewRecord() view public returns(uint256 id, string memory name,uint64 age, bool gender, bool testResult)
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
