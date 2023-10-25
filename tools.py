def is_in_rectangle(target, point1, point2):
    x, y = target
    x1, y1 = point1
    x2, y2 = point2
    return (x1 <= x <= x2 and y1 <= y <= y2) or (x2 <= x <= x1 and y2 <= y <= y1)

def is_rectangle(rectangle):
    if isinstance(rectangle,(tuple, list)) and len(rectangle) == 2:
        if isinstance(rectangle[0],(tuple,list)) and len(rectangle[0]) == 2 :
            if isinstance(rectangle[1],(tuple,list)) and len(rectangle[1]) == 2 :
                for item in rectangle[0]:
                    try:
                        float(item)
                    except:
                        return False
                for item in rectangle[1]:
                    try:
                        float(item)
                    except:
                        return False
                return True
    return False


if __name__ == "__main__":
    # print(is_in_rectangle((2,2),(1,1),(3,3)))
    # print(is_in_rectangle((2,2),(3,3),(1,1)))
    # print(is_in_rectangle((3,3),(1,1),(2,2)))

    print(is_rectangle([(1,1),(3,3.5)]))
    print(is_rectangle([(),()]))