import sys
#sys.path.insert(0, "../printing")
import os
sys.path.append(os.path.abspath('../printing'))
import printing as p


class RubricItem():

    def __init__(self, table_item, desc, points, funct):
        '''
            table: the table letter (e.g. A, D, etc)
            table_item: the item number of the subtable (e.g. A1, C3, etc)
            desc: the description of the item
            points: you get it
            funct: callback function to grade the item
        '''
        self.table_item = table_item
        self.desc = desc
        self.points = points
        self.tester = funct

    # def test_item(self):
    #     while True:
    #         # print info text 
    #         p.prGreen('Grading: {}'.format(self.table_item))

    #         for i, d in enumerate(self.desc):
    #             p.prLightPurple("\t{}.{} ({}p): {}".format(self.table_item, i+1, self.points[i], d))
    #         p.prCyan('-'*85)

    #         self.funct()

    #         p.prCyan('-'*85)
    #         usr_input = input("\033[91mDo you want to run the test again [Y/(n)]? \033[00m")

    #         if usr_input != 'Y':
    #             break

    #     p.prCyan('-'*85)
    #     p.prGreen("End test of {}".format(self.table_item))
    #     p.prCyan('='*85)
    #     print('\n\n')

def fun():
    print('hello from fun')

if __name__ == '__main__':
    p.prCyan("FUCK")
    r = RubricItem('A1', 'test description', 5, fun)

    r.tester()
