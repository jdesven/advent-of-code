banks = open("2025\input\day3_input.txt").read().split()
    
def calc(l, bank):
    num = ""
    for i in range(l):
        for n in map(str, range(9, -1, -1)):
            if n in bank and len(bank) - bank.find(n) >= l - len(num):
                num += n
                bank = bank[bank.find(n)+1:]
                break
    return int(num)

print(sum(calc(2, bank) for bank in banks))

print(sum(calc(12, num) for num in banks))