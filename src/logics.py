"""This module includes base logics of CalcAPI"""

import re

from fastapi import HTTPException


def validate_input(input_str: str) -> list:
    """Input string validation"""

    results = []
    valid_pattern = re.compile(
        r"""
        \s*                             # space
        ([+-]?)                         # first operand
        \s*                             # space
        (\d+\.?\d*?)                    # first number
        \s*                             # space
        (([+-\/*])\s*(\d+\.?\d*?)\s*)*  # n-operand and number phrase
    """,
        re.X,
    )

    valid_string = valid_pattern.fullmatch(input_str)
    if valid_string:
        results = re.findall(r"[+-\/*]?\s*\d+\.?\d*\s*", valid_string.group(0))
    return results


def expression_count(input_valid_string: list) -> float:
    """Expression math execution"""

    total = 0

    for value in input_valid_string:
        value = value.strip()
        if value[0].isdigit():
            total += float(value)
        elif value[0] == "+":
            total += float(value[1:])
        elif value[0] == "-":
            total -= float(value[1:])
        elif value[0] == "/":
            total = total / float(value[1:])
        else:
            total *= float(value[1:])
    return round(total, 3)


def history_support(CACHE: list, limit: int = 40, status: str = None):
    """History filters execution"""

    limited_history = []

    if CACHE == []:
        raise HTTPException(status_code=404, detail="History is empty")
    if limit and (limit < 1 or limit > 30):
        raise HTTPException(status_code=400, detail="Invalid limit (1:30)")
    if status and (status != "success" and status != "fail"):
        raise HTTPException(status_code=400, detail="Invalid status")
    if limit and (limit >= 1 and limit <= 30) and status is None:
        for value in CACHE[: -limit - 1: -1]:
            limited_history.append(value)
        return limited_history
    elif limit is None and status and (status == "success" or status == "fail"):
        for value in CACHE[::-1]:
            if value["status"] == status:
                limited_history.append(value)
        return limited_history
    elif (
        limit
        and status
        and (limit >= 1 and limit <= 30)
        and (status == "success" or status == "fail")
    ):
        for value in CACHE:
            if value["status"] == status:
                limited_history.append(value)
        return limited_history[: -limit - 1: -1]
    else:
        return CACHE[::-1]
