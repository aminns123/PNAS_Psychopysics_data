"""Function definitions extracted from supplied code; source lines in provenance.
No top-level analysis scripts are executed. Numerical bodies are preserved.
"""
import numpy as np
from numpy import real
from math import factorial
from itertools import combinations

# LIB001 source lines 1626-1636
def condition1(lisT, n):
	for j in range(len(lisT)-1, 0, -1):
		if lisT[j] >= n:
			lisT[j-1] += 1
			if lisT[j-1]+1 < n:  # <=
				lisT[j] = lisT[j-1]+1
			elif lisT[j-1]+1 >= n:  # >
				lisT[j] = lisT[j]
		elif lisT[j] != n:
			pass
	return lisT

# LIB001 source lines 1641-1655
def condition2(lisT, n):
	j = len(lisT)-1
	found = False
	if lisT[len(lisT)-1] >= n-1:  # ==, >= n
		while found == False:
			if lisT[j] <= lisT[j-1]+1:
				pass
			elif lisT[j] > lisT[j-1]+1:
				lisT[j-1] += 1
				lisT[j] = lisT[j-1]+1
				found = True
			j += -1
	elif lisT[len(lisT)-1] != n-1:  # n
		pass
	return lisT

# LIB001 source lines 1660-1669
def condition3(lisT, n):
	"""
	 If any element is greater than n, then reset value.
	"""
	for x in range(1, len(lisT), 1):
		if lisT[x] >= n-1:  # >= n
			lisT[x] = lisT[x-1]+1
		elif lisT[x] < n-1:  # < n
			pass
	return lisT

# LIB001 source lines 1674-1687
def endCondition(lisT, n):
	count = 1

	if lisT[len(lisT)-1] >= n-1:
		count = 0
		for i in range(len(lisT)-1, 0, -1):
			if (lisT[i] == lisT[i-1]+1):
				count += 0
			elif (lisT[i] != lisT[i-1]+1):
				count += 1
	elif lisT[len(lisT)-1] != n-1:
		pass

	return count

# LIB001 source lines 1692-1705
def removeErrorIndex(listIndex, n):
    valuePops = []
    for j in range(len(listIndex)):
        # print(listIndex[j])
        if n in listIndex[j]:
            # print('pop:',listIndex[j][:])
            valuePops.append(listIndex[j][:])
        elif n not in listIndex[j]:
            pass
    # print(valuePops)
    for i in range(len(valuePops)):
        listIndex.remove(valuePops[i])
    # print(len(listIndex))
    return listIndex

# LIB001 source lines 1710-1716
def conditionP1End(pIndexList, n):
    count = 1
    if pIndexList[0] == n-1:
        count = 0
    elif pIndexList[0] < n-1:
        count = 1
    return count

# LIB001 source lines 1802-1807
def listCombitorial(n, r):
    pipList = []
    # testA   = find_indexPop(n, r, pipList)
    testA   = find_indexPop_Complete(n, r, pipList)
    testA   = removeErrorIndex(testA, n)  
    return testA

# LIB001 source lines 1811-1862
def find_indexPop_Complete(n,r, popList):
    if int(n-r) == 1:
        p = n-r
        n = n+1
        pIndexList = list(np.arange(0, p, 1))
        popList.append(pIndexList[:])
        # print(pIndexList)
        pS  = len(pIndexList)
        end = False
        while end == False:
            pIndexList[pS-1] += 1
            popList.append(pIndexList[:])
            endValue = conditionP1End(pIndexList, n)
            
            if endValue == int(0):
                end = True
            elif endValue > 0:
                pass
    elif int(n-r) > 1:
        p = n-r
        n = n+1
        pIndexList = list(np.arange(0, p, 1))
        popList.append(pIndexList[:])
        # print(pIndexList)
        pS = len(pIndexList)
    
        end = False
        while end == False:
            pIndexList[pS-1] += 1
            pIndexList = condition1(pIndexList, n)
            pIndexList = condition2(pIndexList, n)
            pIndexList = condition3(pIndexList, n)
    
            # print(pIndexList)
            # popList.append(pIndexList[:])

            if n in pIndexList[:]:
                continue
            elif n not in pIndexList[:]:
                popList.append(pIndexList[:])

            endValue = endCondition(pIndexList, n)
            if endValue == int(0):
                end = True
            elif endValue > 0:
                pass
    elif int(n-r) == 0:
        p          = n-r
        pIndexList = list(np.arange(0, p, 1))
        popList.append(pIndexList[:])
        
    return popList

