import numpy as np
import math
import random


class EngagexPlayer(object):
    def __init__(self, id, x, y, game):
        self.id = id
        self.x = x
        self.y = y
        self.hp = 100
        self.xp = 0
        self.game = game

    def move(self, direction):
        if direction == "north":
            self.y += 1
            self.hp -= 1
        elif direction == "south":
            self.y -= 1
            self.hp -= 1
        elif direction == "east":
            self.x += 1
            self.hp -= 1
        elif direction == "west":
            self.x -= 1
            self.hp -= 1
        else:
            print("Invalid direction")

    def commit(self):
        committed = self.hp // 2
        self.hp -= committed
        self.xp += committed

    def collect(self):
        life = 0
        if (self.x, self.y) in self.game.cell_life:
            life = self.game.cell_life[(self.x, self.y)]
        diff = min(100 - self.hp, life)
        self.hp += diff
        if (self.x, self.y) in self.game.cell_life:
            self.game.cell_life[(self.x, self.y)] -= diff

    def attack(self):
        playersInPos = [
            p
            for p in self.game.players
            if p.x == self.x and p.y == self.y and p.id != self.id
        ]
        # if len(playersInPos) >= 1:
        player2 = playersInPos[0]
        half_own = self.hp // 2
        half_other = player2.hp // 2
        self.hp -= half_own
        player2.hp -= half_other
        sum_spent = half_own + half_other
        if random.randint(1, 100) <= 50:
            self.hp = min(self.xp + sum_spent // 2, 100)
        else:
            player2.hp = min(player2.xp + sum_spent // 2, 100)

    def kill(self):
        playersInPos = [
            p
            for p in self.game.players
            if p.x == self.x and p.y == self.y and p.id != self.id
        ]
        # if len(playersInPos) >= 1:
        player2 = playersInPos[0]
        if random.randint(1, 100) <= 25:
            rem_hp = player2.hp
            player2.hp = 0
            self.xp = min(self.xp + rem_hp // 2, 100)
        else:
            rem_hp = self.hp
            self.hp = 0
            player2.xp = min(player2.xp + rem_hp // 2, 100)

    def flee(self):
        dist_run = 3
        while True:
            possible_moves = []
            i = -dist_run
            while i <= dist_run:
                j = dist_run - abs(i)
                j2 = -j
                if self.game.can_flee_to(self.x + i, self.y + j):
                    possible_moves.append((i, j))
                if self.game.can_flee_to(self.x + i, self.y + j2):
                    possible_moves.append((i, j2))
                i += 1
            if len(possible_moves) == 0:
                dist_run += 1
            else:
                r = random.randint(0, len(possible_moves) - 1)
                self.x += possible_moves[r][0]
                self.y += possible_moves[r][1]
                break

    def seed(self):
        to_seed = 10
        deltas = [(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0)]
        x, y = self.x, self.y
        for d in deltas:
            life = 0
            if (x + d[0], y + d[1]) in self.game.cell_life:
                life = self.game.cell_life[(x + d[0], y + d[1])]
            self.game.cell_life[(x + d[0], y + d[1])] = min(life + to_seed, 100)
        self.hp -= 2 * to_seed

    def share(self):
        playersInPos = [
            p
            for p in self.game.players
            if p.x == self.x and p.y == self.y and p.id != self.id
        ]
        # if len(playersInPos) >= 1:
        player2 = playersInPos[0]
        if self.hp > player2.hp:
            diff = (self.hp - player2.hp) // 2
            self.hp -= diff
            player2.hp += diff

    def is_alive(self):
        return self.hp > 0

    def apply_action(self, action_string):
        if action_string == "move_north":
            self.move("north")
        elif action_string == "move_south":
            self.move("south")
        elif action_string == "move_east":
            self.move("east")
        elif action_string == "move_west":
            self.move("west")
        elif action_string == "commit":
            self.commit()
        elif action_string == "collect":
            self.collect()
        elif action_string == "attack":
            self.attack()
        elif action_string == "kill":
            self.kill()
        elif action_string == "flee":
            self.flee()
        elif action_string == "seed":
            self.seed()
        elif action_string == "share":
            self.share()
        else:
            print("Invalid action")


def hash_pos(pos, key):
    str_pos = "(%d,%d)" % (pos[0], pos[1])
    return hash(str_pos) ^ key


class GameState(object):
    def __init__(self, num_players, no_moves=500):
        self.key = random.randint(1, 1e9)
        self.num_players = num_players
        self.players = [EngagexPlayer(i, i, i, self) for i in range(num_players)]
        self.cell_life = {}
        self.remaining_moves = no_moves
        self.num_actions = 11
        self.total_actions = [0 for i in range(self.num_actions)]

    def can_to_go(self, x, y):
        playersInPos = [p for p in self.players if p.x == x and p.y == y]
        return len(playersInPos) < 2

    def can_flee_to(self, x, y):
        playersInPos = [p for p in self.players if p.x == x and p.y == y]
        return len(playersInPos) < 1

    def legal_actions(self, player):
        ans = []
        if player.hp <= 0:
            return ans
        playersNorth = [
            p for p in self.players if p.x == player.x and p.y == player.y + 1
        ]
        if len(playersNorth) < 2:
            ans.append(0) # "move_north"
        playersSouth = [
            p for p in self.players if p.x == player.x and p.y == player.y - 1
        ]
        if len(playersSouth) < 2:
            ans.append(1) # "move_south"
        playersEast = [
            p for p in self.players if p.x == player.x + 1 and p.y == player.y
        ]
        if len(playersEast) < 2:
            ans.append(2) # "move_east"
        playersWest = [
            p for p in self.players if p.x == player.x - 1 and p.y == player.y
        ]
        if len(playersWest) < 2:
            ans.append(3) # "move_west"

        if (
            (player.x, player.y) in self.cell_life
            and self.cell_life[(player.x, player.y)] > 0
            and player.hp < 100
        ):
            ans.append(4)  # collect - player must not be in full health
        if player.hp > 1:
            ans.append(5)  # commit
        if player.hp > 20 and (
            (player.x, player.y) not in self.cell_life
            or self.cell_life[(player.x, player.y)] < 100
        ):  # seed
            ans.append(6)

        playersInPos = [
            p
            for p in self.players
            if p.x == player.x and p.y == player.y and p.id != player.id and p.hp > 0
        ]
        if len(playersInPos) > 0:
            ans.append(7)  # attack
            ans.append(8)  # kill
            if player.hp > 25:
                ans.append(9)  # flee
            if playersInPos[0].hp < player.hp:
                ans.append(10)  # share
        # print("Legal actions: ", ans)
        return np.array(ans, dtype=np.int32)

    def observation_tensor(
        self, player_id
    ):  # to what point could we include game-related metrics such as closest cell with fuel?
        num_rows_observation = 2
        num_cols_observation = 3
        observation = np.zeros(
            (num_rows_observation * 2 + 1, num_cols_observation * 2 + 1, 5)
        )
        for i in range(-num_rows_observation, num_rows_observation + 1):
            for j in range(-num_cols_observation, num_cols_observation + 1):
                ri = i + num_rows_observation
                rj = j + num_cols_observation
                x = self.players[player_id].x + j
                y = self.players[player_id].y + i
                if (x, y) in self.cell_life:
                    observation[ri, rj, 0] = self.cell_life[(x, y)]
                observation[ri, rj, 1:4] = -100
                playersInPos = [p for p in self.players if p.x == x and p.y == y]
                playersInPos.sort(key = lambda p: abs(player_id - p.id))
                if len(playersInPos) > 0:
                    observation[ri, rj, 1] = playersInPos[0].hp
                    observation[ri, rj, 2] = playersInPos[0].xp
                    if len(playersInPos) > 1:
                        observation[ri, rj, 3] = playersInPos[1].hp
                        observation[ri, rj, 4] = playersInPos[1].xp
        observation = observation.flatten()
        # now include other relevant metrics
        other_scores = [p.xp for p in self.players if p.id != player_id]
        own_score = self.players[player_id].xp
        observation = np.hstack((observation, own_score, other_scores))
        return observation

    def step(self, id_player, action, print_player_action = False):
        actions = [
            "move_north",
            "move_south",
            "move_east",
            "move_west",
            "collect",
            "commit",
            "seed",
            "attack",
            "kill",
            "flee",
            "share",
        ]
        act = actions[action]
        prev_score = self.players[id_player].xp
        prev_health = self.players[id_player].hp
        self.players[id_player].apply_action(act)
        curr_score = self.players[id_player].xp
        reward = curr_score - prev_score
        if action < 0 or action > len(actions):
            print("Invalid action")
            return
        if act == "collect" and prev_health <=35:
            # aims to favor collection when health <= 35
            reward += 100
        if act == "seed" and prev_health >=70:
            # aims to favor sowing when health >= 70
            reward += 100
        if (
            self.players[id_player].hp == 0
        ):  # player died, needs to avoid dying and to maximize score
            if self.players[id_player].xp < 100:
                reward -= 100 - self.players[id_player].xp
            else:
                best_player_score = max([p.xp for p in self.players])
                reward -= best_player_score - self.players[id_player].xp
        observation = self.observation_tensor(id_player)
        self.remaining_moves -= 1
        done = self.remaining_moves <= 0 or all(
            [self.players[i].hp <= 0 for i in range(self.num_players)]
        )
        if print_player_action:
            print(id_player, "-", act, "health", self.players[id_player].hp, "xp", self.players[id_player].xp)
        if self.remaining_moves % 100 == 0:
            print("Remaining moves: ", self.remaining_moves)

        self.total_actions[action] += 1  # so that we can count and plot them

        # print("observation: ", observation.shape)
        # print("reward", reward)
        # print("done", done)
        return observation, reward, done

    def is_terminal(self):
        return (
            self.remaining_moves <= 0
            or len([p for p in self.players if p.is_alive()]) <= 1
        )
