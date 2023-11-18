"""
This python program includes both the simple and advance calculator.
Note from Lecturer: 'CW1 code will not be marked based on code quality and effeciency only based on functionalities'
"""

# global variables
inputs = [] # input values into the calculator
maxValue = int(2147483647) # assigning max value
minValue = int(-2147483648) # assigning min value
randomNumIndex = int(0)
randomNums = [1804289383, 846930886, 1681692777, 1714636915, 1957747793,\
     424238335, 719885386, 1649760492, 596516649, 1189641421, 1025202362,\
     1350490027, 783368690, 1102520059, 2044897763, 1967513926, 1365180540,\
     1540383426, 304089172, 1303455736, 35005211, 521595368, 1804289383]
withInHash = False

def appendWithMaxAndMin(value):
    """check for minimum and maximum"""
    if value > maxValue:
        inputs.append(maxValue)
    elif value < minValue:
        inputs.append(minValue)
    else:
        inputs.append(value)

# check if the input is a number
def isNum(a):
    try:
        int(a)
        return True
    except:
        return False

# octal to decimal function
def convertOctaltoDecimal(cmd):
    res = int(0)
    for i, val in enumerate(reversed(str(cmd))):
        if int(val) > 0:
            res=int(res) + (int(val)*int(8**i))
    return res

# processing indiviual command -> actual calculator
def process_individual_command(command):
    global withInHash
    if withInHash and command != '#':
        return
    if command == '#':
        withInHash = not withInHash
    if len(inputs) <= 1 and command in ['+', '-', '*', '/', '%', '^']:
        print ('Stack underflow.')
        return
    if command == 'r': # random number from the list
        global randomNumIndex
        if randomNumIndex==23:
            print ('Stack overflow.') 
            return
        appendWithMaxAndMin(randomNums[randomNumIndex])
        randomNumIndex+=1
        return
    if command == '+': # Addition
        num1 = inputs.pop()
        num2 = inputs.pop()
        num3 = int(num2) + int(num1)
        appendWithMaxAndMin(int(num3))
    elif not len(inputs) == 0 and command == '^' and int(inputs[len(inputs)-1])< 0:
        print('Negative power.')
    elif command == '-': # subtraction operator
        num1 = inputs.pop()
        num2 = inputs.pop()
        num3 = int(num2) - int(num1)
        appendWithMaxAndMin(int(num3))
    elif command == '*': # multipication operator
        num1 = inputs.pop()
        num2 = inputs.pop()
        num3 = int(num2) * int(num1)
        appendWithMaxAndMin(int(num3))
    elif command == '/': # division operator
        num1 = inputs.pop()
        num2 = inputs.pop()
        try: # check div by zero error
            num3 = int(num2) / int(num1)
            appendWithMaxAndMin(int(num3))
        except ZeroDivisionError:
            print("Divide by 0.")
    elif command == '%': # modulus operator
        num1 = inputs.pop()
        num2 = inputs.pop()
        num3 = int(num2) % int(num1)
        appendWithMaxAndMin(int(num3))
    elif command == '^': # power operator
        num1 = inputs.pop()
        num2 = inputs.pop()
        num3 = int(pow(int(num2), int(num1)))
        appendWithMaxAndMin(int(num3))
    elif command == 'd':
        if len(inputs) == 0:
            print(minValue)
        else:
            print(*inputs, sep='\n')
    elif len(inputs) >= 23:
        print ('Stack overflow.')
    elif command.startswith('0'):
        if len(command) >= 20:
            appendWithMaxAndMin(-1)
            return
        result = convertOctaltoDecimal(command)
        appendWithMaxAndMin(result)
    elif isNum(command):
        appendWithMaxAndMin(int(command))
    elif not command in ['+','-','*','/','%','^','d','r','=', '#'] and not isNum(command):
        print ('Unrecognised operator or operand "%s".' % command)
    elif command == '=':
        if len(inputs) == 0 :
            print ('Stack empty.')
        else:
            print(inputs[len(inputs)-1])

# splits commands into individual command to process
def process_command(command):
    all_commands_to_process = []
    for c in command.split( ):
        commands_to_process = []
        individual_command = ''
        isNumber = False
        for index, i in enumerate(c):
            if(i == "-" or isNum(i)):
                individual_command += str(i)
                isNumber = True
                continue
            if isNumber:
                commands_to_process.append(individual_command)
            isNumber = False
            individual_command = i
            commands_to_process.append(individual_command)
            individual_command = ''
        else:
            # append if ended in number
            if isNumber:
                isNumber=False
                commands_to_process.append(individual_command)
        # if commands contain numbers followed by operators, reorder for processing
        reordered_commands = []
        reordered_commands.extend(commands_to_process)
        for i, val in enumerate(commands_to_process):
            # skip every other element
            if i % 2 != 0:
                continue
            if isNum(val) and i + 2 < len(commands_to_process) and isNum        (commands_to_process[i+2]):
                reordered_commands[i+2], reordered_commands[i+1] = commands_to_process[i+1], commands_to_process[i+2]
        all_commands_to_process.extend(reordered_commands)
    for c in all_commands_to_process:
        process_individual_command(c)

#--------DO NOT Change Below--------#
#This is the entry point for the program.
#Do not edit the below
if __name__ == "__main__":
    while True:
        try:
            cmd = input()
            pc = process_command(cmd)
            if pc != None:
                print(str(pc))
        except:
            exit()
        #except Exception as e:
        #    print(e)
        #    exit()