import cv2.cv2


class Median_pt:
    def __init__(self, list):
        self.List      = list

    def calculate(self):
        temp_x = []
        temp_y = []
        for i in range(0, len(self.List), 1):

            if i + 1 == len(self.List) - 1:
                st_x, st_y = self.List[i][0], self.List[i][1]
                nd_x, nd_y = self.List[i + 1][0], self.List[i + 1][1]
                rd_x, rd_y = nd_x, nd_y
            elif i == len(self.List) - 1:
                st_x, st_y = self.List[i][0], self.List[i][1]
                nd_x, nd_y = st_x, st_y
                rd_x, rd_y = nd_x, nd_y
            else:
                st_x, st_y = self.List[i][0], self.List[i][1]
                nd_x, nd_y = self.List[i + 1][0], self.List[i + 1][1]
                rd_x, rd_y = self.List[i + 2][0], self.List[i + 2][1]

            temp = []
            temp.append(st_x)
            temp.append(nd_x)
            temp.append(rd_x)
            temp.sort()
            temp_x.append(temp[1])
            # if st_x <= nd_x <= rd_x or rd_x <= nd_x <= st_x:
            #     temp_x.append(nd_x)
            # elif nd_x <= st_x <= rd_x or rd_x <= st_x <= nd_x:
            #     temp_x.append(st_x)
            # else:
            #     temp_x.append(rd_x)

            temp = []
            temp.append(st_y)
            temp.append(nd_y)
            temp.append(rd_y)
            temp.sort()
            temp_y.append(temp[1])

            # if st_y <= nd_y <= rd_y or rd_y <= nd_y <= st_y:
            #     temp_y.append(nd_y)
            # elif nd_y <= st_y <= rd_y or rd_y <= st_y <= nd_y:
            #     temp_y.append(st_y)
            # else:
            #     temp_y.append(rd_y)

        result = []
        for i in range(0,len(temp_x),1):
            result.append((temp_x[i],temp_y[i]))
        # print(result)

        return result