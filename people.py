import io
from sqlalchemy import func
import numpy as np
from array import *
from math import log10, log
import random

#generate a dict of values corresponding to the attributes of a Person
def generate_person_dict(data, state, district, mpce):
    person = generate_person(data, state, district, mpce)
    return person.to_dict()

def generate_person(data, state, district, mpce):
    #This is where math and statistics comes in
    money = generate_income(mpce, district.classification) - generate_expense_log(mpce, district.classification)
    gender = generate_gender()
    age = generate_age(mpce, district.classification)
    #Just a number in a uniform distribution from 0-1
    #Obviously needs to be changed later
    eye_health = random.random()
    cardio = random.random()
    classification = district.classification
    person = io.Person(money, gender, age, eye_health, cardio, district.name,
            state.name, classification)
    return person

#Note that this is merely a demonstration of how to randomly generate money
# for a Person. This will be rewritten later!
def randomize_money(mpce):
    #generate random value between 0 and double the MPCE average
    #The mean is therefore the MPCE average
    return random.random()*mpce.mpce_average*2

######################## below by RieK #########################

def exp_percentile(mpce, class_type):
    #return mpce.get_d_all(add_zero = False)
    return data.get_mpce_by_state_name(mpce, class_type).get_d_all(add_zero = False)

def generate_expense(mpce, class_type):
    # Currently not in use
    # For testing, only generating 100,000th of population
    pop = 0.1 * (data.pop_by_state(mpce, "rural"))/100000
    listPercentile = exp_percentile(mpce, class_type)
    expenseList=[]
    for i in xrange(len(li  stPercentile)-1):
        genUniform = np.random.uniform(listPercentile[i], listPercentile[i+1],
                pop)
        expenseList.append(genUniform)
    return expenseList

def generate_expense_log(mpce, class_type):
    listPercentile = exp_percentile(mpce, class_type)
    logPercentile = []
    # http://stackoverflow.com/questions/4561113/python-list-conversion
    logPercentile[:] = [log(x) for x in listPercentile]
    return np.random.lognormal(mean=np.mean(logPercentile), sigma=np.std(logPercentile))

def generate_income(mpce, class_type):
    # get meanMPCE and % of classMPCE in meanMPCE
    ruralMPCE = data.meanMpce_by_state(mpce, "rural")
    urbanMPCE = data.meanMpce_by_state(mpce, "urban")
    meanMPCE = (ruralMPCE + urbanMPCE)/2
    classMPCE = data.meanMpce_by_state(mpce, class_type)
    classPercent = float(classMPCE) / meanMPCE
    # multiply GSP (in Rs.10M) by % to get modified GSP for given class
    meanGSP = data.get_gsp(mpce, "total").gsp * 10000000
    classGSP = int(classPercent * meanGSP)
    classPop = data.pop_by_state(mpce, class_type)
    # get mean
    meanIncome_person = classGSP / classPop / 10000
    # get sd (I manually calculated from raw data, and made adj,
    # calculation refer to R3.r file: "2. Distribution of Income")
    poorMean = 17097.05 - 2000
    richMean = 171282.9 - 7000
    if classGSP < (60000 * 10000000):
        sdIncome_person = poorMean * 10000000 / data.pop_by_state(mpce, "total")/ 10000
    else:
        sdIncome_person = richMean * 10000000 / data.pop_by_state(mpce, "total")/ 10000
    return np.random.lognormal(log(meanIncome_person),log(sdIncome_person)) * 10000 / 12

def generate_gender():
    # mean prob of M = 0.5117376, F = 0.4882624
    # (I manually calculated from raw data,
    # calculation refer to R3.r file: "3. Distribution of Age")
    if random.random() >= 0.4882624:
        return "M"
    else:
        return "F"

