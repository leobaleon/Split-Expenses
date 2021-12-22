import sys
import csv
import glob

# list to hold all of the transactions in the csv file
transactions = []

class Transaction():
    def __init__(self, date, amount, description): 
        self.date = date
        self.amount = float(amount)
        self.description = description
        self.include_transaction = False

    def __str__(self):
        return "%s %s $%d" % (self.date, self.description, self.amount)
        
    def __repr__(self):
        return "%s $%d %s" % (self.date, self.amount, self.description)

    def include(self, decision):
        self.include_transaction = decision

    def get_record(self):
        return self.date, self.description, self.amount, self.include_transaction

# simple helper function meant to aid in the reading and parsing of the csv file
# this function accepts a substring as string and a list as a list of strings
# this function will find the first occurrence of the substring in the list
# parameter and return the index in which it was found 
def findIndex(substring, list):
    for index, string in enumerate(list):
        if substring in string:
              return index

def parseFile(fileName):
    indicies = []

    # open file with read access
    file = open(fileName, "r")

    # read the header and tokenize the terms
    header = file.readline()
    header = header.split(',')

    # get the corresponding index values for each of the keyterms
    indicies.append(findIndex("Date", header))
    indicies.append(findIndex("Amount", header))
    indicies.append(findIndex("Description", header))

    # make tuples of each row
    with open(fileName, newline='') as f:
        reader = csv.reader(f)
        data = [tuple(row) for row in reader]

    # insert each row of data into a list of transactions
    for i, row in enumerate(data):
        if (i != 0):
            transactions.append( Transaction(row[indicies[0]], row[indicies[1]], row[indicies[2]]) )
    
    # print(*transactions, sep='\n')

def filter():
    print("For each of the following transactions, enter y or n to include each transaction or not.\n")
    print("Date\t", "Description\t\t", "Amount")

    # for each transaction
    for x in transactions:
        # print each transaction and ask user for a decision
        print(x, end='\t')
        decision = input()

        # send bool with user decision to each transaction's mutator to decide whether or not 
        # to include the current transaction in the resulting csv file
        x.include(True if decision.upper() == 'Y' else False)

def write():
    with open('dues.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    
        for x in transactions:
            # call each transaction's accessor to pull the following info:
            # 0: date
            # 1: description 
            # 2: amount 
            # 3: decision
            row = x.get_record()

            # if the user decided to include the current transaction,
            # write it into the resultant csv file, and ensure amount is positive
            if (row[3]):
                writer.writerow([row[0], row[1], abs(row[2])])

def no_files_found():
    print("============================================================================================================")
    print("No csv files were found..!")
    print("Place your csv files in the same folder that this program is currently in and try running the program again.")
    print("============================================================================================================")

def main():
    # list to hold file names
    fileNames = glob.glob("*.csv")
    fileNames.remove('dues.csv')

    if not fileNames:
        no_files_found()
    else:
        # for each file, open and parse its transactions
        for name in fileNames:
            parseFile(name)

        # analyze each transaction and export to new csv file
        filter()

        # use the transactions info to create a csv for easy copy pasting
        write()

        print("Dues.csv has been successfully created!")


if __name__ == '__main__': main()