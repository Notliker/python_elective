class Player:
    def __init__(self, name):
        self.name = name

class Random(Player):  
    def __init__(self, name):
        super().__init__(name)
    
    def guess(self, low, high):
        import random
        return random.randint(low, high)

class Dihotomy(Player):
    def __init__(self, name):
        super().__init__(name)

    def guess(self, low, high):
        return (low+high)//2

class User(Player):
    def __init__(self, name):
        super().__init__(name)

    def guess(self, low, high):
        while True:
            return int(input(f"Угадай число, где нижняя граница {low}, а верхняя {high}: "))
            
player = Player("Kirill")
low = 1
high = 100
num = 37

# rand = Random(player)
# if rand.guess(low, high) == num:
#     print("Congratulation")
# else:
#     print("Nope")

# dih = Dihotomy(player)
# l=low
# r=high
# c=1
# while True:
#     ans = dih.guess(l,r)
#     if ans < num:
#         l=ans+1
#         c+=1
#     elif ans > num:
#         r=ans-1
#         c+=1
#     else:
#         print(f"Congrats, it makes with {c} attemps")
#         break

# us = User(Player)
# while True:
#     if us.guess(low, high) == num:
#         print("Congrats")
#         break
#     else:
#         print("try again")

class Gamemanager:
    import random
    def __init__(self, player1, player2, max_steps, num=random.randint(1,100)):
        self.players=[[player1,[]], [player2,[]]]
        self.low = max(0, num-50)
        self.high = min(100, num+50)
        self.max_steps = max_steps
        self.num = num
        self.steps = 0

    def start_game(self):
        l, r = self.low, self.high
        while self.steps < self.max_steps:
            for i in range(len(self.players)):
                player = self.players[i][0]         
                history = self.players[i][1] 

                if isinstance(player, Dihotomy):
                    ans = player.guess(l, r)
                else:
                    ans = player.guess(self.low, self.high)
                while ans in history:
                    if isinstance(player, Dihotomy):
                        ans = player.guess(l, r)
                    else:
                        ans = player.guess(self.low, self.high)
                if ans == self.num:
                    print(f"Congrats, winner is {player.__class__.__name__}")
                    return player.__class__.__name__
                else:
                    history.append(ans)
                if isinstance(player, Dihotomy):
                    if ans < self.num:
                        l = ans + 1
                    else:
                        r = ans - 1

                self.steps += 1
                if self.steps >= self.max_steps:
                    break

        best_dist = float('inf')
        winners = []
        for p, h in self.players:
            last_guess = h[-1] if len(h)>0 else None
            dist = abs(self.num - last_guess) if last_guess is not None else float('inf')
            if dist < best_dist:
                best_dist = dist
                winners = [p]
            elif dist == best_dist:
                winners.append(p)

        if not winners or best_dist == float('inf'):
            print("Draw")
            return "Draw"
        if len(winners) == 1:
            p = winners[0]
            print(f"Winner by proximity: {p.__class__.__name__}")
            return p.__class__.__name__
        else:
            names = ", ".join(w.__class__.__name__ for w in winners)
            print(f"Tie by proximity between: {names}")
            return "Draw"


player1=Random(player)
player2=Dihotomy(player)
game=Gamemanager(player1, player2, max_steps=20, num=37)
print(game.start_game())

