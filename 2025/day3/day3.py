banks = open("2025\input\day3_input.txt").read().split('\n')
    
def calc(l):
    ans = 0
    for bank in banks:
        num = ""
        for i in range(l):
            for n in map(str, range(9, -1, -1)):
                if n in bank and len(bank) - bank.find(n) >= l - len(num):
                    num += n
                    bank = bank[bank.find(n)+1:]
                    break
        ans += int(num)
    print(ans)

calc(2)

calc(12)