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

def notGateCount():
    ntGtCnt = 0
    pattern = r"component not(?:[1-9]|1[0-9]|2[0-5])\b"
    not_chain_pattern = r"not\((?:not\()+"
    chainPresent = False
    presence = False
    for line in content:
        if re.search(pattern, line):
            ntGtCnt+=1
        if "begin" in line:
            presence=True
        if presence and 'end' in line:
            presence=False 
        if presence:
            if re.search(not_chain_pattern, line):
                chainPresent=True 

    return ntGtCnt, chainPresent

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
    if presence:
        pattern = r"component comparator(?:[1-9]|1[0-9]|2[0-5])\b"
        regPattern = r"component register[A-Z]{1,2}"
        checkComp, checkReg = False, False
        extraReg = 0
        compDefnList = {}
        regDefnList = {}
        itr = 0
        container = {}
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
                container={}
                defn = ""
                checkComp=False
            if checkComp:
                res = re.split(r'[;:,]', line)
                for i in range(res):
                    if res[i]=='in':
                        container[itr]='input'
                        itr+=1
                    if res[i]=='out':
                        container[itr]='ouput'
                        itr+=1
            if re.search(regPattern, line) and not checkReg:
                checkReg=True 
                res=line.split()
                defn+=res[1]
            if checkReg and re.search(r'end component', line):
                itr = 0
                regDefnList[defn]=container
                container={}
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
                        container['output']=itr
                        itr+=1
        regOutput = []

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
                regOutput.append(elements[regDefnList[defn]['output']])
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
        return extraReg
    return 0

def muxToMux():
    pattern = r"component (?<!de)mux(?:[0-9]|1[0-9]|20)?_(?:2|4|8|16|32)_to_(?:1|2|4|8|16)"
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
    return mTmCnt


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



if __name__ == "__main__":
    print(muxCount(2))
    print(notGateCount())
    print(counterCount())
    print(triStateBuffer())
    compCount, presence = comparaterCount()
    print(extraRegister(presence))
    print(muxToMux())
    print(functionalUnit())