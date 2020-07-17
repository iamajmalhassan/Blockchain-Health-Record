# Blockchain-Health-Record
Users can publish their Health Record on the Blockchain, where it can only be viewed/changed by the user, and a few selected people (such as doctors and health officials).

## Functions in the Smart Contract
### *createRecord()*:
  * Accepts ID, Name, Age, Gender, and the Test result of the patient and stores it in the blockchain.
  * Only a Patient can create/change the health record with this function, as it uses the *msg.sender* function.

### *changePatientRecord()*:
  * Accepts Patient's Address, ID, Name, Age, Gender, and the Test result of the patient and stores it in the blockchain.
  * Only the owner and doctor can create/change the health record with this function. It will revert the transaction if any other person calls this function.
### *viewRecord()*:
  * This function uses function overloading. 
  * One function is only for owner and doctor. They can view the record by passing in the address of the patient. 
  * The other function is for the patient, where they don't need to pass in any address as it finds the patient's address using the *msg.sender* function.
### *elevatePermission()*:
  * This function can only be accessed by the owner.
  * It accepts an address, and that address is given 'doctor' status, i.e. they can view/change a patient's record.
### *doctor*:
  * It is a mapping of address with bool data type.
  * Anyone can pass in an address, and if it is mapped to true, then that address belongs to a doctor. If it returns false, then that address does not belong to a doctor.
