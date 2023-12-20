import math

#read file into buffer as string
with open("policy_10000_False.txt", "r") as file:
    input = file.read()


large_map = [
    'SFFFFFFF',
    'FFFFFFFF',
    'FFFHFFFF',
    'FFFFFFFF',
    'HFFFFFFF',
    'FFFFFFFF',
    'FFFFFFFF',
    'GFFFFFFF'
]


# function that translate the actions numbers into unicode arrows
# 0: left, 1: down, 2: right, 3: up
def translate_action(action):
    if action == 0:
        return "←"
    elif action == 1:
        return "↓"
    elif action == 2:
        return "→"
    elif action == 3:
        return "↑"

#print(input)

# read the input and split it into lines
lines = input.splitlines()
# for each state, print the associated action in a grid, according to the state's coordinates
# the states are a nxn matrix
n = int(math.sqrt(len(lines)))

for i in range(n):
    for j in range(n):
        action = lines[i*n + j].split(",")[1].split(": ")[1]
        if(large_map[i][j] == 'H'):
            print("H", end=" ")
            continue
        elif(large_map[i][j] == 'G'):
            print("G", end=" ")
            continue
        print(translate_action(int(action)), end=" ")
    print()