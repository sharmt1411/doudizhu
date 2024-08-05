from doudizhu import Card, new_game,check_card_type,cards_greater,list_greater_cards

cards_groups = new_game()
for cards_group in cards_groups:
    Card.print_pretty_cards(cards_group)
    print(cards_group)
    print(Card.cards_without_suit(cards_group))
#   [ 2 ♣ ], [ A ♠ ], [ 7 ❤ ]
# [140, 27, 36]
# 2-A-7

test_four_two = Card.card_ints_from_string('2c-2d-2h-2s-BJ-CJ')
test_four_two2 = Card.card_ints_from_string('Ac-Ad-Ah-As-BJ-CJ')

print(check_card_type(test_four_two))
print(check_card_type(test_four_two2))
# (True, [('four_two_solo', 13)])
# if check_card_type(test_four_two)[0]:
#     print('four_two_solo')


chain = Card.card_ints_from_string('3c-4d-5h-6s-7s-8h-9h')
bomb = Card.card_ints_from_string('8h-8s-8d-8c')
rocket = Card.card_ints_from_string('BJ-CJ')
print(cards_greater(chain, bomb))
# (False, 'solo_chain_7')

def PrettyPrint(cards_gt):
 for card_type, cards_list in cards_gt.items():
     print('card type: {}'.format(card_type))
     for card_int in cards_list:
         Card.print_pretty_cards(list(card_int))

cards_candidate = Card.card_ints_from_string('CJ-Ah-As-Ac-Kh-Qs-Jc-10h-10s-10c-10d-9h-7c-7d-5c-5s')
cards_two = Card.card_ints_from_string('Jh-Jc')
cards_none = Card.card_ints_from_string('3h')
cards_chain_solo = Card.card_ints_from_string('5h-6h-7s-8c-9d')
cards_trio_two = Card.card_ints_from_string('6h-6s-6c-3d-3c')
greater_cards = list_greater_cards(cards_none, cards_candidate)
print(greater_cards)
# print(Card.cards_without_suit(greater_cards))
PrettyPrint(greater_cards)
# {'pair': [[43, 27]], 'bomb': [[135, 39, 71, 23]]}
# card type: pair
#   [ A ❤ ], [ A ♠ ]
# card type: bomb
#   [ 10 ♣ ], [ 10 ❤ ], [ 10 ♦ ], [ 10 ♠ ]
