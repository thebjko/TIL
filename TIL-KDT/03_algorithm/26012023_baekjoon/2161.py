# 카드1

def card_1_2161():
    n = int(input())
    cards = list(range(1, n + 1))
    while True:
        print(cards.pop(0))
        if cards:
            cards.append(cards.pop(0))
        else:
            break

if __name__ == "__main__":
    solution = card_1_2161
    solution()
