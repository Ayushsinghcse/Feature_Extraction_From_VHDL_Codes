import re
with open ("Datapath VHDL_with portmap.txt", 'r') as file:
    content = file.readlines()

# def entity_Presence(lst):
#     look = False
#     unwanted = [',',';','(', ')', ':']
#     for line in content:
#         if 'entity' in line:
#             look=True 
#         if look:


r"mux(?:[1-9]|1[0-9]|20)_(?:2|4|8|16|32)_to_(?:1|2|4|8|16)"
def muxCount(type):
    muxCnt = 0
    pattern = rf"component mux(?:[0-9]|1[0-9]|20)?_{type}_to_1"
    for line in content:
        if re.search(pattern, line):
            print(line)
            muxCnt+=1
        
    return muxCnt

def deMuxCount(type):
    deMuxCnt = 0
    pattern = rf"component ([d|D]emux)(?:[0-9]|1[0-9]|20)?_1_to_{type}"
    for line in content:
        if re.search(pattern, line):
            print(line)
            deMuxCnt+=1
        
    return deMuxCnt

def notGateCount():
    pattern = r"component ([N|n]ot)(?:[1-9]|1[0-9]|2[0-5])\b"
    checkNot, checkReg = False
    compDefnList = {}
    itr = 0
    container = {'input':[], 'output':[]}
    defn = ""
    for line in content:
        if re.search(pattern, line) and not checkNot:
            checkNot=True
            res = line.split(" ")
            defn += res[1]
        if checkNot and re.search(r'end component', line):
            itr = 0
            compDefnList[defn]=container
            container={'input':[], 'output':[]}
            defn = ""
            checkNot=False
        if checkNot:
            res = re.split(r'[;:,]', line)
            for i in range(res):
                if res[i]=='in':
                    container['input'].append(itr)
                    itr+=1
                if res[i]=='out':
                    container['output'].append(itr)
                    itr+=1
    notIp,notOp = [],[]
    for key,value in compDefnList:
        notIp.extend(i for i in value['input'])
        notOp.extend(i for i in value['output'])
    notChain = False
    for i in notIp:
        if i in notOp:
            notChain=True 
    print('not chain present' if notChain else '')
    return len(compDefnList),notChain

def counterCount():
    counterCnt = 0
    pattern = r"component counter(?:[1-9]|1[0-9]|2[0-5])\b"
    for line in content:
        if re.search(pattern, line):
            counterCnt+=1
    return counterCnt

def comparaterCount():
    comperatorCnt = 0
    pattern = r"component comparator(?:[1-9]|1[0-9]|2[0-5])\b"
    for line in content:
        if re.search(pattern, line):
            comparaterCount+=1
    if comperatorCnt>=1:
        print("check for extra register ")
    else:
        print("dont check for extra register ")
    return comperatorCnt, True if comperatorCnt else False

def triStateBuffer():
    TSBCnt = 0
    pattern = r"component  tri-state buffer(?:[1-9]|1[0-9]|2[0-5])\b"
    for line in content:
        if re.search(pattern, line):
            TSBCnt+=1
    return TSBCnt

# compCount, presence = comparaterCount()
def extraRegister(presence):
    # presence=True
    regOutput = []
    regDefnList = {}
    if presence:
        pattern = r"component comparator(?:[1-9]|1[0-9]|2[0-5])\b"
        regPattern = r"component register[A-Z]{1,2}"
        checkComp, checkReg = False, False
        extraReg = 0
        compDefnList = {}
        itr = 0
        container = {'input':[], 'output':[]}
        defn = ""
        check=False
        for line in content:
            if re.search(pattern, line) and not checkComp:
                checkComp=True
                res = line.split(" ")
                defn += res[1]
            if checkComp and re.search(r'end component', line):
                itr = 0
                compDefnList[defn]=container
                container={'input':[], 'output':[]}
                defn = ""
                checkComp=False
            if checkComp:
                res = re.split(r'[;:,]', line)
                for i in range(res):
                    if res[i]=='in':
                        container['input'].append(itr)
                        itr+=1
                    if res[i]=='out':
                        container['output'].append(itr)
                        itr+=1
            if re.search(regPattern, line) and not checkReg:
                checkReg=True 
                res=line.split()
                defn+=res[1]
            if checkReg and re.search(r'end component', line):
                itr = 0
                regDefnList[defn]=container
                container={'input':[], 'output':[]}
                defn = ""
                checkReg=False
            if checkReg:
                res = re.split(r'[;:, ]', line)
                if '' in res:
                    res.remove('')
                for i in range(len(res)):
                    if res[i]=='in':
                        if 'input' not in container:
                            container['input']=[]
                        container['input'].append(itr)
                        itr+=1
                    if res[i]=='out':
                        container['output'].append(itr)
                        itr+=1


        for line in content:
            if 'begin' in line:
                check=True
            if check and re.search(r"register[A-Z]{1,2}", line):
                print(line)
                res = re.split(r'[: ]', line)
                if '' in res:
                    res.remove('') 
                defn=res[1]
                match = re.search(r"\((.*?)\)", line)
                inside_brackets = match.group(1)
                elements = [elem.strip() for elem in inside_brackets.split(",")]
                regOutput.extend([elements[i] for i in regDefnList[defn]['output']])
        print(regOutput)
        check = False
        for line in content:
            if 'begin' in line:
                check=True
            if check and re.search(r'comparator(?:[1-9]|1[0-9]|2[0-5])\b', line):
                res.split = re.split(r'[: ]',line)
                if '' in res:
                    res.remove('') 
                defn=res[1]
                match = re.search(r"\((.*?)\)", line)
                inside_brackets = match.group(1)
                elements = [elem.strip() for elem in inside_brackets.split(",")]
                print(compDefnList[defn]['input'])
                for i in compDefnList[defn]['input']:
                    if elements[i] in regOutput:
                        extraReg+=1
        if extraReg:
            print('extra register present!')
        return extraReg, regOutput, len(regDefnList)
    return 0,regOutput, len(regDefnList)

