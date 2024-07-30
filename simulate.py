import random
from collections import Counter
from typing import List

from doudizhu import Card, new_game,check_card_type,cards_greater,list_greater_cards
CARDS = '3-4-5-6-7-8-9-10-J-Q-K-A-2-BJ-CJ'.split('-')
CARD_IDX = {c : w for w, c in enumerate(CARDS)}
class LandlordGame :
    def __init__(self) :


        self.cards = None
        self.players = [
            {"cards": [], "bid": 0,"charactor": 0, "score": 0},
            {"cards": [], "bid": 0,"charactor": 0, "score": 0},
            {"cards": [], "bid": 0,"charactor": 0, "score": 0}
        ]

        self.landlord_cards = []
        self.score = 0
        self.history = []
        self.landlord = None
        self.last_winner = None
        self.last_winner2 = None  # 农民获胜有两个赢家
        self.current_cards = []
        self.current_cards_user = None

    def distribute_cards(self):
        cards_groups = new_game()
        self.history = []
        self.landlord_cards = []
        self.score = 0
        # self.last_winner = None
        self.current_cards = []
        self.current_cards_user = None
        for i in range(3) :
            self.players[i]["cards"].extend(reversed(cards_groups[i]))
            print("玩家", i, "初始牌", Card.cards_without_suit(self.players[i]["cards"]))
        self.landlord_cards = cards_groups[3]
        print("地主牌", Card.cards_without_suit(self.landlord_cards))

    def bid_for_landlord(self) :
        # 简单的随机抢地主策略，每个玩家随机出0, 1, 2, 3分
        if self.last_winner is not None :
            start_player = self.last_winner
            print("叫地主，从上局赢家", start_player, "开始叫分")
        else :
            start_player = random.randint(0, 2)
            print("叫地主,无上局赢家,随机从玩家", start_player, "开始叫分")

            # 从start_player开始叫分
        current_bid = 0
        self.landlord = start_player
        for i in range(3) :
            player_id = (start_player + i) % 3
            bid = random.randint(0, 3)
            self.players[player_id]["bid"] = bid
            if bid > current_bid :
                current_bid = bid
                self.landlord = player_id
        self.score = current_bid if current_bid > 0 else 1
        print("地主", self.landlord, "叫分", current_bid)
        self.players[self.landlord]["charactor"] = 1
        self.players[self.landlord]["cards"].extend(self.landlord_cards)
        new_landlord_cards = Card.sort_cards_by_rank_int(self.players[self.landlord]["cards"])
        # print(new_landlord_cards)
        new_landlord_cards = list(reversed(new_landlord_cards))
        # print(new_landlord_cards)
        self.players[self.landlord]["cards"] = new_landlord_cards
        print("地主牌已经更新,地主", self.landlord, Card.cards_without_suit(self.players[self.landlord]["cards"]))

    def play(self):
        # 简单的模拟出牌过程
        # 这里可以实现更加复杂的策略
        current_player = self.landlord
        self.history = []
        self.current_cards = []
        self.last_winner2 = None
        self.current_cards_user = None

        while not self.is_game_over():
            # print("当前玩家", current_player, "手牌", Card.cards_without_suit(self.players[current_player]["cards"]))
            move = self.make_move(current_player)
            # print("当前出牌", move)
            if not move:
                move = []
            print("当前出牌", move)
            if move:
                self.current_cards = move
                self.current_cards_user = current_player
            print("玩家", current_player, "出牌", Card.cards_without_suit(move) if move else "不出")
            # print("手牌更新，玩家",current_player,"新的手牌", Card.cards_without_suit(self.players[current_player]["cards"]))

            self.history.append((current_player, move))
            current_player = (current_player + 1) % 3

    def make_move(self, player_id):
        # 基于简单规则的出牌决策
        print("玩家", player_id, "出牌决策")
        is_right = False
        time_limit = 0
        cards = []
        while not is_right and time_limit < 5:
            if not self.current_cards or self.current_cards_user == player_id:
                # 第一轮必须出牌
                self.current_cards = []
                cards = self.first_move(player_id)

            else:
                # 非第一轮出牌，随机选择能压过的牌
                cards = self.second_move(player_id)
                if not cards:
                    # 不出，不需要额外判断
                    is_right = True

            # 如果要出牌，判断是否可以出牌，并且判断是否大于当前出牌
            if cards and check_card_type(cards)[0]:
                if self.current_cards:
                    if cards_greater(cards, self.current_cards):
                        is_right = True
                        cards_remove = cards.copy()
                        self.remove_cards(cards_remove, player_id)
                else:
                    is_right = True
                    cards_remove = cards.copy()
                    # print("self.cards", self.cards) # [137]
                    self.remove_cards(cards_remove, player_id)
                    # print("self.cards", self.cards)  # []
            time_limit += 1
            if is_right:
                return cards

    def remove_cards(self, cards, player_id):
        for card in cards:
            self.players[player_id]["cards"].remove(card)

    def is_game_over(self) :
        game_over = False
        print("--------------------------------------------------")
        for index,player in enumerate(self.players) :
            print("玩家", index, "手牌", Card.cards_without_suit(player["cards"]),"length", len(player["cards"]))
            if len(player["cards"]) == 0 :
                self.last_winner = index
                if player["charactor"] == 1 :
                    player["score"] += self.score
                    self.players[(index + 1) % 3]["score"] -= self.score/2
                    self.players[(index + 2) % 3]["score"] -= self.score/2
                    print("地主获胜，玩家", index, "获得", self.score, "分")
                    print("目前各玩家分数，id0", self.players[0]["score"], "id1", self.players[1]["score"], "id2", self.players[2]["score"])
                else :
                    player["score"] += self.score/2
                    if self.players[(index + 1) % 3]["charactor"] == 1 :
                        self.players[(index + 1) % 3]["score"] -= self.score
                        self.players[(index + 2) % 3]["score"] += self.score/2
                        self.last_winner2 = (index + 2) % 3
                    else:
                        self.players[(index + 1) % 3]["score"] += self.score/2
                        self.players[(index + 2) % 3]["score"] -= self.score
                        self.last_winner2 = (index + 1) % 3
                    print("玩家", index, "获胜，胜者方获得", self.score, "分")
                    print("目前各玩家分数，id0", self.players[0]["score"], "id1", self.players[1]["score"], "id2",
                          self.players[2]["score"])
                self.current_cards = []
                game_over = True
        return game_over

    def first_move(self, player_id):
        """新回合，不用判断大小，可以直接出牌,而且必须出牌"""
        print("玩家", player_id, "first_move")
        cards_list_int = self.players[player_id]["cards"]
        # 手里可以直接出，直接出
        if check_card_type(cards_list_int)[0]:
            print("玩家", player_id, "手牌可以直接出牌", Card.cards_without_suit(cards_list_int))
            return_cards = cards_list_int.copy()
            # 这里要切片，不然是 self.players[player_id]["cards"]的引用！！改变了就会变化而不是不变
            return return_cards

        cards_score, counts, card_position = self.analyse_card(self.players[player_id]["cards"])
        if sum(card_position) == 2:
            # 只有两类牌并且不能全部出，说明是11,2，14，22，不连33，34，检查最大的牌能否大过全场
            print("玩家", player_id, "手牌只有两类牌并且不能全部出")
            last_count = 0
            for count in counts:
                if count>0:
                    last_count = count
            return_cards = cards_list_int[-last_count:]
            if self.players[player_id]["charactor"] == 1:
                if not list_greater_cards(return_cards, self.players[(player_id+1)%3]["cards"]):
                    if not list_greater_cards(return_cards, self.players[(player_id+2)%3]["cards"]):
                        return return_cards
            else:
                if not list_greater_cards(return_cards, self.players[self.landlord]["cards"]):
                    return return_cards
        is_right = False
        time_limit = 0
        return_cards = []
        while not is_right:
            p = random.random()
            # p=0.3
            if p < 0.3:
                # 随机出牌
                return_cards = self.random_first_move(player_id)
                if return_cards:
                    is_right = True
                # print("当前牌组", Card.cards_without_suit(self.players[player_id]["cards"]))
                print("玩家", player_id, "first_move随机出牌random_first_move", Card.cards_without_suit(return_cards) if return_cards else "无结果重新firstmove出牌")
            else:

                return_cards = self.first_move_low_value_cards(cards_list_int)
                if return_cards:
                    is_right = True
                # print("当前牌组", Card.cards_without_suit(self.players[player_id]["cards"]))
                print("玩家", player_id, "first_move最小值出牌move_low_value_cards", Card.cards_without_suit(return_cards) if return_cards else "无结果重新firstmove出牌")
            time_limit += 1
            if time_limit % 500 == 0:
                print("玩家", player_id, "first_move不出牌卡死，卡死次数", time_limit)

        return return_cards

    def second_move(self, player_id):
        """需要判断大小 """
        # 当前回合未结束，根据上一轮出牌，当前手牌，对手手牌进行决策
        print("玩家", player_id, "second_move")
        return_cards = list_greater_cards(self.current_cards, self.players[player_id]["cards"])
        # 随机选择出牌
        if not return_cards:
            print("玩家", player_id, "second_move无牌可出")
            return []
        else:
            p = random.random()
            if p < 0.2:
                print("玩家", player_id, "second_move随机20%不出牌")
                return []
            # 获取字典的键的列表
            keys = list(return_cards.keys())
            # 使用random.choice进行均匀采样
            sampled_key = random.choice(keys)
            sampled_value = return_cards[sampled_key]
            choice = random.choice(sampled_value)
            return_cards = choice
        return return_cards

    def random_first_move(self, player_id):
        return_cards = []
        while not return_cards:
            p = random.random()
            if p < 0.3 :
                target_cards =Card.card_ints_from_string('3h')
            elif p < 0.6 :
                target_cards =Card.card_ints_from_string('3h-3s')
            elif p < 0.8 :
                q = random.random()
                if q < 0.5 :
                    target_cards =Card.card_ints_from_string('3h-4h-5s-6c-7d')
                elif q < 0.7 :
                    target_cards =Card.card_ints_from_string('3h-4h-5s-6c-7d-8h')
                elif q < 0.9 :
                    target_cards =Card.card_ints_from_string('3h-4h-5s-6c-7d-8h-9s')
                else:
                    target_cards =Card.card_ints_from_string('3h-4h-5s-6c-7d-8h-9s-10c')
            elif p < 0.9 :
                q = random.random()
                if q < 0.5 :
                    target_cards =Card.card_ints_from_string('3h-3s-3c-4h')
                else:
                    target_cards =Card.card_ints_from_string('3h-3s-3c-4d-4c')
            elif p < 0.95 :
                target_cards =Card.card_ints_from_string('3h-3s-3c-3d')
            else:
                target_cards =Card.card_ints_from_string('3h-3s-3c-3d-4h-4d')
            return_cards = list_greater_cards(target_cards, self.players[player_id]["cards"])
            # 随机选择出牌
            if return_cards:
                keys = list(return_cards.keys())
                # 使用random.choice进行均匀采样
                sampled_key = random.choice(keys)
                sampled_value = return_cards[sampled_key]
                choice = random.choice(sampled_value)
                if choice == [14,13] or choice == [13,14]:
                    choice = random.choice(sampled_value)
                return_cards = choice
        return return_cards

    def first_move_low_value_cards(self, cards_list_int):
        """出牌时，出最小的牌，3带需要进一步处理"""
        return_cards = []
        length = len(cards_list_int)
        cards_score, counts, card_position = self.analyse_card(cards_list_int)
        start_index = card_position.index(1)
        if start_index != None:
            # 有牌,注意counts和position列表从3牌面，权重0开始，startindex不确定。而cardlist永远从0开始，牌面权重不定
            if counts[start_index] == 4:
                return_cards = self.first_move_low_value_cards(cards_list_int[4 :])
            if counts[start_index] == 3:
                amount = 1
                # 分析多少个连3，不含2
                for i in range(start_index+1, min(int(length/3),12)):
                    if counts[i] == 3:
                        amount += 1
                    else:
                        break
                if sum(counts[start_index:-2])-amount*3 < amount:  #不够带3张
                    return_cards = cards_list_int[0:3*amount]
                else:
                    return_cards = cards_list_int[0:4*amount] # 正常需要带单张或者对子
            if counts[start_index] == 2:
                amount = 1
                for i in range(start_index+1, min(int(length/ 2),12)):
                    # 分析多少个连2，不含2,并且考虑剩的牌不应该有很多三
                    add ={2:1,3:1,4:2,5:2,6:3}
                    if 1 < counts[i] < 4 and sum(counts[start_index:amount+1]) <= 2*amount+add[amount+1]:
                        amount += 1
                    else:
                        break
                if amount > 2:  # 连对
                    return_cards = cards_list_int[0:2 * amount]
                else :
                    return_cards = cards_list_int[0:2]

            if counts[start_index] == 1:
                amount = 1
                for i in range(start_index+1, min(int(length),12)) :
                    # 分析多少个连1，不含2,并且考虑剩的牌不应该多很多
                    # add = {2: 4, 3: 8, 4: 12, 5: 16, 5: 2, 6 : 3}
                    if 0 < counts[i] < 4 :
                        amount += 1
                    else:
                        break
                if amount > 4:  # 顺子
                    start = start_index
                    for card in cards_list_int:
                        if card & 0x0F == start and start < start_index+amount:
                            start += 1
                            return_cards.append(card)
                else :
                    return_cards = cards_list_int[0:1]

        return return_cards


    def analyse_card(self, cards:List[int]):
        """分析牌面分数，统计牌的种类和数量"""
        cards_without_suit = Card.cards_without_suit(cards)
        cards_list = cards_without_suit.split("-")
        cards_score = self.cards_score(cards_list)
        # CARDS = '3-4-5-6-7-8-9-10-J-Q-K-A-2-BJ-CJ'.split('-')
        # CARD_IDX = {c : w for w, c in enumerate(CARDS)}
        counts = list([0] * 15)
        card_position = list([0] * 15)
        for card in cards_list:
            counts[CARD_IDX[card]] += 1
            card_position[CARD_IDX[card]] = 1
        return cards_score, counts, card_position

    @staticmethod
    def cards_score(cards:List[str]):
        # 简单计算牌面分数
        score = 0
        for card in cards:
            score += CARD_IDX[card]
        return score

    def save_record(self, game_record):
        """按照预设格式保存记录，序列格式 ：初始牌面<sp>地主牌<sp>评估抢分<sp>自身角色<sp>出牌历史<角色><动作><角色><动作><角色><动作><角色><动作>"""
        def convert_cards(cards):
            for index in range(len(cards)):
                if cards[index] == 'BJ':
                    cards[index] = 'B'
                if cards[index] == 'CJ':
                    cards[index] = 'C'
                if cards[index] == '10':
                    cards[index] = 'T'

        # 转换手牌
        initial_hands_list = []
        for player in self.players:
            for initial_hand in game_record['initial_hands']:
                initial_hands = Card.cards_without_suit(initial_hand).split("-")
                convert_cards(initial_hands)
                initial_hands_list.append("".join(initial_hands))

        landlord_cards = Card.cards_without_suit(game_record['landlord_cards']).split("-")
        convert_cards(landlord_cards)
        landlord_cards = "".join(landlord_cards)

        bids_convert ={0:"r", 1:"s", 2:"m", 3:"b" }
        bids = [bids_convert[bid] for bid in game_record['bids']]

        landlord = game_record['landlord']
        characters = ['', '', '']
        characters[landlord] = "L"
        characters[(landlord+1)%3] = "P"
        characters[(landlord+2)%3] = "p"

        history_old = game_record['history']
        history = ""
        for action in history_old:
            character = characters[action[0]]
            if action[1]:
                cards_play = Card.cards_without_suit(action[1]).split("-")
                convert_cards(cards_play)
                history += (character + "".join(cards_play))
            else:
                history += (character + "N")

        result = ["", "", ""]
        winner = [game_record['winner']]
        if self.last_winner2 is not None:
            winner.append(self.last_winner2)
        for i in range(3):
            result[i] = "W" if i in winner else "F"

        separator = ">"
        record_list = []
        for i in range(3):
            record_list.append(initial_hands_list[i] + separator + landlord_cards + separator + str(bids[i]) + separator + characters[i]+ separator + history + separator + result[i])

        print("一局玩家记录\n")
        for record in record_list:
            print(record, "\n")
            with open("records_history.txt", "a") as f:
                f.write(record + "\n")


    def simulate_game(self) :
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        self.distribute_cards()

        game_record = {
            'initial_hands' : [player['cards'].copy() for player in self.players],
            'landlord_cards' : self.landlord_cards,
            'bids': [],
            'score' : None,
            'landlord' : None,
            'winner' : None,
            'history' : []
        }

        self.bid_for_landlord()

        game_record['score'] = self.score
        game_record['landlord'] = self.landlord
        game_record['bids'] = [player['bid'] for player in self.players]

        self.history = []
        self.play()
        game_record['history'] = self.history

        game_record['winner'] = self.last_winner

        self.save_record(game_record)

        return game_record


# 生成数据
num_games = 1
game_records = []
game = LandlordGame()
for i in range(num_games) :
    game_record = game.simulate_game()
    game_records.append(game_record)
    i += 1

# 打印前3局的对局记录作为示例
for i, record in enumerate(game_records[:num_games]) :
    print("==========================================================================")
    print(f"Game {i + 1}:")
    print(f"  Initial Hands: {record['initial_hands']}")
    print(f"  Landlord Cards: {record['landlord_cards']}")
    print(f"  score: {record['score']}")
    print(f"  Landlord: Player {record['landlord']}")
    print(f"  Winner: Player {record['winner']}")
    print(f"  History: {record['history']}")
