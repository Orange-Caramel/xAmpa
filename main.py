import os

#Memory for instructions
program_memory = []

#Main data memory
data_memory = []

#Map to aux in instructions
instructions = {
    "SPC":      ["000", "I"],
    "TCHAN":    ["001", "R"],
    "ARAKETU":  ["010", "R"],
    "PSIRICO":  ["011", "R"],
    "EVA":      ["100", "I"],
    "ASA":      ["101", "I"],
    "IVETE":    ["110", "I"]
}

#Map to aux in registers
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

#Memory of registers
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

#Start data memory
def init_data_memory():
    for i in range(0, 2**6):
        data_memory.append(0)

#Aux to debug register
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

#Base convertion (10) -> (2)
def dec_to_bin(const):
    aux = bin(int(const)).replace("0b", "")
    t = 6 - len(aux)

    ans = ""
    for i in range(0, t):
        ans += "0"

    ans += aux
    return ans

#Exclusive OR between constants
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

#Decoding intructions 
def get_program_memory(path):
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

#Cache Block
class Block:
    def __init__(self, tag, instruction):
        self.tag = tag
        self.instruction = instruction

#Cache
class Cache:
    def __init__(self, size):
        self.blocks = [Block(None, None)] * size

    def load_instruction(self, first):
        if len(program_memory) > first:
            self.blocks[0] = Block(registers["a0"], program_memory[first])
        if len(program_memory) > first+1:
            self.blocks[1] = Block(registers["a0"]+1, program_memory[first+1])
        if len(program_memory) > first+2:
            self.blocks[2] = Block(registers["a0"]+2, program_memory[first+2])
        if len(program_memory) > first+3:
            self.blocks[3] = Block(registers["a0"]+3, program_memory[first+3])

    def check_instruction(self, tag):
        for i in self.blocks:
            if i.tag == tag:
                return True
        return False
    
    def grab_instruction(self, tag):
        for i in self.blocks:
            if i.tag == tag:
                return i.instruction

    def debug(self):
        for i in self.blocks:
            print("Tag", i.tag, "Data", i.instruction)

#Main routine to execute VM
def execute(program_memory, debug):
    #Creating Cache with 4 blocks
    cache = Cache(4)

    #Initialize PC
    registers["a0"] = 0

    #Main exectuion
    while registers["a0"] < len(program_memory):
        #Checking the cache
        if cache.check_instruction(registers["a0"]):
            opcode = cache.grab_instruction(registers["a0"])
            if debug == 'S' or debug == 's':
                print("Cache Hit!")
        else:
            cache.load_instruction(registers["a0"])
            if debug == 'S' or debug == 's':
                print("Cache Miss!")
                print("Cache atualizada: ")
                cache.debug()
            opcode = cache.grab_instruction(registers["a0"])


        #Exectuing the instruction
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
            rdest = "a" + str(int(opcode[3:6], 2))
            const = "a" + str(int(opcode[6:], 2))
            data_memory[const] = registers[rdest]

        elif instruction == "110":
            rdest = "a" + str(int(opcode[3:6], 2))
            const = "a" + str(int(opcode[6:], 2))
            registers[rdest] = data_memory[const]

        if debug == 'S' or debug == 's':
            debug_registers()
            os.system("pause")
            os.system("cls")

        #Increasing PC with the next instruction
        registers["a0"] += 1


path = input("Digite o caminho completo do arquivo: ")
debug = input("Deseja executar em modo debug? (S / N) ")

init_data_memory()
pm = get_program_memory(path)
execute(pm, debug)
if debug == 'N' or debug == 'n':
    debug_registers()