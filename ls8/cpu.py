"""CPU functionality."""

import sys
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010 
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000
JMP = 0b01010100
CMP = 0b10100111
JEQ = 0b01010101
JNE = 0b01010110
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 0
        self.fl = 0

    def load(self, filename):
        """Load a program into memory."""
        try: 
            address = 0

            with open(filename) as f:
                for line in f:
                    # ignore comment
                    comment_split = line.split('#')

                    # convert binary string to integer
                    num = comment_split[0].strip()
                    try:
                        val = int(num, 2)
                    except ValueError:
                        continue
                    # write into ram
                    # print('address:', address, 'num:', num)
                    self.ram_write(address, val)
                    address += 1

        except FileNotFoundError:
            print('File not found')
            sys.exit(1)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == 'CMP':
            # FL bits: 00000LGE
            if self.reg[reg_a] == self.reg[reg_b]:
                self.fl = 0b00000001
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.fl = 0b00000100
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.fl = 0b00000010
            else:
                self.fl = 0b00000000
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        is_running = True
        while is_running is True:
            ir = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            if ir == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif ir == PRN:
                print(self.reg[operand_a])
                # print(self.reg)
                self.pc += 2
            elif ir == HLT:
                is_running = False
                sys.exit(1)
            elif ir == MUL:
                self.alu('MUL', operand_a, operand_b)
                # self.reg[operand_a] *= self.reg[operand_b]
                self.pc += 3
            elif ir == ADD:
                self.alu('ADD', operand_a, operand_b)
                self.pc += 3
            elif ir == PUSH:
                self.sp -= 1
                self.ram[self.sp] = self.reg[operand_a]
                self.pc += 2
            elif ir == POP:
                self.reg[operand_a] = self.ram[self.sp]
                self.sp += 1
                self.pc += 2
            elif ir == CALL:
                self.sp -= 1
                self.ram[self.sp] = self.pc + 2
                # reg = self.ram[self.pc + 1]
                self.pc = self.reg[operand_a]
            elif ir == RET:
                self.pc = self.ram[self.sp]
                # self.sp += 1
            elif ir == JMP:
                self.pc = self.reg[operand_a]
            elif ir == CMP:
                self.alu('CMP', operand_a, operand_b)
                self.pc += 3
            elif ir == JEQ:
                if self.fl == 0b00000001:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2
            elif ir == JNE:
                if ((self.fl == 0b00000001) == 0):
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2
            else:
                print(f'Unknown command: {ir}')
                sys.exit(1)

    def ram_read(self, mar):
        return self.ram[mar]
    def ram_write(self, mdr, value):
        self.ram[mdr] = value
