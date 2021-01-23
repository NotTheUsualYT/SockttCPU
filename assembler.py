import sys


def err(errtype, linenum):
    linenum = int(linenum)
    sys.stderr.write(f"Error: {errtype} at line {linenum}\n")


def parselabels(asmfile):
    memcount = 0
    labels = {}
    for line in asmfile:
        if line.startswith("."):
            labels[line]=memcount
        memcount += 4
        print(hex(memcount))
        for label in labels:
            print(hex(labels[label]))

    return labels


def makebin(asmfile, labels):
    binary = []
    linecount = 1
    for line in asmfile:
        if not line.startswith("."):
            inst = line.split()

            # -----------------------------
            #   Loading into registers    |
            # -----------------------------

            if inst[0] == "ld":
                binary.append(0x00)
                if inst[1] == "r1":
                    binary.append(0x01)
                elif inst[1] == "r2":
                    binary.append(0x02)
                else:
                    err("Invalid register", linecount)
                    sys.exit(1)

                binary.append(int(inst[2], 16) >> 8)
                binary.append(int(inst[2], 16) & 0b11111111)
                linecount += 1

            elif inst[0] == "lm":  # lm: Load from memory
                binary.append(0x01)
                if inst[1] == "r1":
                    binary.append(0x01)
                elif inst[2] == "r2":
                    binary.append(0x02)
                else:
                    err("Invalid register", linecount)
                    sys.exit(1)

                binary.append(int(inst[2], 16) >> 8)
                binary.append(int(inst[2], 16) & 0b11111111)
                linecount += 1

            elif inst[0] == "lr":  # lr: Load from register
                binary.append(0x02)
                if inst[1] == "r1":
                    binary.append(0x01)
                elif inst[1] == "r2":
                    binary.append(0x02)
                else:
                    err("Invalid register", linecount)
                    sys.exit(1)

                binary.append(0x00)

                if inst[2] == "r1":
                    binary.append(0x01)
                elif inst[2] == "r2":
                    binary.append(0x02)
                else:
                    err("Invalid register", linecount)
                    sys.exit(1)
                linecount += 1

            # -----------------------------
            #         Comparisons         |
            # -----------------------------

            elif inst[0] == "cmp":
                binary.append(0x10)
                if inst[1] == "r1":
                    binary.append(0x01)
                elif inst[1] == "r2":
                    binary.append(0x02)
                else:
                    err("Invalid register", linecount)
                    sys.exit(1)

                binary.append(int(inst[2], 16) >> 8)
                binary.append(int(inst[2], 16) & 0b11111111)
                linecount += 1

            elif inst[0] == "cpr":
                binary.append(0x11)
                if inst[1] == "r1":
                    binary.append(0x01)
                elif inst[1] == "r2":
                    binary.append(0x02)
                else:
                    err("Invalid register", linecount)
                    sys.exit(1)

                binary.append(0x00)

                if inst[1] == "r1":
                    binary.append(0x01)
                elif inst[1] == "r2":
                    binary.append(0x02)
                else:
                    err("Invalid register", linecount)
                    sys.exit(1)
                linecount += 1

            elif inst[0] == "cpm":
                binary.append(0x12)
                if inst[1] == "r1":
                    binary.append(0x01)
                elif inst[1] == "r2":
                    binary.append(0x02)
                else:
                    err("Invalid register", linecount)
                    sys.exit(1)

                binary.append(int(inst[2], 16) >> 8)
                binary.append(int(inst[2], 16) & 0b11111111)
                linecount += 1

            # -----------------------------
            #        Math (Addition)      |
            # -----------------------------

            elif inst[0] == "add":
                binary.append(0x20)
                if inst[1] == "r1":
                    binary.append(0x01)
                elif inst[1] == "r2":
                    binary.append(0x02)
                else:
                    err("Invalid register", linecount)
                    sys.exit(1)

                binary.append(int(inst[2], 16) >> 8)
                binary.append(int(inst[2], 16) & 0b11111111)
                linecount += 1

            elif inst[0] == "adr":
                binary.append(0x21)
                if inst[1] == "r1":
                    binary.append(0x01)
                elif inst[1] == "r2":
                    binary.append(0x02)
                else:
                    err("Invalid register", linecount)
                    sys.exit(1)

                binary.append(0x00)

                if inst[2] == "r1":
                    binary.append(0x01)
                elif inst[2] == "r2":
                    binary.append(0x02)
                else:
                    err("Invalid register", linecount)
                    sys.exit(1)
                linecount += 1

            # -----------------------------
            #             Jumps           |
            # -----------------------------

            elif inst[0] == "jmp":
                binary.append(0x30)
                binary.append(0x00)
                if inst[1] in labels:
                    binary.append(int(hex(labels[inst[1]]), 16) >> 8)
                    binary.append(int(hex(labels[inst[1]]), 16) & 0b11111111)
                else:
                    err("Unknown label", linecount)
                linecount += 1

            else:
                err("Invalid instruction", linecount)
                sys.exit(2)

    with open("out.bin", "wb") as f:
        f.write(bytes(binary))

    print("done!")


if len(sys.argv) != 2:
    sys.stderr.write(f"Usage: {sys.argv[0]} File")
else:
    file = []

    with open(sys.argv[1], "r") as f:
        for line in f:
            line = line.strip()
            if line:
                file.append(line)

    labels = parselabels(file)
    makebin(file, labels)
