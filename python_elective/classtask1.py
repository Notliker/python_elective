class Player:
    def __init__(self, name):
        self.name = name


class Random(Player):  
    def __init__(self, name):
        super().__init__(name)
    
    def guess(self, game_data):
        import random
        return random.randint(game_data['low'], game_data['high'])


class Dihotomy(Player):
    def __init__(self, name):
        super().__init__(name)
    
    def guess(self, game_data):
        return (game_data['low'] + game_data['high']) // 2


class User(Player):
    def __init__(self, name):
        super().__init__(name)
    
    def guess(self, game_data):
        while True:
            return int(input(f"Угадай число, где нижняя граница {game_data['low']}, а верхняя {game_data['high']}: "))


class Gamemanager:
    def __init__(self, player1, player2, max_steps, num=None):
        import random
        if num is None:
            num = random.randint(1, 100)
        
        self.players = [[player1, []], [player2, []]]
        self.low = max(0, num - 50)
        self.high = min(100, num + 50)
        self.max_steps = max_steps
        self.num = num
        self.steps = 0

    def start_game(self):        
        player_bounds = [[self.low, self.high], [self.low, self.high]]
        
        while self.steps < self.max_steps:
            for i in range(len(self.players)):
                player = self.players[i][0]         
                history = self.players[i][1]
                
                game_data = {
                    'low': player_bounds[i][0],
                    'high': player_bounds[i][1],
                    'history': history,
                    'num': self.num,  
                    'steps': self.steps
                }
                
                ans = player.guess(game_data)
                
                while ans in history:
                    ans = player.guess(game_data)
                
                if ans == self.num:
                    print(f"Congrats, winner is {player.name}")
                    return player.__class__.__name__
                else:
                    history.append(ans)
                
                if ans < self.num:
                    player_bounds[i][0] = ans + 1
                else:
                    player_bounds[i][1] = ans - 1
                
                self.steps += 1
                if self.steps >= self.max_steps:
                    break
        
        best_dist = float('inf')
        winners = []
        for p, h in self.players:
            last_guess = h[-1] if len(h) > 0 else None
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
            print(f"Winner by proximity: {p.name}")
            return p.name
        else:
            names = ", ".join(w.name for w in winners)
            print(f"Tie by proximity between: {names}")
            return "Draw"


player = Player("Kirill")
player1 = Random("Egor")
player2 = Dihotomy("Edik")
game = Gamemanager(player1, player2, max_steps=20, num=37)
print(game.start_game())

