
def polynomialEval(inString):

    inputs =  inString.split(";")
    params1 = inputs[0]
    params1 = params1.split(" ")

    params2 = inputs[1]
    params2 = int(params2)

    length = len(params1)

    sum = 0
    for i in range(length):
        sum += int(params1[i]) * (params2 **(length - i - 1))

    return str(sum)

print(polynomialEval("1 2 3; 4"))
print(polynomialEval("1 1 1 1; 2"))
print(polynomialEval("10; 5"))
print(polynomialEval("5 4; 20"))