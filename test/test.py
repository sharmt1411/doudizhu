dict1={0: '2', 1: '3', 2: '4', 3: '5', 4: '6', 5: '7', 6: '8', 7: '9', 8: '>', 9: 'A', 10: 'B', 11: 'C', 12: 'F', 13: 'J', 14: 'K', 15: 'L', 16: 'N', 17: 'P', 18: 'Q', 19: 'T', 20: 'W', 21: 'b', 22: 'm', 23: 'p', 24: 's', 25: 'r', 26: 'E'}
dict2 = {}
for key, value in dict1.items():
    dict2[value] = key

print(dict2)



def transform_string(input_str) :
    # 定义映射字典
    dict1 = {
        '2' : '2 ', '3' : '3 ', '4' : '4 ', '5' : '5 ', '6' : '6 ', '7' : '7 ', '8' : '8 ', '9' : '9 ',
        '>' : '--> ', 'A' : 'A ', 'B' : '小王 ', 'C' : '大王 ', 'F' : '输', 'J' : 'J ', 'K' : 'K ', 'L' : '地主：',
        'N' : '不出 ', 'P' : '下家：', 'Q' : 'Q ', 'T' : 'T ', 'W' : '赢', 'b' : '叫分3', 'm' : '叫分2',
        'p' : '上家：', 's' : '叫分1 ', 'r' : '叫分0 '
    }

    result = []
    i = 0
    length = len(input_str)
    character = None
    while i < length :
        char = input_str[i]

        if char == 'E' :
            # 检查连续的 'E'
            count = 0
            while i < length and input_str[i] == 'E' :
                count += 1
                i += 1
            result.append('<填充>')
        else :
            if char in dict1 :

                if character is None and char in ["L", "P", "p"]:
                    character = char
                    result.append('本局角色：')
                    result.append((dict1[char]).replace('：', ''))
                    result.append('\n开始出牌 ')

                else:
                    if char == character:
                        result.append('自己：')
                    else:
                        result.append(dict1[char])
            else :
                result.append(char)  # 未知字符保持原样
            i += 1

    result = ''.join(result)

    return result


# 测试输入字符串
# input_str = "55556677899TTJKAC>QT4>m>p>L33P66p77LNPKKpNL22PNp5555LNPNp66LQQPAApNLNP33p99LNPNpTTLNPNp8LJP2pCLNPNpAL2PBpNLNP4pJLNPQpK>W"
input_str = "2556666789TJJQ22C>QJ7>m>P>LAAP22pNLNP33p77LT9P22pNLNP4pTLJPApNLNPKQJTpNLNPCpNLNPJpNLAPNpNL3336PNp99LNPNp3L55PNpJJLNPNpKLNPNp44L77PNpNL6PJpALNPNp6LQPNpNLBPNpNL999>F"
output_str = transform_string(input_str)
print(output_str)

# 统计胜利次数及对局记录
# with open('records_history-100000.txt.', 'r', encoding='utf-8') as f:
#     text = f.read()
#
# win_lines = []
# lines = text.split('\n')
# for line in lines:
#     if line.endswith('W'):
#         win_lines.append(line)
#
# win_count = len(win_lines)
# print('胜利次数：', win_count)
#
# with open('win_records.txt', 'w', encoding='utf-8') as f:
#     for line in win_lines:
#         f.write(line + '\n')

