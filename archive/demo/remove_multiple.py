# if remove team selected 
  # get a list of team players 
  # for each player in team list of players 
    # find matching item in league view players
    # delete item in league view players










test = [('nick', 'beef', 10),('james', 'beef', 10),('kirk', 'beef', 10),('alfred', 'beef', 10),('allison', 'beef', 10)]

# abc sorting would be faster 
# binary search algortihm 
# recursive - remove from target list 
# keep track of matche sin separate list

def remove_league_view_multiple(targets, lst, ret=[]):
    lst.sort(key=my_sort)
    #targets.sort()
    #print(lst)

    for el in targets:
      #print(el)
      binary_search(lst, el, ret)
    
    return ret

def my_sort(x):
    return x[0]

def binary_search(lst, target, ret=[]):
    left = 0 
    right = len(lst)-1
    #middle = left // right 

    while left <= right:
        middle = left + (right - left) // 2
        #print(middle, left, right)
        name = lst[middle][0]
        if target == name:
            print(target, name)
            #append index of list searched
            ret.append(name) 
            return ret
        elif target > lst[middle][0]:
            left = middle + 1 
        elif target < lst[middle][0]:
            right = middle - 1  
    return
            
result = remove_league_view_multiple(['nick', 'alfred', 'abc', 'kirk'], test)

print(result)


def binary_search_test(lst, target, ret=[]):
    left = 0 
    right = len(lst)-1

    while left <= right:
        middle = left + (right - left) // 2
        #print(middle, left, right)
        if target == lst[middle]:
            #append index of list searched
            ret.append(middle)
            return ret
        elif target > lst[middle]:
            left =  middle + 1 
        elif target < lst[middle]:
            right = middle - 1 


test = [1,2,3,4,5,6,7,8,9,10]

#result_test = binary_search_test(test, 5)
#print(result_test)
