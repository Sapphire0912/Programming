import cv2
import random
import glob as gb
import numpy as np
import pandas as pd
import ECG_BD as ecg_bd
import Rising_pt as Rs
import plotly.express as px
import multi_thres as mult
from PIL import Image
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import scipy.signal as signal

def regress_pt(list,power,C,A):
    angle   = []
    dist    = []
    div = len(list)
    for i in range(0, div, 1):
        ang = list[i][2]
        angle.append(ang)

        a   = (C[1], C[0])
        b   = list[i][0]
        length = dist_pt(a, b)
        dist.append(length)

    # Define input array with angles from 60deg to 300deg converted to radians
    y = np.array(dist)
    # Setting seed for reproducibility
    x = np.array(angle)

    data = pd.DataFrame(np.column_stack([x, y]), columns=['x', 'y'])
    plt.plot(data['x'], data['y'], '.')
    # plt.show()
    for i in range(2, 16):  # power of 1 is already there
        colname = 'x_%d' % i  # new var will be x_power
        data[colname] = data['x'] ** i

    # Initialize a dataframe to store the results:
    col = ['rss', 'intercept'] + ['coef_x_%d' % i for i in range(1, 16)]
    ind = ['model_pow_%d' % i for i in range(1, 16)]
    coef_matrix_simple = pd.DataFrame(index=ind, columns=col)

    # Define the powers for which a plot is required:
    models_to_plot = {1: 231, 3: 232, 6: 233, 9: 234, 12: 235, 15: 236}

    y_point = []
    # Iterate through all powers and assimilate results
    for i in range(1, 16):
        coef_matrix_simple.iloc[i - 1, 0:i + 2], y_pre = linear_regression(data, power=i,
                                                                           models_to_plot=models_to_plot)
        y_point.append(y_pre)

    plt.show()
    plt.clf()

    pd.options.display.float_format = '{:,.2g}'.format

    # print(coef_matrix_simple)
def linear_regression(data, power, models_to_plot):
    # initialize predictors:
    predictors = ['x']
    if power >= 2:
        predictors.extend(['x_%d' % i for i in range(2, power + 1)])

    # Fit the model
    linreg = LinearRegression(normalize=True)
    linreg.fit(data[predictors], data['y'])
    y_pred = linreg.predict(data[predictors])

    # Check if a plot is to be made for the entered power
    if power in models_to_plot:
        plt.subplot(models_to_plot[power])
        plt.tight_layout()
        plt.plot(data['x'], y_pred)
        plt.plot(data['x'], data['y'], '.')
        plt.title('Plot for power: %d' % power)

    # Return the result in pre-defined format
    rss = sum((y_pred - data['y']) ** 2)
    ret = [rss]
    ret.extend([linreg.intercept_])
    ret.extend(linreg.coef_)
    return ret, y_pred

def dist_pt(a,b):
    x = np.array((int(a[0]), int(a[1])))
    y = np.array((int(b[0]), int(b[1])))
    dist = np.sqrt(np.sum(np.square(x - y)))
    return dist

#video-dir
video_dir       ="C:\\Users\\Tim_Lab\\Desktop\\Laptop\\Left ventricle\\All_Data\\Normal\\"
# video_dir       ="C:\\Users\\Tim_Lab\\Desktop\\Program\\Data_division\\Views\\0009_Parasternal Long Axis\\"
video_paths     = gb.glob(video_dir+"*.avi")