# LIB001 source lines 4742-4751
def weberContrast(contrast_cpu: [], background_crt,max_crt, logFunction, logStatment:bool):
    maxC        = max_crt # max(contrast_cpu)
    contrast_W  = []
    if logStatment == False:
        for i in range(len(contrast_cpu)):
            contrast_W.append((contrast_cpu[i]-background_crt)/(maxC-background_crt))
    elif logStatment == True:
        for i in range(len(contrast_cpu)):
            contrast_W.append(logFunction((contrast_cpu[i]-background_crt)/(maxC-background_crt)))
    return contrast_W

# LIB001 source lines 20815-20857
def permutationsBootstrapNp(num_permutations: int, value_range: int, list_size: int, sizeList: int):
    """
        Generate a list of unique random permutations (with possible repeated values in each row).

        Parameters:
        ----------
        num_permutations : int
            Total number of unique rows (permutations) to generate.
            
        value_range : int
            Values in each row will be randomly chosen in the range [0, value_range).
            i.e., up to but not including value_range.

        list_size : int
            Length of each row (number of elements per permutation).

        sizeList : int
            Final number of permutations to return (must be <= num_permutations).
            This is useful if you want to generate a large pool of unique rows but only return a subset.

        Notes:
        -----
        - A `set()` is used to ensure all rows are unique.
          Since sets only allow unique items, adding a row (as a tuple) that already exists will be ignored.
        - Each row may contain repeated values (e.g., [1, 1, 3]), but no two rows will be exactly the same.
        - If not enough unique permutations can be generated given the constraints, the function raises an error.
    """
    unique_rows = set() 
    attempts = 0
    max_attempts = 10 * num_permutations  # prevent infinite loops

    while len(unique_rows) < num_permutations and attempts < max_attempts:
        row = tuple(np.random.randint(0, value_range, size=list_size))
        unique_rows.add(row)
        attempts += 1

    if len(unique_rows) < sizeList:
        sizeList = len(unique_rows)-1
        print('actual permutation: ', sizeList)
        # raise ValueError("Could not generate enough unique rows. Try increasing value_range or list_size.")

    # Convert to NumPy array
    return np.array(list(unique_rows)[:sizeList])

# LIB001 source lines 22354-22358
def factorialN(x):
    value = 1
    for i in range(1,int(x)+1, 1):
        value = value*i
    return value

# LIB001 source lines 22363-22368
def nChooseR_list(listData: [], sample_Size):
    n = len(listData)
    r = sample_Size

    value = factorialN(n)/(factorialN(r)*(factorialN(n-r)))
    return value

# LIB001 source lines 22457-22469
def singleListpop(arrayToPop, arrayIndex):
    newList  = []
    tickList = list(np.zeros(len(arrayToPop)))
    for i in range(len(arrayIndex)):
        j            = arrayIndex[i]
        tickList[j] += 1

    for m in range(len(tickList)):
        if tickList[m] == 0:
            newList.append(arrayToPop[m])
        elif  tickList[m] > 0:
            pass
    return newList

# LIB001 source lines 22473-22490
def createCombitorialList(listData: [], sample_Size):
    Cnr         = nChooseR_list(listData, sample_Size)
    r           = sample_Size
    n           = len(listData)
    newList     = [[] for x in range(int(Cnr))]
    ArrayWhole  = [listData for x in range(int(Cnr))]
    popList     = listCombitorial(n, r)
    # e.g. n = 4, r = 2, Cnr = 6. Therefore j -> 6, i-> 2, index->4 

    for j in range(len(popList)):
        ArrayNew = ArrayWhole[j]
        popArray = popList[j]
        ArrayNew = singleListpop(ArrayNew, popArray)
        newList[j].append(ArrayNew)

    # newList = newList[0]        
    # outList = listReturn_sequence(newList, Cnr)
    return newList

