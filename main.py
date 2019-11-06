instructions = {
    "SPC":      ["000", "I"],
    "TCHAN":    ["001", "R"],
    "ARAKETU":  ["010", "R"],
    "PSIRICO":  ["011", "R"],
    "EVA":      ["100", "I"],
    "ASA":      ["101", "I"],
    "IVETE":    ["110", "I"]
}

registers_info = {
    "a0": "000",
    "a1": "001",
    "a2": "010",
    "a3": "011",
    "a4": "100",
    "a5": "101",
    "a6": "110",
    "a7": "111"
}

registers = {
    "a0": 0,
    "a1": 0,
    "a2": 0,
    "a3": 0,
    "a4": 0,
    "a5": 0,
    "a6": 0,
    "a7": 0
}

def debug_registers():
    print("Registradores:")
    print("a0: ", registers["a0"]) 
    print("a1: ", registers["a1"]) 
    print("a2: ", registers["a2"]) 
    print("a3: ", registers["a3"]) 
    print("a4: ", registers["a4"]) 
    print("a5: ", registers["a5"]) 
    print("a6: ", registers["a6"]) 
    print("a7: ", registers["a7"]) 

def dec_to_bin(const):
    aux = bin(int(const)).replace("0b", "")
    t = 6 - len(aux)

    ans = ""
    for i in range(0, t):
        ans += "0"

    ans += aux
    return ans    


#path = input("Digite o caminho completo do arquivo: ")

path = "first.xampa"

f = open(path).read()
lines = f.split("\n")

program_load = [y.split(" ") for y in lines]
program_memory = []

for i in program_load:
    opcode = ""
    for j in i:
        if j == "a0":
            print("Erro de decodificação! Acesso inválido")
            exit()

    if instructions[i[0]][1] == "I":
        opcode = instructions[i[0]][0] + registers_info[i[1]] + dec_to_bin(i[2])
    else:
        if i[0] == "TCHAN":
            opcode = instructions[i[0]][0] + registers_info[i[1]] + registers_info[i[2]]
        else:
            opcode = instructions[i[0]][0] + registers_info[i[1]] + registers_info[i[2]] + registers_info[i[3]]
    
    program_memory.append(opcode)

registers["a0"] = 0

while registers["a0"] < len(program_memory):
    
    opcode = program_memory[registers["a0"]]
    instruction = opcode[0:3]

    # I, R ou TCHAN
    instruction_type = ""

    if instruction == "000":
        instruction_type = "I"
        rdest = "a" + str(int(opcode[3:6], 2))
        const = opcode[6:]
        registers[rdest] = int(const, 2)  

    elif instruction == "001":
        instruction_type = "TCHAN"
        rdest = "a" + str(int(opcode[3:6], 2))
        rsrc = "a" + str(int(opcode[6:], 2))
        registers[rdest] = registers[rsrc]

    elif instruction == "010":
        instruction_type = "R"
    elif instruction == "011":
        instruction_type = "R"
    elif instruction == "100":
        instruction_type = "I"
    elif instruction == "101":
        instruction_type = "I"
    elif instruction == "110":
        instruction_type = "I"

    registers["a0"] += 1

debug_registers()