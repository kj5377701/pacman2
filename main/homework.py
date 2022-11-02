words = input().split()

li = []

func = {
    '+': int.__add__,
    '-': int.__rsub__,
    '*': int.__mul__,
    '/': int.__rfloordiv__,
}
for w in words:
    li.append(int(w) if w not in '+-*/' else func[w](li.pop(), li.pop()))
print(li[0])

