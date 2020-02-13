import numpy as np

def SeqRouter(x, s):
    # in array x
    # start route s
    # out array y
    N = len(x)
    y = np.zeros(len(x))
    for i in range(len(x)):
        j = i - s if i - s >= 0 else N - s + i
        y[i] = x[j]
    return y

def Route4Test(x):
    # Try all route options
    for i in range(4):
        print(x, SeqRouter(x, i))

def Seq(s):
    x0 = np.zeros(4)
    x0[0:s] = np.arange(1, s+1, 1)
    x1 = np.arange(s+1, s+5, 1)
    return x0, x1

def Seq(n, s):
    x0 = np.zeros(n)
    x0[0:s] = np.arange(1, s+1, 1)
    return x0

def Seq2x8(n0, n1):
    x0 = np.zeros(8)
    x0[0:n0] = np.arange(1, n0+1, 1)
    x1 = np.zeros(8)
    x1[0:n1] = np.arange(n0+1, n0+1+n1, 1)
    return x0, x1

def RouteToUniqueAddr(x, la, ga):
    #print("la: {}".format(la))
    la = la.astype('int')
    # data x, local address la, global address ga
    y = np.zeros(len(x))
    ay = np.zeros(len(x))
    for i in range(len(x)):
        if x[i] > 0:
            y[la[i]] = x[i]
            ay[la[i]] = ga[i]
    return y, ay

def Merge2x4To8(x0, x1):
    # find the first '0' in x1
    s0, s1 = 0, np.min(np.argwhere(x0 == 0))
    print(s0, s1)
    a0 = np.arange(0, s1, 1)
    la0 = a0 % 4
    a1 = np.arange(s1, s1 + 4, 1)
    la1 = a1 % 4

    x0_0, a0_0 = RouteToUniqueAddr(x0, la0, a0)
    x1_0, a1_0 = RouteToUniqueAddr(x1, la1, a1)

    # 'cross' outputs
    x0_1, a0_1 = np.append(x0_0[:2], x1_0[:2]), np.append(a0_0[:2], a1_0[:2])
    x1_1, a1_1 = np.append(x0_0[2:], x1_0[2:]), np.append(a0_0[2:], a1_0[2:])

    la0 = (2 * a0_1 // 4 + a0_1 % 4).astype('int')
    la1 = (2 * a1_1 // 4 + a1_1 % 4).astype('int')

    print(a1_1, la1)

    x0_2, a0_2 = RouteToUniqueAddr(x0_1, la0, a0_1)
    x1_2, a1_2 = RouteToUniqueAddr(x1_1, la1, a1_1)
    y = np.append(x0_2, x1_2)
    print(y)
    return y

def Merge2x8To16(x0, x1):
    h0 = np.min(np.arghwere(x0 == 0)) if sum(x0 == 0) > 0 else 8
    h1 = np.min(np.argwhere(x1 == 0)) if sum(x1 == 0) > 0 else 8
    s0, s1, s2 = 0, h0, h1
    a = np.zeros(16)
    x = np.append(x0, x1)
    a[0:s1] = np.arange(0, s1, 1).astype('int')
    a[8:8+s2] = np.arange(s1, s1+s2, 1).astype('int')
    print("x : {}".format(x))
    print("a : {}".format(a))
    ia = np.arange(0, 16, 1).astype('int') // 4
    la0 = (a % 4).astype('int')
    #la0 = ((a+ia) % 4).astype('int')

    y_0 = np.array([])
    a_0 = np.array([])
    for i in range(4):
        l, h = int(4 * i), int(4 * (i + 1))
        yy, aa = RouteToUniqueAddr(x[l:h], la0[l:h], a[l:h])
        y_0 = np.append(y_0, yy)
        a_0 = np.append(a_0, aa)

    print("x : {}".format(y_0))
    print("a : {}".format(a_0))

    x_1 = np.zeros(16)
    a_1 = np.zeros(16)
    for i in range(4):
        for j in range(4):
            x_1[4*i + j] = y_0[4*j + i]
            a_1[4*i + j] = a_0[4*j + i]

    print("x : {}".format(x_1))
    print("a : {}".format(a_1))

    y_1 = np.array([])
    a_2 = np.array([])
    la1 = a_1 // 4
    for i in range(4):
        l, h = 4 * i, 4 * (i + 1)
        yy, aa = RouteToUniqueAddr(x_1[l:h], la1[l:h], a_1[l:h])
        y_1 = np.append(y_1, yy)
        a_2 = np.append(a_2, aa)

    x_2 = np.zeros(16)
    a_2 = np.zeros(16)
    for i in range(4):
        for j in range(4):
            x_2[4*i + j] = y_1[4*j + i]
            a_2[4*i + j] = a_1[4*j + i]

    print("y : {}".format(x_2))
    return x_2

def Route16To64(x, start):
    n = np.min(np.argwhere(x == 0)) if sum(x == 0) > 0 else 16
    a = np.zeros(16)
    a[0:n] = np.arange(start, start +n, 1)
    print("x : {}".format(x))
    print("a : {}".format(a))
    la0 = (a % 4).astype('int')
    #la0 = ((a+ia) % 4).astype('int')

    y_0 = np.array([])
    a_0 = np.array([])
    for i in range(4):
        l, h = int(4 * i), int(4 * (i + 1))
        yy, aa = RouteToUniqueAddr(x[l:h], la0[l:h], a[l:h])
        y_0 = np.append(y_0, yy)
        a_0 = np.append(a_0, aa)

    print("x : {}".format(y_0))
    print("a : {}".format(a_0))

    x_1 = np.zeros(16)
    a_1 = np.zeros(16)
    for i in range(4):
        for j in range(4):
            x_1[4*i + j] = y_0[4*j + i]
            a_1[4*i + j] = a_0[4*j + i]

    print("x : {}".format(x_1))
    print("a : {}".format(a_1))

    y_1 = np.array([])
    a_2 = np.array([])
    la1 = (a_1 % 16) // 4
    for i in range(4):
        l, h = 4 * i, 4 * (i + 1)
        yy, aa = RouteToUniqueAddr(x_1[l:h], la1[l:h], a_1[l:h])
        y_1 = np.append(y_1, yy)
        a_2 = np.append(a_2, aa)

    x_2 = np.zeros(16)
    a_3 = np.zeros(16)
    for i in range(4):
        for j in range(4):
            x_2[4*i + j] = y_1[4*j + i]
            a_3[4*i + j] = a_2[4*j + i]

    print("x : {}".format(x_2))
    print("a : {}".format(a_3))

    y_2 = np.zeros(64)
    # Do groups of 4 (one from each quarter
    for i in range(16):
        #print("i: {}".format(i))
        for j in range(4):
            iy = 16 * j + i
            #print("  iy: {}".format(iy))
            if a_3[i] == iy:
                y_2[iy] = x_2[i]

    return y_2
