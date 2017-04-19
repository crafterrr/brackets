def ispow2(n):
    if n & (n - 1) == 0:
        return True
    return False


class SegmentTree:
    def __init__(self, string):
        """ Class initialization """
        self.tree = []
        while not ispow2(len(string)):
            string += 'D'
        self.flayer = [self.__morph(bracket) for bracket in string]
        # print(self.flayer)
        self.tree = [(0, 0, 0) for i in range(0, len(self.flayer) * 2 + 1)]
        self.__build(self.flayer, 1, 0, len(string))

    def __morph(self, bracket):
        if bracket == '(':
            return (1, 0, 0)
        elif bracket == ')':
            return (0, 1, 0)
        else:
            return (0, 0, 0)


    def __getcounts(self, partition):
        opened = 0
        closed = 0
        completed = 0
        for part in partition:
            closed += part[1]
            tempclosed = part[1]
            if opened > 0:
                if tempclosed >= opened:
                    completed += opened
                    closed -= opened
                    opened = 0
                elif tempclosed != 0:
                    completed += tempclosed
                    opened -= tempclosed
                    closed -= tempclosed
            opened += part[0]
            completed += part[2]
        return opened, closed, completed

    def __build(self, flayer, current, left, right):
        """ Private function to build the tree """
        left = int(left)
        right = int(right)
        if left == right - 1:
            self.tree[current] = flayer[left]
        else:
            mid = (left + right) / 2
            self.__build(flayer, current * 2, left, mid)
            self.__build(flayer, current * 2 + 1, mid, right)
            temp = []
            temp.append(self.tree[current * 2])
            temp.append(self.tree[current * 2 + 1])
            self.tree[current] = self.__getcounts(temp)

    def __query(self, current, sl, sr, l, r):
        """ Private version of query function """
        if l > r:
            return (0, 0, 0)
        if l == sl and r == sr:
            self.answer.append(self.tree[current])
        else:
            mid = (sl + sr) // 2
            self.__query(current * 2, sl, mid, l, min(r, mid))
            self.__query(current * 2 + 1, mid + 1, sr, max(l, mid + 1), r)
        # print(self.answer)
        answer = self.__getcounts(self.answer)
        return answer

    def query(self, l, r):
        """ Public version of query function """
        self.answer = []
        q = self.__query(1, 1, len(self.flayer), l, r)
        return q[2]

    def __str__(self):
        i = 1
        answer = ''
        while (i < len(self.tree)):
            answer += str(self.tree[i: i*2]) + '\n'
            i *= 2
        return answer

# brackets = input()
# l, r = map(int, input().split())
brackets = '))(()()'
l, r = 1, 8
tree = SegmentTree(brackets)
print(tree)
print(tree.query(l, r))
