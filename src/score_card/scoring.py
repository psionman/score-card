# scoring.py

def calculate_score(contract, declarer, tricks, vulnerable, our_contract):
    level, strain, doubled = _parse_contract(contract)

    target = 6 + level
    made = tricks - target

    is_vul = _is_vulnerable(declarer, vulnerable)

    declarer_factor = 1 if our_contract else -1
    if made >= 0:
        return _score_made(
            level, strain, doubled, made, is_vul) * declarer_factor
    else:
        return _score_down(made, doubled, is_vul) * declarer_factor

def _score_made(level, strain, doubled, overtricks, is_vul):
    # trick value
    if strain in ["C", "D"]:
        trick_value = 20
    elif strain in ["H", "S"]:
        trick_value = 30
    else:  # NT
        trick_value = 30

    base = level * trick_value

    if strain == "NT":
        base += 10  # NT bonus

    # apply doubles
    if doubled == 1:
        base *= 2
    elif doubled == 2:
        base *= 4

    score = base

    # game / partscore bonus
    if base >= 100:
        score += 500 if is_vul else 300
    else:
        score += 50

    # slam bonuses
    if level == 6:
        score += 750 if is_vul else 500
    elif level == 7:
        score += 1500 if is_vul else 1000

    # insult bonus
    if doubled == 1:
        score += 50
    elif doubled == 2:
        score += 100

    # overtricks
    if doubled == 0:
        if strain in ["C", "D"]:
            score += overtricks * 20
        else:
            score += overtricks * 30
    else:
        if is_vul:
            score += overtricks * (200 if doubled == 1 else 400)
        else:
            score += overtricks * (100 if doubled == 1 else 200)

    return score

def _score_down(made, doubled, is_vul):
    down = -made  # positive number

    if doubled == 0:
        return -down * (100 if is_vul else 50)

    penalties = 0

    if is_vul:
        penalties += 200
        penalties += (down - 1) * 300
    else:
        if down >= 1:
            penalties += 100
        if down >= 2:
            penalties += 200
        if down >= 3:
            penalties += 200
        if down >= 4:
            penalties += (down - 3) * 300

    if doubled == 2:
        penalties *= 2

    return -penalties

def _parse_contract(contract: str):
    contract = contract.upper().strip()

    doubled = 0
    if contract.endswith("XX"):
        doubled = 2
        contract = contract[:-2]
    elif contract.endswith("X"):
        doubled = 1
        contract = contract[:-1]

    if contract.endswith("NT"):
        strain = "NT"
        level = int(contract[:-2])
    else:
        strain = contract[-1]
        level = int(contract[:-1])

    return level, strain, doubled

def _is_vulnerable(declarer, vulnerable):
    if vulnerable == "Both":
        return True
    if vulnerable == "None":
        return False
    if vulnerable == "NS":
        return declarer in ["N", "S"]
    if vulnerable == "EW":
        return declarer in ["E", "W"]
    return False