for path in video_paths :

    #sample_name
    name        = path.split("\\")[-1]
    category    = "0002_Apical Four Chamber"        # category= path.split("\\")[-2]
    print(name)

    cap         = cv2.VideoCapture(path)
    FPS         = int(cap.get(cv2.CAP_PROP_FPS))

    width       = 800
    height      = 600
    x_bound     = []
    y_bound     = []

    try:
        model_dir   = "C:\\Users\\Tim_Lab\\Desktop\\Program\\Data_division\\Model_anchor\\0002_Apical Four Chamber\\" + name + ".png"
        model       = cv2.imread(model_dir)
    except:
        print(name+"_None")
        continue


    bound                       = np.zeros([600, 800], dtype=np.uint8)
    car_bound                   = np.zeros([600, 800,3], dtype=np.uint8)
    info_msk                    = np.zeros([600, 800], dtype=np.uint8)


    info_msk[100:550, 100:700]  = 255

    pic         = cv2.cvtColor(model, cv2.COLOR_BGR2GRAY)
    image       = cv2.add(pic, np.zeros(np.shape(pic), dtype=np.uint8), mask=info_msk)



    #Finding_Model's_bounder------------------------------------------------------------------------------------------------
    cnt, hierarchy          = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for i in range(0,len(cnt)):
        for q in range(0,len(cnt[i])):

            x_bound.append(cnt[i][q][0][0])
            y_bound.append(cnt[i][q][0][1])
    try:
        x      = (max(x_bound) + min(x_bound))/2
        y      = (max(y_bound) + min(y_bound))/2
        rad_x  = (max(x_bound) - min(x_bound))/2
        rad_y  = (max(y_bound) - min(y_bound))/2

        if rad_x > rad_y:
            radius  = rad_x + 10
        else:
            radius  = rad_y + 10

        center      = (int(x), int(y))
        radius      = int(radius)

        left_B      = int(x) - radius
        top_B       = int(y) + radius
        right_B     = int(x) + radius
        bottom_B    = int(y) - radius

        # image   = image[ bottom_B:top_B, left_B:right_B]
        area_ADD    = cv2.morphologyEx(image,cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3)), iterations = 2)

        t = image.ravel()

        if (t.max()) < 100:
            continue

        else:
            cnt, hierarchy = cv2.findContours(area_ADD, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            hull = []

            for i in range(len(cnt)):
                contour = cnt[i].tolist()

                for k in range(len(contour)):
                    hull.append(contour[k])

            my_array = np.asarray(hull)
            hull = cv2.convexHull(my_array)

            cv2.drawContours(bound, [hull], 0, (255, 255, 255), -1)
            bound = cv2.erode(bound, cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9)), iterations=9)
            cnt_B = cv2.findContours(bound, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
            cv2.drawContours(car_bound, cnt_B, 0, (255, 255, 255), -1)

        # cv2.waitKey(0)

    except:
        print(path)

    ECG_mask    = ecg_bd.roi_region(path, mask_threshold=10, kernel_size=(3, 3), morph_iteration=3)
    count       = 0

    out = cv2.VideoWriter('C:\\Users\\Tim_Lab\\Desktop\\Laptop\\Left ventricle\\frame\\' + name,
                          cv2.VideoWriter_fourcc(*'XVID'), 20.0, (width, height))

    X_cen=[]
    Y_cen=[]
    areac_x=[]
    areac_y=[]
    cav_ar = []
    dt = []
    while(cap.isOpened()):

        ret, frame  = cap.read()
        ECG_mask    = ECG_mask.copy()

        count       = count + 1
        cv2.putText(frame, 'Dection_len_count =  ' + str(count), (20, 15), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 255, 255), 1, cv2.LINE_AA)

        if ret == False:
            break

        cv2.imshow("frame", frame)
        median = cv2.medianBlur(frame, 19)
        img_bl = cv2.blur(frame,(17,17))



        frame_mask      = cv2.bitwise_and(median, ECG_mask)
        median_gr       = cv2.cvtColor(median, cv2.COLOR_BGR2GRAY)
        # ----------------------------------------------------------
        # t = median_gr.ravel()
        # hist = cv2.calcHist([median_gr], [0], None, [256], [0, 256])
        # plt.hist(median_gr.ravel(), 256, [30, 256])
        # plt.show()


        # height = median_gr.shape[0]
        # width = median_gr.shape[1]
        # hst = [0] * 256
        #
        # for x in range(0, width):
        #     for y in range(0, height):
        #         if (30 < median_gr[y, x] < 255):
        #             hst[int(median_gr[y, x])] += 1
        #
        # hist_out = np.zeros((256, 256), np.uint8)
        # for x in range(0, 256):
        #     for y in range(0, 256):
        #         if (hst[x] * 256 / (max(hst) + 0.00001) > 256 - y):
        #             hist_out[y, x] = 255
        # cv2.imshow("hist_out", hist_out)
        # for i in range (0,len(hst),1) :
        #     if hst[i] == 0:
        #         hst[i] = hst[i-1]

        # print(hst)
        # mlt = mult.multi_thres(hst,9,40,220)
        #
        # L, M, H, ZL, LM, MH, HX = mlt.search_max()
        # print(L, M, H, ZL, LM, MH, HX)
        # blk = np.zeros([600, 800], dtype=np.uint8)
        #
        # blk[median_gr < 255] = 255
        # blk[median_gr < H] = 160
        # blk[median_gr < M] = 80
        # blk[median_gr < L] = 0
        # cv2.imshow("blk", blk)
#----------------------------------------------------------
        # print(hist)

        frame_mask      = cv2.cvtColor(frame_mask, cv2.COLOR_BGR2GRAY)
        #
        thresh2         = cv2.adaptiveThreshold(frame_mask, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                         cv2.THRESH_BINARY, 221, 7)
        ret, thresh_inv = cv2.threshold(thresh2, 120, 255, cv2.THRESH_BINARY_INV)
        ECG_mask_gy     = cv2.cvtColor(ECG_mask, cv2.COLOR_BGR2GRAY)
        thresh_inv      = cv2.bitwise_and(thresh_inv, ECG_mask_gy)
        cv2.imshow("median", median)
        dist_cb         = cv2.distanceTransform(thresh_inv, cv2.DIST_L1, 3)
        # print(np.amax(dist_cb))

        dist_ms         = cv2.distanceTransform(thresh2, cv2.DIST_L1, 3)
        dist_ct         = cv2.distanceTransform(thresh_inv, cv2.DIST_L1, 3)

        cv2.normalize(dist_cb, dist_cb, 0, 1.0, cv2.NORM_MINMAX)
        cv2.normalize(dist_ms, dist_ms, 0, 1.0, cv2.NORM_MINMAX)
        thresh2         = cv2.cvtColor(thresh2, cv2.COLOR_GRAY2RGB)
        thresh2         = cv2.bitwise_and(thresh2, ECG_mask)

        cv2.imshow("dist_cb", dist_cb)

        _, dist = cv2.threshold(dist_cb, 0.6, 255, cv2.THRESH_BINARY)

        dist = cv2.cvtColor(dist, cv2.COLOR_GRAY2RGB)
        thresh_inv = cv2.cvtColor(thresh_inv, cv2.COLOR_GRAY2RGB)
        dist = np.uint8(dist)
        cen = cv2.bitwise_and(dist, car_bound)

