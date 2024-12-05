from typing import List


def part1(data: str) -> int:
    rows = data.split('\n')
    lists: List[List[int]] = []
    for row in rows:
        numbers = row.split('   ')
        for i, number in enumerate(numbers):
            if i >= len(lists): lists.append([])
            lists[i].append(int(number))

    for list in lists:
        list.sort(reverse=True)

    results = 0
    for i, leftValue in enumerate(lists[0]):
        rightValue = lists[1][i]
        results += abs(rightValue - leftValue)
        
    return results


def part2(data) -> int:
    rows = data.split('\n')
    leftList = []
    rightList = []
    for row in rows:
        leftNumber, number = row.split('   ')
        leftList.append(int(leftNumber))
        rightList.append(int(number))

    leftList.sort()
    rightList.sort()
    rightNumbersMap = {}
    for number in rightList:
        if number not in rightNumbersMap:
            rightNumbersMap[number] = 0
        rightNumbersMap[number] += 1


    results = 0
    for leftValue in leftList:
        if leftValue not in rightNumbersMap:
            continue
        
        results += leftValue * rightNumbersMap[leftValue]
        
    return results