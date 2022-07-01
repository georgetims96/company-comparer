from typing import List

class SimpleFinancialEntry:
  def __init__(self, fields_to_check: List[str]):
    self.fields_to_check = fields_to_check

class ComputedFinancialEntry:
  def __init__(self, expression: str):
    self.expression = expression