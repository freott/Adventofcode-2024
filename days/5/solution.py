from typing import Dict, List

Rules = Dict[str, List[int]]
Update = List[int]
Updates = List[Update]

def read(data: str):
    rules_str, updates_str = data.split('\n\n')
    rules: Rules = {}
    for rule_str in rules_str.split('\n'):
        before, after = list(map(int, rule_str.split('|')))
        rules.setdefault(before, []).append(after)
        
    updates: Updates = []
    for update_str in updates_str.split('\n'):
        updates.append(list(map(int, update_str.split(','))))
        
    return rules, updates

def validate_update(rules: Rules, update: Update):
    order = []
    for value in update:
        after_values = rules.get(value, [])
        if any(item in after_values for item in order):
            return False
        order.append(value)
        
    return True

def part1(data: str) -> int:
    rules, updates = read(data)
    return sum(
        update[len(update) // 2]
        for update in updates
        if validate_update(rules, update)
    )

def reorder_update(rules: dict, update: list):
    order = []
    for value in update:
        after_values = rules.get(value, [])
        insert_index = next(
            (i for i, item in enumerate(order) if item in after_values),
            len(order)
        )
        order.insert(insert_index, value)
    return order

def part2(data) -> int:
    rules, updates = read(data)
    invalid_updates = [update for update in updates if not validate_update(rules, update)]
    reordered_updates = [reorder_update(rules, update) for update in invalid_updates]
    return sum(
        update[len(update) // 2] 
        for update in reordered_updates
    )