def generate_age(mpce, class_type):
    # age distribution at last tab "17.Population by Age-Group"
    # http://rural.nic.in/sites/downloads/IRDR/1.%20Demographic%20Profile.xls
    # does this need to go to database? or shall we use the average
    # but this needs to have the total number: pop ***!!!
    # my current idea idea is to simulate age dist and bootstrap
    if class_type == "rural":
        ageDistList = [19.1, 20.7, 33.1, 18.8, 7.6, 0.8] / 100
    elif class_type == "urban":
        ageDistList = [16.4, 18.3, 35.9, 21.5, 7.3, 0.7] / 100
    pop = data.pop_by_state(mpce, class_type)
    to9 = np.random.uniform(1,9,pop * (ageDistList[0]/100.0))
    to19 = np.random.uniform(10,19,pop * (ageDistList[1]/100.0))
    to39 = np.random.uniform(20,39,pop * (ageDistList[2]/100.0))
    to59 = np.random.uniform(40,59,pop * (ageDistList[3]/100.0))
    to79 = np.random.uniform(60,79,pop * (ageDistList[4]/100.0))
    to102 = np.random.uniform(80,102,pop * (ageDistList[5]/100.0))
    ageList = np.concatenate((to9,to19,to39,to59,to79,to102), axis=0)
    return random.sample(ageList,1)

def generate_life_exp(gender, age):
    # life-expectancy data from 
    # http://www.worldlifeexpectancy.com/country-health-profile/india
    # we could make database or make dicitonary
    MaleLifeExp = {"0":63.8, "5":62.7, "10":58.1, "15":53.4, "20":52.9, "25":44.2, "30":39.7, "35":35.3, "40":31.1, "45":26.9, "50":23, "55":19.3, "60":15.7, "65":12.7, "70":10.2, "75":8.3, "80":6.7,"85":5.2, "90":3.9, "95":2.8, "100":2.0}
    FemaleLifeExp = {"0":67.3, "5":66.8, "10":62.2, "15":57.5, "20":52.9, "25":48.4, "30":43.8, "35":39.2, "40":34.7, "45":30.2, "50":25.8, "55":25.8, "60":17.7, "65":14.3, "70":11.3, "75":9.0, "80":7.0,"85":5.3, "90":3.9, "95":2.8, "100":2.0}

    if gender == 'F':
        return FemaleLifeExp(age)
    else:
        return MaleLifeExp(age)

def generate_eye_health(age):
   
    return random.random()

def generate_2ndHealth(mpce, class_type, gender, age):
    return random.random()

def generate_age(mpce, class_type):
    # age distribution at last tab "17.Population by Age-Group"
    # http://rural.nic.in/sites/downloads/IRDR/1.%20Demographic%20Profile.xls
    # does this need to go to database? or shall we use the average
    # but this needs to have the total number: pop ***!!!
    # my current idea idea is to simulate age dist and bootstrap
    if class_type == "rural":
        ageDistList = [19.1, 20.7, 33.1, 18.8, 7.6, 0.8] / 100
    elif class_type == "urban":
        ageDistList = [16.4, 18.3, 35.9, 21.5, 7.3, 0.7]
    pop = data.pop_by_state(mpce, class_type)
    to9 = np.random.uniform(1,9,pop * (ageDistList[0]/100.0))
    to19 = np.random.uniform(10,19,pop * (ageDistList[1]/100.0))
    to39 = np.random.uniform(20,39,pop * (ageDistList[2]/100.0))
    to59 = np.random.uniform(40,59,pop * (ageDistList[3]/100.0))
    to79 = np.random.uniform(60,79,pop * (ageDistList[4]/100.0))
    to102 = np.random.uniform(80,102,pop * (ageDistList[5]/100.0))
    ageList = np.concatenate((to9,to19,to39,to59,to79,to102), axis=0)
    return random.sample(ageList,1)

if __name__ == '__main__':
    data = io.Database()
    test_state_name = "Tamil Nadu"
    test_classif = "urban"
    mpce = data.get_mpce_by_state_name(test_state_name, test_classif).state
    print mpce, test_classif
    print 'pop_by_state', data.pop_by_state(mpce, test_classif)
    print 'meanMpce_by_state', data.meanMpce_by_state(mpce, test_classif)
    print 'exp_percentile', exp_percentile(mpce, test_classif)
    print 'Income: urban', generate_income(mpce, test_classif)
    print 'Income: rural', generate_income(mpce, test_classif)
    print 'Gender:', generate_gender()
    print 'Age:', generate_age(mpce, test_classif)
