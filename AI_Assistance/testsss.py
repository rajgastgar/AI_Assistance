import re
from nltk.tokenize import word_tokenize

tradeList = ['trade', 'book']
enquiryList = ['enquiry','details']

queryList= ['trade', 'book', 'the']

if __name__ == "__main__":
    tradeBookRegex = re.compile(r'\b\d{4}:(B|S):(\w{3}/\w{3}):(SPOT|FWD)\b')
    tradeEnquiryRegex = re.compile(r'\b\d{4}\b')
    analysisRegex = re.compile(r'(analyse) \b(ctr|ccy|cmrName|valueDate)\b')
    if(analysisRegex.match("analyse valueDae")):
        print("Matched")
        # print(re.split(':', "1234:B:INR/USD:FWD"))
    else:
        print("Not matched")