def muxToMux():
    pattern = r"component (?<!de)mux(?:[0-9]|1[0-9]|20)?_(?:2|4|8|16|32)_to_(?:1)"
    checkMux = False
    regDefnList={}
    container={'output':[],'input':[]}
    defn=""
    itr=0
    for line in content:
        if re.search(pattern, line) and not checkMux:
            checkMux=True
            res = line.split(" ")
            defn += res[1]
        if checkMux and re.search(r'end component', line):
            # print(line)
            itr = 0
            regDefnList[defn]=container
            container={'output':[],'input':[]}
            defn = ""
            checkMux=False
        if checkMux:
            res = re.split(r'[;:, ]', line)
            res = [item for item in res if item]
            # print(res)
            for i in range(len(res)):
                if res[i]=='in':
                    container['input'].append(itr)
                    itr+=1
                if res[i]=='out':
                    container['output'].append(itr)
                    itr+=1
    # print(regDefnList)
    pattern = r"(?<![D|d]e)mux(?:[0-9]|1[0-9]|20)?_(?:2|4|8|16|32)_to_(?:1|2|4|8|16)"
    muxInput = []
    defn=""
    check=False
    for line in content:
        if 'begin' in line:
            check=True
        if check and re.search(pattern, line):
            print(line)
            res = re.split(r'[: ]', line)
            res = [item for item in res if item]
            # print(res)
            defn=res[1]
            match = re.search(r"\((.*?)\)", line)
            if match:
                inside_brackets = match.group(1)
                elements = [elem.strip() for elem in inside_brackets.split(",")]
                # print(defn)
                for i in regDefnList[defn]['input']:
                    muxInput.append(elements[i])
    # print(muxInput)
    mTmCnt = 0
    defn=""
    for line in content:
        if 'begin' in line:
            check=True
        if check and re.search(pattern, line):
            # print(line)
            res = re.split(r'[: ]', line)
            res = [item for item in res if item] 
            defn=res[1]
            match = re.search(r"\((.*?)\)", line)
            if match:
                inside_brackets = match.group(1)
                elements = [elem.strip() for elem in inside_brackets.split(",")]
                for i in regDefnList[defn]['output']:
                    # print(elements[i],sep=" ")
                    if elements[i] in muxInput:
                        mTmCnt+=1
    if mTmCnt>0:
        print("mux to mux entry present!")
    return mTmCnt, muxInput



def functionalUnit():
    check = False
    pattern = r"component ([A|a]dder|[M|m]ultiplier)(?:[0-9]|1[0-9]|20)?"
    patt = r"\b(\w+)\b(?=\s*:\s*(in|out))"
    present = []
    for line in content:
        if "component control_unit" in line and not check:
            check=True 
        elif check and re.search(r"end component", line):
            check=False
        elif check:
            # print(line)
            res = re.split(r'[;:, ]', line)
            res = [item for item in res if item]
            print(res)
            present.extend([i for i in res])
    unwanted_strings = {"\n", "in", "out", "std_logic", "INTEGER", "port(", ")", ""}
    
    # Filter the list to keep only valid signal names
    present = [
        item for item in present 
        if item not in unwanted_strings and not item.startswith("--") and not item.isspace()
    ]
    check=False
    trojan = False
    for line in content:
        if re.search(pattern, line) and not check:
            print(line)
            check=True 
        if check and re.search("end component", line):
            check=False 
        if check:
            res = re.split(r'[;:, ]', line)
            res = [item for item in res if item]
            print(res)
            for i in range(len(res)):
                if res[i]=='in' and 'enable' in res[i-1]:
                    print(res[i-1], res[i])
                    if res[i-1] not in present:
                        trojan=True 
                    
    print('Trojan Present' if trojan else None)
    return trojan

def regToMux(regOp, muxIp):
    extraReg = 0
    for i in regOp:
        if i in muxIp:
            extraReg+=1
    print("extra Register Present")

def latch():
    latchCnt = 0
    pattern = r"component ([l|L]atch)(?:[1-9]|1[0-9]|2[0-5])\b"
    for line in content:
        if re.search(pattern, line):
            latchCnt+=1
    return latchCnt

def FU(s):
    Cnt = 0
    pattern = fr"component ([{s[0]}[|{s[0].upper()}]{s[1:]})(?:[1-9]|1[0-9]|2[0-5])\b"
    for line in content:
        if re.search(pattern, line):
            Cnt+=1
    return Cnt


if __name__ == "__main__":
    mux2 = muxCount(2)
    mux4 = muxCount(4)
    mux8 = muxCount(8)
    mux16 = muxCount(16)
    mux32 = muxCount(32)

    demux2=deMuxCount(2)
    demux4=deMuxCount(4)
    demux8=deMuxCount(8)
    demux16=deMuxCount(16)
    demux32=deMuxCount(32)
    notCnt, notChain = notGateCount()
    counterCnt = counterCount()
    TSBCnt = triStateBuffer()
    compCount, presence = comparaterCount()
    extra, regOp, regCnt = extraRegister(presence)
    mtmPresent, muxIp = muxToMux()
    print(regToMux(regOp, muxIp))
    latchCnt = latch()
    # functionalUnit())
    Adder = FU('adder')
    Subtractor = FU('subtractor')
    multiplier = FU('multiplier')