import sys
import csv

keywords = ["sweetgreen", "monty's", "target", "spectrum", "lao tao", "vons", "my thai", 
"green leaves", "yoga-urt", "lassens", "just ride", "rei", "chegg", "gegen", "cuscatleca",
"so cal gas", "check #"]

class Transaction():
    def __init__(self, date, amount, description): # transactionID, date, amount, description, category):
        # self.transactionID = transactionID
        self.date = date
        self.amount = float(amount)
        self.description = description
        # self.category = category.lower()

    def __str__(self):
        return "%s $%d %s" % (self.date, self.amount, self.description)
        # return "%d %s $%d %s %s" % (self.transactionID, self.date, self.amount, self.category, self.description)
        
    def __repr__(self):
        return "%s $%d %s" % (self.date, self.amount, self.description)
        # return "%d %s $%d %s %s" % (self.transactionID, self.date, self.amount, self.category, self.description)

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

    header = file.readline()
    header = header.split(',')

    # get the corresponding index values for each of the keyterms
    indicies.append(findIndex("Date", header))
    indicies.append(findIndex("Amount", header))
    indicies.append(findIndex("Description", header))
    # indicies.append(findIndex("Category", header)) # DONT NEED THIS

    # make tuples of each row
    with open(fileName, newline='') as f:
        reader = csv.reader(f)
        data = [tuple(row) for row in reader]

    # insert each row of data into a list of transactions
    for i, row in enumerate(data):
        if (i != 0):
            transactions.append( Transaction(row[indicies[0]], row[indicies[1]], row[indicies[2]]) )
    
    print(*transactions, sep='\n')

def filter():
    with open('dues.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        writer.writerow(["Date", "Description", "Amount"])

        # for each transaction
        for x in transactions:

            # if it contains one of the keywords that designates splitting
            if any(keyword.lower() in x.description.lower() for keyword in keywords):

                # if the amount is large enough to split 4 ways
                if abs(x.amount / 4) > 10:
                    writer.writerow([x.date, x.description, 0, abs(x.amount / 4)])

                # otherwise split 3 ways
                else:
                    writer.writerow([x.date, x.description, 0, abs(x.amount / 3)])
      

# list to hold all of the transactions in the csv file
transactions = []

def main():
    # list to hold file names
    fileNames = []

    # get file names from user as command-line arguments (skipping the first since it's the exec name)
    for arg in sys.argv[1:]:
        print(arg)
        fileNames.append(arg)

    # TESTING:
    # fileNames.append("ChaseCredit.csv")
    # fileNames.append("WPCUCredit.csv")
    # fileNames.append("WPCUDebit.csv")

    # for each file, open and parse its transactions
    for name in fileNames:
        parseFile(name)

    # analyze each transaction and export to new csv file
    filter()


if __name__ == '__main__': main()