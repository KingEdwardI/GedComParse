#!/usr/bin/python
# v. 0.3.5
"""
Strategy:
    loop through each record in the source file and make a list for every field in the source file where each index of each list pertains to a singular person/record in the source file.
    output JSON file by loop through all lists and return information formatted as JSON using string concatenation.
"""

# import requirements for things to work
import gedcom
    # don't forget to build / install gedcompy for parsing
    ## in the gedcompy folder, run `python setup.py build && python setup.py install`
from datetime import datetime
from pytime import pytime
import re
import argparse
import sys

#  # parse for arguments from the command line. input/output files or help.
#  # for command line use
#  #  parser = argparse.ArgumentParser(description="Parse a .gedcom file into .json for use in FamilyGenie")
#  #  parser.add_argument('-i','--input', help='Input file name', required=True)
#  #  parser.add_argument('-o','--output', help='Output file name', required=True)
#  #  args = parser.parse_args()

# for use with node
args = sys.argv[1]

def main():
    """
    the main function (this one) is the only function that runs when the program is called to run
    """
    ### parse gedcom file for information
    gedfile = gedcom.parse(args)

    ### file to write to 
    #  jsonfile = args.output
   
    ### runs all functions and writes to file
    writeToJSONfile(gedfile)
    
    ### test functions ###
    #  makeJSONobject(gedfile)

    #  getAllInfo(gedfile)
    #  getName(gedfile)
    #  getSexAtBirth(gedfile)
    #  getBirthPlace(gedfile)
    #  getBirthDate(gedfile)
    #  getDeathDate(gedfile)
    #  getDeathPlace(gedfile)
    #  getBirth(gedfile)
    #  getDeath(gedfile)
    #  parseTime(gedfile)
    #  print parseOutApprox(gedfile)
    
"""''''''''''''''''''''''''''''''''''''''''''''''''''''''"""
####################################################
####################################################
"""''''''''''''''''''''''''''''''''''''''''''''''''''''''"""

""" ########## STATIC functions for testing purposes ######### """

def getAllInfo(filename):
    """
    get all info unformatted
    """
    people = []
    # loop through each person in the file and add them to an list and return
    for person in filename.individuals:
        people.append(person)

    # loop through the the newly created list and print each record
    #  for person in people:
        #  print person

    # this is used for the length of the file as well
    return people

def getBirth(filename):
    """
    get all birth records and print them to console
    """
    birth = []
    # loop through each person in the file and add the birth record to a list and return
    for person in filename.individuals:
        birth.append(person.birth)
    
    # loop through the newly created list and print the new records
    for person in birth:
        print person

def getDeath(filename):
    """
    get all death records and print them to console
    """
    death = []
    # loop through the gedfile and add the death records to a list
    for person in filename.individuals:
        try:
            death.append(person.death.date)
        except AttributeError:
            death.append('No Death Record')
    
    # loop through the new list and print each record
    for person in death:
        print person

""" ########## BUILDER functions for JSON files ######### """

# note: AttributeError in this case means that there is no record of that type for that person

def getBirthPlace(filename):
    """
    get all of the birth place records from the GEDCOM file

    # loop through people from the input file, store their Birth Place records and return the list of records
    # if there is no Birth Place record (AttributeError), the list will store the value as null
    """
    birthPlace = []
    for person in filename.individuals:
        try:
            birthPlace.append('"birthPlace" : "' + person.birth.place + '"')
        except AttributeError:
            birthPlace.append('"birthPlace" : "null"')
    return birthPlace

def getBirthDate(filename):
    """
    get all of the birth date records from the GEDCOM file

    # store the Birth Date records and return a list
    """
    birthDate = []
    for person in filename.individuals:
        try:
            birthDate.append('"birthDate" : "' + person.birth.date + '"')
        except AttributeError:
            birthDate.append('"birthDate" : "null"')
    return birthDate

def getDeathPlace(filename):
    """
    get the death place from the GEDCOM file

    # store the Death Place records and return a list
    """
    deathPlace = []
    for person in filename.individuals:
        try:
            deathPlace.append('"deathPlace" : "' + person.death.place + '"')
        except AttributeError:
            deathPlace.append('"deathPlace" : "null"')
    return deathPlace

def getDeathDate(filename):
    """
    get the death date from the GEDCOM file

    # store the Death Date records and return a list
    """
    deathDate = []
    for person in filename.individuals:
        try:
            deathDate.append('"deathDate" : "' + person.death.date + '"')
        except AttributeError:
            deathDate.append('"deathDate" : "null"')
    return deathDate

def getSexAtBirth(filename):
    """
    get the gender of a person from the GEDCOM file

    # store the gender records and return a list
    """
    sexAtBirth = []
    for person in filename.individuals:
        try:
            sexAtBirth.append('"sexAtBirth" : "' + person.sex + '"')
        except AttributeError:
            sexAtBirth.append('"sexAtBirth" : "null"')
    return sexAtBirth

