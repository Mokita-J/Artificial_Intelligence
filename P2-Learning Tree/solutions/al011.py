# -*- coding: utf-8 -*-
"""
Grupo al011
Afonso Carvalho id 93681
Monica Jin id 92532
"""

import numpy as np
import math

def entropy(q):
    if q == 1 or q == 0:
        return 0
    return -(q * math.log(q, 2) + (1 - q) * math.log((1 - q), 2))

def importance(attributes, examples, decisions):
    gain = []
    p = 0
    n = 0
    for i in decisions:
        if i == 0:
            n+=1
        else:
            p+=1
    q = (p)/(p+n)   #probabilidade
    B = entropy(q) #entropia inicial

    for a in attributes:
        pk_0 = nk_0 = 0
        pk_1 = nk_1 = 0
        for i in range(len(examples)):
            if examples[i][a]:
                if decisions[i]:
                    pk_1+=1
                else:
                    nk_1+=1
            else:
                if decisions[i]:
                    pk_0+=1
                else:
                    nk_0+=1

        if (pk_0+nk_0 == 0):
            q_0 = 0
        else:
            q_0 = (pk_0)/(pk_0+nk_0)
        if(pk_1+nk_1 == 0):
            q_1 = 0
        else:
            q_1 = (pk_1)/(pk_1+nk_1)
        sum =(pk_0 + nk_0)/(p + n ) *entropy(q_0) + (pk_1 + nk_1)/(p + n) * entropy(q_1) #entropia inicial

        gain.append((a, B - sum))
    # print("information Gain:", gain)        
    
    maxGain = max(x[1] for x in gain)
    if maxGain <= 0.05:
        return -1
    return [x[0] for x in gain if x[1]==maxGain][0]

def plurality(d):
    if isinstance(d, np.ndarray):
        d = d.tolist()
    t = (d.count(0), d.count(1))
    if t[1] == t[0]:
        return 1
    return t.index(max(t))

def decisionTreeLearning(attributes, examples, classifications, p_exs, p_cla, noise):
    if len(examples) == 0:
        return plurality(p_cla)
    elif(all(elem == classifications[0] for elem in classifications)):
        return int(classifications[0])
    elif len(attributes) == 0:
        return plurality(classifications)
    else:
        maxAt = importance(attributes, examples, classifications)
        if(maxAt == -1 and noise):
            return plurality(classifications)
        if(maxAt == -1):
            maxAt = attributes[0]
        tree = [maxAt]
        at = [x for x in attributes if x!= maxAt]
        for v in [0,1]:
            exs = [] #examples with attribute = v
            cla = [] #classifications of exs
            for i in range(0, len(examples)):
                if examples[i][maxAt]==v:
                    exs.append(examples[i])
                    cla.append(classifications[i])
            subtree = decisionTreeLearning( at, exs, cla, examples, classifications, noise)
            tree.append(subtree)
    return tree

def cutTree(root, left, right):
    if isinstance(left, list) and isinstance(right, list):
        if left == right:
            return left, True
        elif left[0]== right[0]:
            new_root = left[0]
            new_left, leftBool = cutTree(root, left[1], right[1])
            new_right, rightBool = cutTree(root, left[2], right[2])
            if leftBool or rightBool:
                root = new_root
                left = new_left
                right = new_right
    return [root, left, right], False


def createdecisiontree(D,Y, noise = False):
    A = list(range(0, len(D[0])))
    T = decisionTreeLearning(A, D, Y, [], [], noise)
    if isinstance(T, int):
        return [0, T, T]
    smallTree, b = cutTree(T[0], T[1], T[2])
    return smallTree