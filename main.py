#### MODULES _______________________________________________________________
import pdb
import json
import datetime
import os
import sys

#### FUNCTION DEFINITIONS __________________________________________________

## FUNCTION 1 - Record Key <working>
def record_key(confirm):
    if confirm == 'F':
        return 'F'
    elif confirm == 'R':
        return 'R'
    else:
        print("Invalid Key...")
        confirm = input("Press F to commit, press R to re-enter : ")
        record_key(confirm)

## FUNCTION 2 - Record New Activity <working>
def new_activity():
    key = input("Enter Name of Activity : ")
    rate = input("Enter credit per unit with sign : ")
    unit = input("Enter unit : / ")
    print(key + " @ " + rate + " / " + unit)
    confirm = input("Press F to commit, press R to re-enter : ")
    record_result = record_key(confirm)
    if record_result == 'R':
        new_activity()
    else:
        ACTIVITIES[key]=[int(rate), '/ '+unit]
        with open(pwd +"/ACTIVITIES.txt", "w+") as act:
            act.write(str(ACTIVITIES))

## FUNCTION 3 - Add Exchange <depriciated; handled within main>
def exchange(option, reps, bal):
    key_value = list(ACTIVITIES.keys())[option]
    bal += (int(ACTIVITIES[key_value][0])*float(reps))
    return bal

## FUNCTION 4 - Check Balance
def balance_check():
    try:
        with open(pwd +"/balance.txt", "r+") as b:
            balance = float(b.read())
    except Exception as e:
        balance=0.0
        b= open(pwd +"/balance.txt", "w+")
        b.write(str(balance))
        b.close()
        print("Balance File Created") 
    return balance

## FUNCTION 5 - Delete Activity
def delete_activity():
    l = list(ACTIVITIES.keys())
    for item in l:
        print(str(l.index(item)) + " - " + item)
    chosenOption = int(input("Select option to delete : "))
    chosenKey = l[chosenOption]
    confirm = input("Press F to commit, press R to re-enter : ")
    record_result = record_key(confirm)
    if record_result == 'R':
        delete_activity()
    else:
        ACTIVITIES.pop(chosenKey)

## FUNCTION 6 - Show Records
def records():
    print("Developing option to list history\n")
    try:
        with open(pwd +"/activity_record.txt", "r+") as ar:
            lines = ar.readlines()
            print("Records are shown reverse-chronologically")
            n = input("Enter number of records to show (press enter for all) : ")
            if n != '':
                n = int(n)
                for i in range(1,n+1):
                    i=i*-1
                    print(lines[i])
            else:
                for i in range(1, len(lines)+1):
                    i=i*-1
                    print(lines[i])
    except Exception as e:
        ar = open(pwd +"/activity_record.txt", "w+")
        print("Created Activity Record")
        ar.close()

## FUNCTION 7 - Activity Record
def activity():
    BALANCE = balance_check()
    print("Choose activity from the following list : ")
    l = list(ACTIVITIES.keys())
    for item in l:
        print(str(l.index(item)) + " - " + item)
    # Required Params
    chosenOption = int(input("Enter the number : "))
    chosenKey = l[chosenOption]
    chosenRate = ACTIVITIES[chosenKey][0]
    chosenUnit = ACTIVITIES[chosenKey][1]
    chosenTime = datetime.datetime.now()
    print("Details:\n\
        Activity : " + chosenKey + "\n\
        Rate : " + str(chosenRate) +" "+ chosenUnit)
    chosenReps = float(input("\nEnter number of reps : "))
    change_in_balance = chosenRate*chosenReps
    print("\tOriginal Balance : " + str(BALANCE))
    print("\tExchange = " + str(change_in_balance))
    try:
        with open(pwd +"/activity_record.txt", "a+") as ar:
            ar.write(chosenTime.strftime("%d-%m-%y %H:%M:%S") + " | " + chosenKey + " @ " + str(chosenRate) +" "+ chosenUnit + " * " + str(chosenReps) + " = " + str(change_in_balance) + "\n")
    except Exception as e:
        ar = open(pwd +"/activity_record.txt", "w+")
        print("Created Historical Record")
        ar.write(chosenTime.strftime("%d-%m-%y %H:%M:%S") + " | " + chosenKey + " @ " + str(chosenRate) +" "+ chosenUnit + " * " + str(chosenReps) + " = " + str(change_in_balance) + "\n")
        ar.close()
    BALANCE = BALANCE + change_in_balance
    with open(pwd +"/balance.txt", "w+") as b:
        b.write(str(BALANCE))
        print("\tUpdating Ledger... \n\nNew balance is : " + str(BALANCE))

