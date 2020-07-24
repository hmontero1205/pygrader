"""rubric_item.py: Rubric item definition"""

class RubricItem():
    """Representation of a rubric item

    Attributes:
        table_item: the number of the item (e.g. A1, C3, etc)
        desc: tuple containing point value and desc of item
        tester: callback function to grade this item
    """

    def __init__(self, table_item, desc, funct):
        self.table_item = table_item
        self.desc = desc
        self.tester = funct
