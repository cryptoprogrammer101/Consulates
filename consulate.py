import os
from bs4 import *
import csv

# EXCEPTIONS: BRAZIL
# NO EMAIL

# create list of consulates
lst = []

# retrieve information       
def retrieve_info(soup):
    
    # create empty fields
    country = type = street = city = phone = website = head = ""
    
    # retrieve info
    for h1 in soup.find_all("h1"):
        # retrieve text
        text = retrieve_text(h1)
        # create substring to remove
        substring = " in boston, united states"
        # see if header contains substring
        if substring in text:
            # remove substring
            info = text.split(substring)[0]
            # check type of consulate
            type = check_type(info)
            # remove type
            country = info.split(type + " of ")[1]
            break
    
    # retrieve info
    for li in soup.find_all("li"):
        # retrieve text
        text = retrieve_text(li)
        # create substring for address
        substring = ", ma "
        # check if text contains address
        if substring in text:
            # remove substring
            info = text.split(substring)[0]
            # remove comma
            info = info.split(",")[0]
            # get city
            city = get_city(info)
            # get street
            street = info
            # check if street contains city
            if city in info:
                # remove city
                street = info.split(city)[0]
                
            break
            
    # retrieve info
    for i, li in enumerate(soup.find_all("li")):
        # retrieve text
        text = retrieve_text(li)
        # create substring for phone
        substring = "(+1) "
        # check if text contains phone and not fax
        if substring in text:
            # remove substring
            info = text.split(substring)[1]
            # format
            phone = info.split("/")[0]
            # format
            phone = format_phone(phone, [" ", "(", ")", "-", "emergency"])
            break
    
    # retrieve info
    for li in soup.find_all("li"):
        # retrieve text
        text = retrieve_text(li)
        # split url
        s = text.split()
        # create substring for url
        substring = "."
        # create another substring for url
        substring2 = "bos"
        # check if url contains period and boston & is proper length
        if substring in text and substring2 in text and len(s) == 1 and len(s[0]) > 1:
            website = text
            break
            
    # retrieve info
    for li in soup.find_all("li"):
        # retrieve text
        text = retrieve_text(li)
        # retrieve name of head
        test_head = retrieve_name(text, ["consul", "consul general", "trade representative"])
        
        # if head is not empty
        if len(test_head) > 0:
            # update head
            head = test_head
            break
    
    row = [country, type, street, city, "", phone, website, head]
    lst.append(row)

# format text
def retrieve_text(element):
    # retrieve text
    text = element.text
    # make lowercase
    text = text.lower()
    # format
    text = text.strip()
    # return text
    return text
    
# retrieve name of head
def retrieve_name(text, substrings):
    
    # define empty head
    head = ""
    
    # loop through substrings
    for s in substrings:
        # if job title is at end
        if s in text and text.index(s) + len(s) == len(text):
            # format
            head = text.split(",")[0]
            # if head exists
            if len(head) > 0:
                # return head
                return head
                
                
    # return nothing
    return ""
    

# remove titles for people
def remove_title(name, titles):

    # loop through each title
    for t in titles:
        if t + " " in name:
            # split by title
            s = name.split(t + " ")
            # remove title
            name = "".join(s)

    # return name
    return name

# replace "" with N/A & capitalize words
def format_lst():
                
    # start at first row
    i = 0
    # loop through rows
    while i < len(lst):
        # retrieve row
        row = lst[i]
        # retrieve head
        head = lst[i][len(row) - 1]
        
        # remove personal titles
        lst[i][len(row) - 1] = remove_title(head, ["mr", "mrs", "ms", "dr"])
            
        # increment row
        i += 1
    
    # loop through rows
    for i, r in enumerate(lst):
        # loop through columns
        for j, c in enumerate(r):
            # if column is not phone or website
            if j != 5 and j != 6:
                # split column
                split_col = c.split()
                # create new column
                new_col = []
                # remove first word if "the"
                if len(split_col) > 0 and split_col[0] == "the":
                    # remove first word
                    split_col.remove(split_col[0])
                # loop through split words
                for w in split_col:
                    # capitalize words
                    new_col.append(w.capitalize())
                # combine words to form column
                join_col = " ".join(new_col)
                # update lst
                lst[i][j] = join_col
    
    # loop through rows
    for i, r in enumerate(lst):
        # loop through columns
        for j, c in enumerate(r):
            # if the column is empty
            if c == "":
                # set column to N/A
                lst[i][j] = "N/A"
            
                
    # sort list
    lst.sort()
                
    
# remove characters from phone number    
def format_phone(phone, chars):
    # loop through characters
    for c in chars:
        # split phone number
        s = phone.split(c)
        phone = "".join(s)
    
    phone = "(+1) " + phone[:3] + "-" + phone[3:6] + "-" + phone[6:]
        
    return phone
    
# retrieve the city    
def get_city(info):
    
    # list of cities
    cities = ["east boston", "andover", "springfield", "weston", "newton", "cambridge", "lowell", "needham", "chelsea", "brighton", "belmont"]
    
    # loop through cities
    for city in cities:
        # check if this is city and if city is at end
        if city in info and info.index(city) + len(city) == len(info):
            # return city
            return city
    
    # default, return boston
    return "boston"
    
    
# check the type of consulate
def check_type(info):
    
    # define types of consulates
    types = ["consulate general", "consulate", "consul"]
    
    # loop through types
    for type in types:
        # try
        try:
            # see if type is in the header
            test = info.split(type + " of ")[1]
            # return the type
            return type
        
        # otherwise
        except:
            # keep going
            pass
    
    return "trade office"

os.system("clear")

# for every HTML file
for file in os.listdir(os.fsencode("ConsulateList/").decode()):
    # retrieve filename
    fname = os.fsdecode(file)
    # open file
    with open("ConsulateList/%s" % fname) as fp:
        # parse HTML
        soup = BeautifulSoup(fp, 'html.parser')
        
        # retrieve info
        retrieve_info(soup)

# format lst
format_lst()    

# define field names
field_names = ["Country", "Type", "Street", "City", "Email", "Phone", "Website", "Head"]

print(field_names, "\n")

for r in lst:
    print(r)

# create csv file
with open("Consulates.csv", mode="w") as file:
    # create csv writer
    writer = csv.DictWriter(file, fieldnames=field_names)
    # write header
    writer.writeheader()
    # loop through lst
    for r in lst:
        # create dictionary
        consulate_dict = {}
        # loop through columns
        for i, val in enumerate(r):
            # retrieve key
            key = field_names[i]
            # update dictionary
            consulate_dict[key] = val
        # write to csv
        writer.writerow(consulate_dict)