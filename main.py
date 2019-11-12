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

def xor(rsrc1, rsrc2):
    
    value_1 = dec_to_bin(registers[rsrc1])
    value_2 = dec_to_bin(registers[rsrc2])

    ans = ""

    for i in range(0, len(value_1)):
        if value_1[i] == value_2[i]:
            ans += "0"
        else:
            ans += "1"

    return int(ans, 2)


def get_program_memory(path):

    program_memory = []

    f = open(path).read()
    lines = f.split("\n")

    program_load = [y.split(" ") for y in lines]

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

    return program_memory

def execute(program_memory):

    registers["a0"] = 0

    while registers["a0"] < len(program_memory):
        
        opcode = program_memory[registers["a0"]]
        instruction = opcode[0:3]

        if instruction == "000":
            rdest = "a" + str(int(opcode[3:6], 2))
            const = opcode[6:]
            registers[rdest] = int(const, 2)  

        elif instruction == "001":
            rdest = "a" + str(int(opcode[3:6], 2))
            rsrc = "a" + str(int(opcode[6:], 2))
            registers[rdest] = registers[rsrc]

        elif instruction == "010":
            rdest = "a" + str(int(opcode[3:6], 2))
            rsrc1 = "a" + str(int(opcode[6:9], 2))
            rsrc2 = "a" + str(int(opcode[9:], 2))
            registers[rdest] = xor(rsrc1, rsrc2)

        elif instruction == "011":
            rdest = "a" + str(int(opcode[3:6], 2))
            rsrc1 = "a" + str(int(opcode[6:9], 2))
            rsrc2 = "a" + str(int(opcode[9:], 2))
            registers[rdest] = registers[rsrc1] + registers[rsrc2]

        elif instruction == "100":
            rdest = "a" + str(int(opcode[3:6], 2))
            const = "a" + str(int(opcode[6:], 2))
            registers[rdest] = registers[rdest] * registers[const]

        elif instruction == "101":
            instruction_type = "I"

        elif instruction == "110":
            instruction_type = "I"

        registers["a0"] += 1

#path = input("Digite o caminho completo do arquivo: ")
path = "first.xampa"
pm = get_program_memory(path)
execute(pm)
debug_registers()