## FUNCTION 8 - Temporary Record
def temporary_activity():
    print("Enter the following details: \n")
    chosenKey = input("Activity Name : ")
    chosenValue = input("Total Credits Earned/Lost : ")
    chosenTime = datetime.datetime.now()
    BALANCE = balance_check()
    change_in_balance = int(chosenValue)
    print("\tOriginal Balance : " + str(BALANCE))
    print("\tExchange = " + str(change_in_balance))
    try:
        with open(pwd +"/activity_record.txt", "a+") as ar:
            ar.write(chosenTime.strftime("%d-%m-%y %H:%M:%S") + " | " + chosenKey + str(chosenValue) + " @ Unknown Rate and Unit"  + " = " + str(change_in_balance) + "\n")
    except Exception as e:
        ar = open(pwd +"/activity_record.txt", "w+")
        print("Created Historical Record")
        ar.write(chosenTime.strftime("%d-%m-%y %H:%M:%S") + " | " + chosenKey + str(chosenValue) + " @ Unknown Rate and Unit"  + " = " + str(change_in_balance) + "\n")
        ar.close()
    BALANCE = BALANCE + change_in_balance
    with open(pwd +"/balance.txt", "w+") as b:
        b.write(str(BALANCE))
        print("\tUpdated Ledger... \n\nNew balance is : " + str(BALANCE))



#### GLOBAL VARIABLES ______________________________________________________
cwf = sys.argv[0]
pwd = cwf.rsplit("/",1)[0]
print("The current Directory is : " + pwd)
print("All files will be created and used from above directory")
#pdb.set_trace()
ACTIVITIES={}
try:
    with open(pwd +"/ACTIVITIES.txt", "r+") as act:
        data = act.read()
        if data != '':
            ACTIVITIES = eval(data)
except Exception as e:
    act = open(pwd +"/ACTIVITIES.txt", "w+")
    act.close()
    print("Activities File created")

# print(str(ACTIVITIES))

BALANCE=balance_check()


### Try to elimiate this:
with open(pwd + "/activity_record.txt", "a+") as ar:
    print("activity_record.txt exists")

#### MAIN LOGIC ____________________________________________________________
#pdb.set_trace()

print("\n*****Welcome to Dopamine Exchange v0.0*****")
print("\
    This program acts as a 'wallet' for your daily activities - to try and find balance between high dopamine activities <like gaming, social media, etc.> and low dopamine activities <like work, reading, writing, exercise, etc.>.\n\
    This is a self sufficient version (hopefully), and all you need is python installed in the system.\n\
    Before you begin, please sit down and determine your highest and lowest dopamine activiies and set up an exchange within them\n\
    For Example : Gaming costs you 500 credits per hour, and 1 pushup earns you 10 credits\n\
    Here's to hoping you won't let the credit go negative\n\
    \n\
    Contact me at : alololy18@gmail.com or find me on GitHub\n")
print("Your Current Dopamine Balance is : \n***\t" + str(BALANCE) + " credits\t***\n")
if BALANCE < 0:
    print("***** WARNING : NEGATIVE BALANCE !!! *****")

while True:

    # Listing Options
    user_choice=input("\n\
Please select from the following menu \n\
    L : List existing activities \n\
    N : Add new activity to the list \n\
    A : Add new record / exchange \n\
    D : Delete Existing Record\n\
    R : Display Record of Activities\n\
    Q : Quit the program \n\
    B : Check Balance\n\
    T : A temporary record\n"
    )

    # Logic
    # Exit Program
    if user_choice == 'Q':
        break
    # Add Activity Record
    elif user_choice == 'A':
        activity()
    # Balance Enquiry
    elif user_choice == 'B':
        print(balance_check())
    # List of Activities
    elif user_choice == 'L':
        l = list(ACTIVITIES.keys())
        for item in l:
            print(str(l.index(item)) + " - " + item)
    # Add new activity to record
    elif user_choice == 'N':
        new_activity()
        print(ACTIVITIES)
    # Delect activity
    elif user_choice == 'D':
        delete_activity()
    # Show Record of activities / History
    elif user_choice == 'R':
        records()
    elif user_choice == 'T':
        temporary_activity()
    # Any other key
    else:
        print("Key Error")
        continue