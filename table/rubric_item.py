"""rubric_item.py: Rubric item definition"""

class RubricItem():
    """Representation of a rubric item

    Attributes:
        table: the table letter (e.g. A, B, etc)
        table_item: the number of the item (e.g. A1, C3, etc)
        desc: the desciption of this item
        points: value of this item
        tester: callback function to grade this item
    """

    def __init__(self, table_item, desc, points, funct):
        self.table_item = table_item
        self.desc = desc
        self.points = points
        self.tester = funct
