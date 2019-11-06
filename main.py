def dec_to_bin(const):
    aux = bin(int(const)).replace("0b", '')
    t = 6 - len(aux)

    ans = ""
    for i in range(0, t):
        ans += '0'

    ans += aux
    return ans    


instructions = {
    "SPC":      ["000", 'I'],
    "TCHAN":    ["001", 'R'],
    "ARAKETU":  ["010", 'R'],
    "PSIRICO":  ["011", 'R'],
    "EVA":      ["100", 'I'],
    "ASA":      ["101", 'I'],
    "IVETE":    ["110", 'I']
}

registers = {
    "a0": "000",
    "a1": "001",
    "a2": "010",
    "a3": "011",
    "a4": "100",
    "a5": "101",
    "a6": "110",
    "a7": "111"
}

#path = input("Digite o caminho completo do arquivo: ")

path = "first.xampa"

f = open(path).read()
lines = f.split('\n')

program_load = [y.split(' ') for y in lines]
program_memory = []

for i in program_load:
    opcode = ""
    if instructions[i[0]][1] == 'I':
        opcode = instructions[i[0]][0] + registers[i[1]] + dec_to_bin(i[2])
    else:
        if i[0] == "TCHAN":
            opcode = instructions[i[0]][0] + registers[i[1]] + registers[i[2]]
        else:
            opcode = instructions[i[0]][0] + registers[i[1]] + registers[i[2]] + registers[i[3]]
    
    program_memory.append(opcode)

program_counter = 0
while program_counter < len(program_memory):
    opcode = program_memory[program_counter]
    instruction = opcode[0:3]

    if instruction == "000":

    elif instruction == "001":

    elif instruction == "00":

    elif instruction == "001":

    elif instruction == "001":

    elif instruction == "001":

    elif instruction == "001":

    elif instruction == "001":

    elif instruction == "001":

    program_counter += 1