#--------------------------------------------------------------------
        cen_gy = cv2.cvtColor(cen, cv2.COLOR_BGR2GRAY)
        cnt_cen, hierarchy = cv2.findContours(cen_gy, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cavity = np.zeros([600, 800, 3], dtype=np.uint8)

        for c in cnt_cen:
            area = cv2.contourArea(c)

            R = random.randint(120, 255)
            G = random.randint(120, 255)
            B = random.randint(120, 255)

            if area > 10:
                hull = cv2.convexHull(c)
                x, y, w, h = cv2.boundingRect(hull)
                cen_x = int(x+w/2)
                cen_y = int(y+h/2)
                st_cen = (cen_x, cen_y)
                print(st_cen)
                cv2.circle(median, (cen_x, cen_y), 5, (B, G, R), -1)
                # print(st_cen)
                adt_thres = cv2.cvtColor(thresh2, cv2.COLOR_RGB2GRAY)

                pt = Rs.Rising_pt(st_cen, adt_thres, 180, 12, 10, 5, 2)
                result = pt.search_pt()
                print(result)
                reg=[]
                for i in range (0,len(result),1):
                    x = int(result[i][0][0])
                    y = int(result[i][0][1])
                    distant = 20-int(result[i][1])
                    reg.append((x,y))
                    # if i == len(result)-1:
                    #     cv2.line(frame, (result[i][0][1], result[i][0][0]),
                    #              (result[0][0][1], result[0][0][0]), (B, G, R), 2)
                    #     cv2.line(cavity, (result[i][0][1], result[i][0][0]),
                    #              (result[0][0][1], result[0][0][0]), (255, 255, 255), 2)
                    #
                    # else:
                    #     cv2.line(frame, (result[i][0][1], result[i][0][0]),
                    #          (result[i+1][0][1], result[i+1][0][0]), (B, G, R), 2)
                    #     cv2.line(cavity, (result[i][0][1], result[i][0][0]),
                    #          (result[i+1][0][1], result[i+1][0][0]), (255, 255, 255), 2)


                    cv2.circle(median, (y, x), 3, (int(B*distant/20), int(G*distant/20), int(R*distant/20)), -1)

        # cavity_gy = cv2.cvtColor(cavity, cv2.COLOR_BGR2GRAY)
        # cnt_ca, hierarchy = cv2.findContours(cavity_gy, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # temp=[]
        # for c in cnt_ca:
        #     # hull = cv2.convexHull(c)
        #     area = cv2.contourArea(c)
        #     temp.append(area)
        #     cv2.drawContours(cavity, [c], 0, (255, 255, 255), -1)
        #
        # ct_gy = cv2.cvtColor(cavity, cv2.COLOR_BGR2GRAY)
        # cav_ar.append(sum(temp))
        # cavity_array = np.array(ct_gy)
        # dist_ct=np.uint8(dist_ct)
        # # print(type(cavity_array),type(dist_ct))
        # # print(cavity_array.shape,dist_ct.shape)
        # dist_ct = np.bitwise_and(cavity_array, dist_ct)
        # # print(np.amax(cavity_array), "----ct-and",cavity_array[400][400])
        # # print(np.amax(dist_ct),"----and",dist_ct[400][400])
        # dt.append(np.sum(dist_ct)/sum(temp))
                # regress_pt(result, 5,C=st_cen, A=12)
        cv2.imshow("cavity", cavity)
        cv2.imshow("res", median)
        # cv2.waitKey(0)
        out.write(frame)
        key = cv2.waitKey(1)
        if key == ord('q') or key == 27:
            break
        elif key == ord(' '):
            while cv2.waitKey(1) != ord(' '):
                pass
    # ct = [i for i in range(count-1)]
    # # plt.plot(ct, dt, color='blue')
    # # plt.show()
    # df = pd.DataFrame(dict(
    #     count=ct,
    #     area=dt
    # ))
    # fig = px.line(df, x="count", y="area", title='cavity')
    # # fig["layout"].pop("updatemenus")
    # fig.show()
    cv2.destroyAllWindows()
