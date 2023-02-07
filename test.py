import random

msg = ["Computer is about to make a move. Press Enter to continue...",
       "It's your turn to make a move. Enter your command.", "Invalid input. Please try again.",
       "The game is over. {winner}!", "Illegal move. Please try again."]


def start(n):
    global domino, player, computer, stock, turn
    domino = [[i, j] for i in range(0, n + 1) for j in range(i, n + 1)]
    while True:
        random.shuffle(domino)
        stock = domino[0:len(domino) // 2]
        computer = domino[len(stock):len(stock) + n + 1]
        player = domino[- n - 1:len(domino)]
        if len(player) != len(computer):
            turn = 0 if len(player) > len(computer) else 1
            break
        else:
            max_ = [max(i) if len(i) != 0 else i for i in
                    [list(filter(lambda x: x[0] == x[1], player)), list(filter(lambda x: x[0] == x[1], computer))]]
            if max(max_) != []:
                turn = max_.index(max(max_))
                who = player if turn == 0 else computer
                domino = [who.pop(who.index(max(max_)))]
            break


def game():
    print("=" * 70)
    print("Stock size:", len(stock))
    print("Computer pieces:", len(computer))
    print()
    if len(domino) < 7:
        print(*domino, sep="")
    else:
        print(*domino[:3], "...", *domino[-4:], sep="")
    print()
    print("Your pieces:")
    for i in player:
        print(player.index(i) + 1, ":", i, sep="")
    result = 0
    if len(player) == 0:
        result = "You won"
    elif len(computer) == 0:
        result = "The computer won"
    elif draw():
        result = "It's a draw"
    if result:
        print("Status:", msg[3].format(winner=result))
        return False
    else:
        print("Status:", msg[turn % 2])
        return True


def move():
    global domino, player, computer, stock, turn
    if turn % 2:
        while True:
            what = input()
            side = 1 if what.find("-") == 0 else 0
            what = what[1:] if side else what
            if what.isnumeric() and (0 <= int(what) <= len(player)):
                card = rule(int(what), side) if int(what) > 0 else (stock.pop() if len(stock) else None)
                if card == None:
                    break
                elif what == "0":
                    player.append(card)
                    break
                elif card == []:
                    print(msg[4])
                    continue
                else:
                    player.pop(int(what) - 1)
                    if side:
                        domino = [card] + domino
                    else:
                        domino.append(card)
                break
            else:
                print(msg[2])
    else:
        lol = input()
        c = None
        for i in range(len(computer)):
            for j in [0, 1]:
                ans = rule(i + 1, j)
                if ans != []:
                    c = ans
                    computer.pop(i)
                    if j:
                        domino = [c] + domino
                    else:
                        domino.append(c)
                    break
            if c != None:
                break
        if c == None:
            if len(stock):
                computer.append(stock.pop())
    turn += 1
    return


start(6)


def draw():
    if len(stock):
        return False
    if len(player) != 0 and len(computer) != 0:
        for who in [0, 1]:
            for i in range(len(player if who else computer)):
                for j in (0, 1):
                    if rule(i + 1, j):
                        return False
    return True


def rule(card, side):
    temp = (player if turn % 2 else computer)[card - 1]
    for i in [temp, temp[::-1]]:
        if i[side] == domino[side - 1][(side + 1) % 2]:
            return i
    return []


while game():
    move()