def knapSack(f, t, jml):
    n = len(jml)
    table = [[0 for x in range(f + 1)] for x in range(n +
1)]
    for i in range(n + 1):
        for j in range(f + 1):
            if i == 0 or j == 0:
                table[i][j] = 0
            elif t[i - 1] <= j:
                table[i][j] = max(jml[i - 1]
                                + table[i - 1][j - t[i
- 1]], table[i - 1][j])
            else:
                table[i][j] = table[i - 1][j]
    return table[n][f]
def Penyelesaian():
    jml = [5,10,55]
    t = [2,6,10]
    f = 2
    return print(knapSack(f, t, jml))

if __name__ == "__main__":
    Penyelesaian()
