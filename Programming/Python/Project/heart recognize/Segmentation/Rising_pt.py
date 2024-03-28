import numpy as np

class Rising_pt:
    def __init__(self, C, I, R, A, S, sR, M):
        """
        C:  Center
        I:  Image
        R:  Radius
        A:  Angle
        S:  Standard Length
        sR: Score Radius
        M:  Mode
        """
        self.x      = C[1]
        self.y      = C[0]
        self.I = I
        self.IW= I.shape[1]
        self.IL= I.shape[0]
        self.R = R
        self.A = A
        self.S = S
        self.sR = sR
        self.M = M


    def search_pt(self):
        pt_lst = []
        div = int(360 / self.A)
        for i in range(0, div, 1):
            angle = self.A*i

            radians = np.radians(angle)
            sin = np.sin(radians)
            cos = np.cos(radians)


            div = self.R / self.S


            all_sc = []
            pt_temp = []
            dis =[]
            # print(angle,"......angle")
            # print(sin,cos)
            for k in range(1, int(div)+1, 1):
                pt_x  = int(self.x + (self.S * k) * cos)
                pt_y  = int(self.y - (self.S * k) * sin)
                area_pixel = []
                # pt_lst.append((pt_x,pt_y))

                for p in range(-(self.sR), self.sR+1, 1):
                    x_p = self.sR-abs(p)
                    for q in range(-(x_p - 1), x_p, 1):

                        try:
                            area_pixel.append(self.I[pt_x + q][pt_y + p])
                            sucess = True
                        except:
                            sucess = False
                            pass

                score = sum(area_pixel)
                all_sc.append(score)
                dis.append(k)
                pt_temp.append((pt_x,pt_y))

            if self.M == 1:
                add = int(all_sc.index(max(all_sc)))
                pt_lst.append(pt_temp[add])

            if self.M == 2:
                for i in range(0,len(all_sc)-1,1):
                    slp = all_sc[i+1]-all_sc[i]
                    if slp > 1000 :
                        pt_lst.append((pt_temp[i+1],dis[i+1],angle))
                        break
                    else:
                        pass
        # print(pt_lst)

        return pt_lst