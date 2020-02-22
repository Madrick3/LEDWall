def PropDivisors(i):
    properDivisors = [1]
    for j in range(int(float(i)**(1/2))):
        j+=1
        #print(i, j)
        if(i%j==0 and j > 1):
            properDivisors.append(j)
            k = int(i/j)
            if(j != k):
                properDivisors.append(int(i/j))
    #print("properdivs of ", i, "are:", properDivisors)
    return properDivisors
    
""" 
A perfect number is a number for which the sum of its proper divisors is exactly equal to the number. For example, the sum of the proper divisors of 28 would be 1 + 2 + 4 + 7 + 14 = 28, which means that 28 is a perfect number.

A number n is called deficient if the sum of its proper divisors is less than n and it is called abundant if this sum exceeds n.As 12 is the smallest abundant number, 1 + 2 + 3 + 4 + 6 = 16, the smallest number that can be written as the sum of two abundant numbers is 24. By mathematical analysis, it can be shown that all integers greater than 28123 can be written as the sum of two abundant numbers. However, this upper limit cannot be reduced any further by analysis even though it is known that the greatest number that cannot be expressed as the sum of two abundant numbers is less than this limit. 

Find the sum of all the positive integers which cannot be written as the sum of two abundant numbers.
 """
def isAbundant(i):
        pd = PropDivisors(i) #retreive a list of all proper divisors 
        sumpd = sum(pd)
        if(sumpd > i):
                return True
        else:
                return False

def isPerfect(i):
        pd = PropDivisors(i) #retreive a list of all proper divisors 
        sumpd = sum(pd)
        if(sumpd == i):
                return True
        else:
                return False

abundances = [0] * 28123
sumAbunds = [0] * 28123
count = 0
for i in range(28123):
        i+=1 #start at 1
        if(isAbundant(i)):
                print(i, " is an abundant number")
                abundances[i] +=1
                count+=1
        elif(isPerfect(i)):
                print(i, "is a perfect number")
                count+=1
        else:
                print(i, " is a deficient number")
                count+=1

for i in range(28123):
        if abundances[i] > 0:
                k = 0
                j = i
                while j < 28123 and k < 28123:
                        if abundances[j] > 0:
                                k = i + j
                                if(k < 28123):
                                        sumAbunds[k] += 1
                                        print(k, " can be obtained by adding abundant numbers: ", i, " and ", j)
                        j+=1
        else:
                print("skipping ", i, " since it is not abundant!")

finalAnswer = 0
for i in range(28123):
        if sumAbunds[i] == 0:
                finalAnswer += i
                #print("adding: ", finalAnswer, " from ", sumAbunds[i])

print(finalAnswer)
#This works! 4179871
"""
#print("abundant nmbers:  ", abundances)

sumofabundances = []
for i in range(count):
    j = i
    a = abundances[i]
    while(i+j<count):
        b = abundances[j]
        c = a + b
        sumofabundances.append(c)
        j+=1

print("sums:  ", sumofabundances)
"""