def getName(filename):
    """
    get the first and last name from the GEDCOM file

    # store the first and last names of each person in individual lists and return
    # gedcom format does not have a middle name available
    """
    firstName = []
    lastName = []
    for person in filename.individuals:
        firstname, lastname = person.name
        if lastname == None:
            lastname = ''
        if firstname == None:
            firstname = ''
        firstName.append('"fName" : "' + firstname + '"')
        lastName.append('"lName" : "' + lastname + '"')
    return firstName, lastName

def parseTime(filename):
    """
    formats timestamps into ISO time

    DATE FORMATTING KEY
    %y = two digit year : 97 | 78 | 65
    %Y = four digit year : 1997 | 1978 | 1842
    %m = one/two digit month : 01 | 3 | 11
    %b = (three letter) abbreviated month : Jan | feb | Dec
    %B = full month name : January | February | march
    %d = one/two digit day : 23 | 02 | 31

    %Y-%m-%d = 1995-06-28
    %m/%y/%d = 06/95/28
    %d %b %Y = 28 Jun 1995

    '\xe2\x80\x93' is a dash character (all 3 hex together represents a dash -- the full string)
    """

    # initilaze birthDate/deathDate lists
    birthDate = []
    deathDate = []

    # get the dates after the approximation strings have been removed
    bDate, dDate = parseOutApprox(filename)

    """
    dateFormat is used to loop through and check for what format the dates might be in
    if an error is thrown when running the file use the key from above and add the format to this list
    make sure that '%Y' is the last element of the list or everything breaks
    """
    dateFormat = ['%m/%d/%Y', '%m-%d-%Y', '%d-%m-%Y', '%d, %b %Y', '%d %B %Y', '%d %b %Y', '%d %B, %Y', '%b %d, %Y', '%B %d, %Y', '%B %d %Y', '%b %d %Y', '%B %Y', '%b %Y', '%m/%Y', '%Y']

    for bd in bDate:
        if '\xe2\x80\x93' in bd:
            # if there is a dash char in the date string that means the date in the file is between date1 & date2. get the avg of these dates and use that. set the ApproxDate to true
            date1 = int(bd[:4])
            date2 = int(bd[-4:])
            avgDate = (date1+date2)/2
            birthDate.append('"birthDate" : "' + str(datetime.strptime(str(avgDate), '%Y')) + '",\n"approxBirth" : "True"')
        elif '00000' in bd:
            # if the date is stored as 00000 that means that it did not exist while parsing through to remove the approximation strings
            birthDate.append('"birthDate" : "null",\n"approxBirth" : "False"')
        else:
            j = 0 # counter for error handling
            for i in dateFormat:
                # loop through the dateFarmats, try to parse the date - expect errors but if the counter goes beyond the length of dateFormat, then the date didn't match any known format strings.
                try:
                    if i == '%Y':
                        # datetime.strptime is a public lib -- see the README. if the date does not match the date format string being tested, this function will error and exception will be passed
                        birthDate.append('"birthDate" : "' + str(datetime.strptime(bd, i)) + '",\n"approxBirth" : "True"')
                        break
                    else:
                        birthDate.append('"birthDate" : "' + str(datetime.strptime(bd, i)) + '",\n"approxBirth" : "False"')
                        break
                except ValueError as e:
                    j += 1
                    pass
            if j > len(dateFormat) -1:
                # if we have looped through all of the known date formats and haven't found a match, we will end up here, and this will throw an error.
                birthDate.append('"birthDate" : "null",\n"approxBirth" : "False"')
                print Exception(bd, "birthDate - NEEDS MODIFICATION - check parseTime() and parseOutApprox()")
                

    for dd in dDate:
        if '\xe2\x80\x93' in dd:
            # if there is a dash char in the date string that means the date was input as between date1 & date2. get the avg of these dates and use that
            date1 = int(dd[:4])
            date2 = int(dd[-4:])
            avgDate = (date1+date2)/2
            deathDate.append('"deathDate" : "' + str(datetime.strptime(str(avgDate), '%Y')) + '",\n"approxDeath" : "True"')
        elif '00000' in dd:
            # if the date is stored as 00000 that means that it was not present while parsing through to remove the approximation strings
            deathDate.append('"deathDate" : "null",\n"approxDeath" : "False"')
        else:
            j = 0
            for i in dateFormat:
                try:
                    if i == '%Y':
                        # datetime.strptime is a public lib -- see the README. if the date does not match the date format string being tested, this function will error and exception will be passed
                        deathDate.append('"deathDate" : "' + str(datetime.strptime(dd, i)) + '",\n"approxDeath" : "True"')
                        break
                    else:
                        deathDate.append('"deathDate" : "' + str(datetime.strptime(dd, i)) + '",\n"approxDeath" : "False"')
                        break
                except ValueError as e:
                    j += 1
                    pass
            if j > len(dateFormat) -1:
                # if we have looped through all of the known date formats and haven't found a match, we will end up here, and this will throw an error.
                deathDate.append('"deathDate" : "null",\n"approxDeath" : "False"')
                print Exception(dd, "deathDate - NEEDS MODIFICATION - check parseTime() and parseOutApprox()")

    return birthDate, deathDate

