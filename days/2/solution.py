from typing import List


def part1(data: str) -> int:
    reports = data.split('\n')
    reportResults = []
    for report in reports:
        reportIsIncreasing = None
        levels = list(map(int, report.split(' ')))
        result = True
        for i, level in enumerate(levels):
            if (i == 0): continue
            diff = levels[i - 1] - level
            if (abs(diff) < 1 or abs(diff) > 3): 
                result = False
                break
            isIncreasing = diff > 0
            if (reportIsIncreasing == None): reportIsIncreasing = isIncreasing
            if (isIncreasing != reportIsIncreasing):
                result = False
                break
        reportResults.append(result)
    return reportResults.count(True)

def part2(data: str) -> int:
    def validateReport(levels: List[int]):
        reportIsIncreasing = None
        result = True
        for i, level in enumerate(levels):
            if (i == 0): continue
            diff = levels[i - 1] - level
            if (abs(diff) < 1 or abs(diff) > 3): 
                result = False
                break
            isIncreasing = diff > 0
            if (reportIsIncreasing == None): reportIsIncreasing = isIncreasing
            if (isIncreasing != reportIsIncreasing):
                result = False
                break
        return result
        
    reports = data.split('\n')
    reportResults = []
    for report in reports:
        levels = list(map(int, report.split(' ')))
        result = validateReport(levels)
        if (result == False):
            for i, _ in enumerate(levels):
                result = validateReport(levels[:i] + levels[i + 1:])
                if (result == True): break
        reportResults.append(result)
    return reportResults.count(True)