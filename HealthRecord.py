from web3 import Web3
import json
import time
import sys
from eth_account import Account

#I am using Ganache; You can use your Infura link as url
url = "HTTP://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(url))
account = input("Enter your account number : ")

# I am using hosted private keys(Ganache), so I don't need to sign transactions. So, I am asking the user's private key to verify the account.
# This is not recommended, but I am excusing myself as it is just for demo purpose.
pvtKey = input("Enter your Private key : ")
acct = Account.from_key(pvtKey)
derived_account = acct.address
if derived_account!=account:
	print("Wrong private key!")
	print("Exiting...")
	time.sleep(2)
	sys.exit()
print(" ")
web3.eth.defaultAccount = web3.eth.accounts[0]
abi = json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"address","name":"_patient","type":"address"},{"internalType":"uint256","name":"_id","type":"uint256"},{"internalType":"string","name":"_name","type":"string"},{"internalType":"uint64","name":"_age","type":"uint64"},{"internalType":"bool","name":"_gender","type":"bool"},{"internalType":"bool","name":"_testResult","type":"bool"}],"name":"changePatientRecord","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_id","type":"uint256"},{"internalType":"string","name":"_name","type":"string"},{"internalType":"uint64","name":"_age","type":"uint64"},{"internalType":"bool","name":"_gender","type":"bool"},{"internalType":"bool","name":"_testResult","type":"bool"}],"name":"createRecord","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"doctor","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_doctor","type":"address"}],"name":"elevatePermission","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_patient","type":"address"}],"name":"viewRecord","outputs":[{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"string","name":"name","type":"string"},{"internalType":"uint64","name":"age","type":"uint64"},{"internalType":"bool","name":"gender","type":"bool"},{"internalType":"bool","name":"testResult","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"viewRecord","outputs":[{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"string","name":"name","type":"string"},{"internalType":"uint64","name":"age","type":"uint64"},{"internalType":"bool","name":"gender","type":"bool"},{"internalType":"bool","name":"testResult","type":"bool"}],"stateMutability":"view","type":"function"}]')
address = web3.toChecksumAddress("0xbb3050B1b6bBf6dB3ebd0550f18825b74f97d223")
contract = web3.eth.contract(address=address,abi=abi)
owner = contract.functions.owner().call()
def admin(account):
	global owner
	while(1):
		print("What do you want to do?\n")
		print("1. View a Patient Record.")
		print("2. Change a Patient's Health Record.")
		print("3. Check whether given Address is a Doctor.")
		print("4. Exit")
		
		#Only owner has permission to assign doctors.
		#The smart contract also prevents patient and doctors from using the 'elevatePermission' function.
		if(account==owner):
			print("5. Elevate Permission (Assign Doctor).")
		c=int(input())
		if(c==1):
			patient=input("Enter the Patient's Account Number : ")
			try:
				record = contract.functions.viewRecord(patient).call({'from':account})
				if(record[0]==0):
					print("The Patient does not exist.")
					continue
				print("ID:",record[0])
				print("Name:",record[1])
				print("Age:",record[2])
				if(record[3]):
					print("Gender: Female")
				else:
					print("Gender: Male")
				if(record[4]):
					print("Test Result: Positive")
				else:
					print("Test Result: Negative")
				print(" ")
			except:
				print("The Transaction did not go through. Try again...")
				time.sleep(2)
		if(c==2):
			patient = input("Enter the Patient's Account Number : ")
			try:
				idn=int(input("Enter Patient's ID: "))
				name=input("Enter Patient's Name: ")
				age=int(input("Enter Patient's Age: "))
				gender=int(input("Enter Patient's Gender (0:Male 1:Female) : "))
				if(gender==0):
					gender=False
				else:
					gender=True
				testResult=int(input("Enter Patient's Test Result (0:Negative 1:Positive) : "))
				if(testResult==0):
					testResult=False
				else:
					testResult=True
				tx_hash = contract.functions.changePatientRecord(patient,idn,name,age,gender,testResult).transact({'from':account})
				tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
				print("\nSuccessfully altered the Record.\n")
				print("Transaction Hash:  ",web3.toHex(tx_hash))
				print(" ")
			except:
				print("The Transaction did not go through. Try again...")
				time.sleep(2)
		if(c==3):
			isDoctor = input("Enter the Account Address: ")
			try:
				res = contract.functions.doctor(isDoctor).call()
				if(res is True):
					print("\nYes, It's a Doctor's account.")
				else:
					print("\nNo, It's not a Doctor's account.")
				print(" ")
			except:
				print("The Transaction did not go through. Try again...")
				time.sleep(2)
		if(c==4):
			print("\nExiting...\n")
			time.sleep(1)
			sys.exit()
		if(c==5):
			doctor = input("Enter the Doctor's Address : ")
			try:
				tx_hash = contract.functions.elevatePermission(doctor).transact({'from':account})
				tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
				print("Transaction Successful.")
				print("Transaction Hash: ",web3.toHex(tx_hash))
				print(" ")
			except:
				print("\nOnly the owner can elevate Permission.\n")
				time.sleep(2)

def patient(account):
	while(1):
		print("What do you want to do?\n")
		print("1. Create or Change your Record.")
		print("2. View your Health Record.")
		print("3. Check whether given Address is a Doctor.")
		print("4. Exit")
		c=int(input())
		if(c==1):
			idn=int(input("Enter Patient's ID: "))
			name=input("Enter Patient's Name: ")
			age=int(input("Enter Patient's Age: "))
			gender=int(input("Enter Patient's Gender (0:Male 1:Female) : "))
			if(gender==0):
				gender=False
			else:
				gender=True
			testResult=int(input("Enter Patient's Test Result (0:Negative 1:Positive) : "))
			if(testResult==0):
				testResult=False
			else:
				testResult=True
			try:
				tx_hash = contract.functions.createRecord(idn,name,age,gender,testResult).transact({'from':account})
				tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
				print("\nSuccessfully altered the Record.\n")
				print("Transaction Hash:  ",web3.toHex(tx_hash))
				print(" ")
			except:
				print("The Transaction did not go through. Try again...")
				time.sleep(2)
		if(c==2):
			try:
				record = contract.functions.viewRecord().call({'from':account})
				if(record[0]==0):
					print("The Record does not exist, please create one.")
					continue
				print("ID:",record[0])
				print("Name:",record[1])
				print("Age:",record[2])
				print("Gender:",record[3])
				if(record[3]):
					print("Gender: Female")
				else:
					print("Gender: Male")
				if(record[4]):
					print("Test Result: Positive")
				else:
					print("Test Result: Negative")
				print(" ")
				time.sleep(2)
			except:
				print("The Transaction did not go through. Try again...")
				time.sleep(2)
		if(c==3):
			isDoctor = input("Enter the Account Address: ")
			try:
				res = contract.functions.doctor(isDoctor).call()
				if(res is True):
					print("\nYes, It's a Doctor's account.")
				else:
					print("\nNo, It's not a Doctor's account.")
				print(" ")
			except:
				print("The Transaction did not go through. Try again...")
				time.sleep(2)
		if(c==4):
			print("\nExiting...\n")
			time.sleep(1)
			sys.exit()

if(account==owner or contract.functions.doctor(account).call()==True):
    print("Welcome. You have admin privileges.\n")
    admin(account)
else:
    print("Welcome.\n")
    patient(account)