def parseOutApprox(filename):
    """
    remove approximation strings from dates.
    also fix four letter month names or make any other modifications to dates
    TODO: throw an error if there is an unknown approx string
    """

    # first get all of the data from the input file
    # if there isn't one put 00000 as a placeholder to be replaced later
    bDate = []
    dDate = []

    for person in filename.individuals:
        try:
            bDate.append(person.birth.date)
        except AttributeError:
            bDate.append('00000')
   
    for person in filename.individuals:
        try:
            dDate.append(person.death.date)
        except AttributeError:
            dDate.append('00000')

    """
    Approximation RegExp to be removed 
    """
    abt = re.compile('abt\.? ', re.IGNORECASE) # matches 'abt', possibly followed by a '.'
    bet = re.compile('bet\.? ', re.I) # matche 'bet', possibly followed by a '.'
    bef = re.compile('bef\.? ', re.I) # matches 'bef', possibly followed by a '.'
    sep = re.compile('sept', re.I) # matches 'sept'
    be = re.compile('before ', re.I) # matches 'about'
    a = re.compile('about ', re.I) # matches 'about'
    e = re.compile('early ', re.I) # matches 'early'
    s = re.compile('(?<=\d)s') # matches an 's' preceded by a number - 1800(s)
    p = re.compile('\.(?= \d)') # matches a '.' followed by a space and a number - oct. 1995
    q = re.compile('\?') # matches a '?'

    # Once the records are stored locally parse out the approximation strings
    # loop through the records and the object with the replacements to find any and all replacements

    # initialize new birthdate/deathdate list
    newbDate = []
    newdDate = []


    # loop through birth dates
    for b in bDate:
        b = abt.sub('', b)
        b = bet.sub('', b)
        b = bef.sub('', b)
        b = sep.sub('sep', b) # not removing approx -- changing the september month abbrev. sept is not a parseable month abbrev
        b = be.sub('', b)
        b = a.sub('', b)
        b = e.sub('', b)
        b = s.sub('', b)
        b = p.sub('', b)
        b = q.sub('', b)
        
        # append parsed birthdate to new birth date list
        newbDate.append(b)

    # loop through death dates
    for d in dDate:
        d = abt.sub('', d)
        d = bet.sub('', d)
        d = bef.sub('', d)
        d = sep.sub('sep', d) # not removing approx -- changing the september month abbrev. sept is not a parseable month abbrev
        d = be.sub('', d)
        d = a.sub('', d)
        d = e.sub('', d)
        d = s.sub('', d)
        d = p.sub('', d)
        d = q.sub('', d)

        # append parsed deathdate to new death date list
        newdDate.append(d)

    return newbDate, newdDate

def makeJSONobject(filename):
    """
    get information from the file, print and structure it in JSON
    run all of the previous functions to get the information - stored as lists
    loop through the lists and save them locally and return to be written to a file 
    """

    length = getAllInfo(filename)
    firstName, lastName = getName(filename)
    sexAtBirth = getSexAtBirth(filename)
    birthDate, deathDate = parseTime(filename)
    birthPlace = getBirthPlace(filename)
    deathPlace = getDeathPlace(filename)

    length = len(length)
    json = ''
    json += '[ \n'
    for i in range(length):
        json += '{ \n'
        json += firstName[i] + ',\n'
        json += lastName[i] + ',\n'
        json += sexAtBirth[i] + ',\n'
        json += birthDate[i] + ',\n'
        json += birthPlace[i] + ',\n'
        json += deathDate [i] + ',\n'
        json += deathPlace[i] + '\n'
        if i == (length - 1):
            json += '}\n'
        else:
            json += '},\n'
    json += ']'
    return json
    
    """ printing for testing purposes """
    #  print "["
    #  for i in range(length):
        #  print "{"
        #  print firstName[i]
        #  print lastName[i]
        #  print sexAtBirth[i]
        #  print birthDate[i]
        #  print birthPlace[i]
        #  print deathDate[i]
        #  print deathPlace[i]
        #  if i == (length - 1):
            #  print "}"
        #  else:
            #  print "},"
    #  print "]"


def writeToJSONfile(filename):
    """
    write the created json object to the output file and save it
    """
    json = makeJSONobject(filename)
    f = open(sys.argv[2], "w") # creat/open the output file
    f.write(json)
    f.close() # save

# run the main function
if __name__ == "__main__":
    main()
