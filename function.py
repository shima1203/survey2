# データを1ms単位に変換する関数
def mince_data(start_time, finish_time, coordinates_ori=[]):
    coordinates = coordinates_ori.copy()
    mince_coordinate = []
    coordinate_tmp = coordinates[0]
    for coordinate in coordinates:
        if(coordinate['time'] >= start_time and coordinate['time'] <= finish_time):
            i = 0
            time_s = 0
            if(coordinate_tmp["time"] < start_time):
                time_s = start_time
            else:
                time_s = coordinate_tmp["time"]
            while(time_s + i < coordinate['time'] and time_s + i < finish_time):
                mince_coordinate.append({"event":coordinate_tmp['event'],"x":coordinate_tmp["x"],"y":coordinate_tmp['y'],"time":time_s + i})
                i += 1
        coordinate_tmp = coordinate
    return mince_coordinate


# マウスの平均スピードを返す関数
def mouse_speed(stop_time , coordinates_ori=[], scroll_ori = []):
    distance = 0
    move_time = 0
    coordinates = coordinates_ori.copy()
    scroll = scroll_ori.copy()
    coordinate_tmp = coordinates[0]
    for coordinate in coordinates:
        i = 0
        if(coordinate_tmp['x'] != coordinate['x'] or coordinate_tmp['y'] != coordinate['y']):
            for sc in scroll:
                if(sc['time'] <= coordinate['time'] ):
                    coordinate_tmp  = coordinate
                    i += 1
                else:
                    break
            for j in range(i):
                del scroll[0]
                
        if(coordinate_tmp['x'] != coordinate['x'] or coordinate_tmp['y'] != coordinate['y']):
            if(coordinate['time'] - coordinate_tmp["time"] <= stop_time):             # stop_time以内でイベントが発生している場合、マウスが連続で動いていると考える
                distance += abs(coordinate['x'] - coordinate_tmp['x']) + abs(coordinate['y'] - coordinate_tmp['y'])
                move_time += coordinate['time'] - coordinate_tmp["time"]
                i += 1
            coordinate_tmp  = coordinate
    if(move_time != 0):
        return(distance / move_time)
    else:
        return None


# マウスの平均スピードを返す関数
def mouse_speed_period(stop_time , start_time, finish_time, coordinates_ori=[], scroll_ori = []):
    distance = 0
    move_time = 0
    coordinates = coordinates_ori.copy()
    scroll = scroll_ori.copy()
    coordinate_tmp = coordinates[0]
    for coordinate in coordinates:
        if(coordinate['time'] >= start_time and coordinate['time'] <= finish_time):
            i = 0
            if(coordinate_tmp['x'] != coordinate['x'] or coordinate_tmp['y'] != coordinate['y']):
                for sc in scroll:
                    if(sc['time'] <= coordinate['time'] ):
                        coordinate_tmp  = coordinate
                        i += 1
                    else:
                        break
                for j in range(i):
                    del scroll[0]
                    
            if(coordinate_tmp['x'] != coordinate['x'] or coordinate_tmp['y'] != coordinate['y']):
                if(coordinate_tmp["time"] < start_time and coordinate['time'] - coordinate_tmp["time"] <= stop_time):
                    distance += (abs(coordinate['x'] - coordinate_tmp['x']) + abs(coordinate['y'] - coordinate_tmp['y'])) * (coordinate['time'] - start_time) / (coordinate['time'] - coordinate_tmp['time'])
                    move_time += coordinate['time'] - start_time
                    i += 1
                elif(coordinate['time'] - coordinate_tmp["time"] <= stop_time):             # stop_time以内でイベントが発生している場合、マウスが連続で動いていると考える
                    distance += abs(coordinate['x'] - coordinate_tmp['x']) + abs(coordinate['y'] - coordinate_tmp['y'])
                    move_time += coordinate['time'] - coordinate_tmp["time"]
                    i += 1
                # 追加
                else:
                    distance += (abs(coordinate['x'] - coordinate_tmp['x']) + abs(coordinate['y'] - coordinate_tmp['y'])) * (finish_time - coordinate['time']) / (coordinate['time'] - coordinate_tmp['time'])
                    move_time += finish_time - coordinate['time']
                    i += 1
                    break
                coordinate_tmp  = coordinate
    if(move_time != 0):
        return(distance / move_time)
    else:
        return None


# クリックイベント直前のマウスのスピードを返す関数
def mouse_speed_click_pre(start_time, finish_time, coordinates_ori=[], clicks_ori=[], scrolls_ori = []):
    coordinates = coordinates_ori.copy()
    clicks = clicks_ori.copy()
    scrolls = scrolls_ori.copy()
    click_pre_list = []
    for click in clicks:
        speed_pre = mouse_speed_period(1000, click['time'] - start_time, click['time'] - finish_time, coordinates, scrolls)
        if(speed_pre != None):
            click_pre_list.append(speed_pre)

    # マウス速度の平均を返す
    time_sum = 0
    j = 0
    for click_pre in click_pre_list:
        time_sum += click_pre
        j += 1
    if(j != 0):
        return(time_sum / j)
    else:
        return(0)
    
    # 最小のマウス速度pick_num個をピックし、その平均を返す
    # pick_num = 100
    # time_sum = 0
    # click_pre_list_sorted = sorted(click_pre_list, reverse=True)
    # # False:min True:max
    # if(len(click_pre_list_sorted) >= pick_num):
    #     for j in range(pick_num):
    #         time_sum += click_pre_list_sorted[j]
    #     return(time_sum / pick_num)
    # else:
    #     for j in range(len(click_pre_list_sorted)):
    #         time_sum += click_pre_list_sorted[j]
    #     if(len(click_pre_list_sorted) != 0):
    #         return(time_sum / len(click_pre_list_sorted))
    #     else:
    #         return(0)

# クリックイベント直前のマウスのイベント数を返す関数
def mouse_event_click_pre(coordinates_ori=[], clicks_ori=[]):
    coordinates = coordinates_ori.copy()
    clicks = clicks_ori.copy()
    click_pre_list = []
    tmp = []
    time_close = 500
    time_tmp = coordinates[0]['time']
    for click in clicks:
        i = 0
        for coordinate in coordinates:
            if(coordinate['time'] <= click['time'] and coordinate['time'] >= click['time'] - time_close):
                if(coordinate['time'] - time_tmp <= 1000):
                    click_pre_list.append(coordinate['time'] - time_tmp)
                    tmp.append(coordinate['time'])
            if(coordinate['time'] > click['time']):
                break
            time_tmp = coordinate['time']
            i += 1
        for j in range(i):
            del coordinates[0]
    # time_close以内のマウスイベントの数を返す
    return(len(click_pre_list))

# クリックイベント直後のマウスのスピードを返す関数
def mouse_speed_click_rear(start_time, finish_time, coordinates_ori=[], clicks_ori=[], scrolls_ori = []):
    coordinates = coordinates_ori.copy()
    clicks = clicks_ori.copy()
    scrolls = scrolls_ori.copy()
    click_pre_list = []
    for click in clicks:
        speed_pre = mouse_speed_period(1000, click['time'] + start_time, click['time'] + finish_time, coordinates, scrolls)
        if(speed_pre != None):
            click_pre_list.append(speed_pre)

    # マウス速度の平均を返す
    time_sum = 0
    j = 0
    for click_pre in click_pre_list:
        time_sum += click_pre
        j += 1
    if(j != 0):
        return(time_sum / j)
    else:
        return(0)
    
    # 最小のマウス速度pick_num個をピックし、その平均を返す
    # pick_num = 30
    # time_sum = 0
    # click_pre_list_sorted = sorted(click_pre_list, reverse=True)
    # if(len(click_pre_list_sorted) >= pick_num):
    #     for j in range(pick_num):
    #         time_sum += click_pre_list_sorted[j]
    #     return(time_sum / pick_num)
    # else:
    #     for j in range(len(click_pre_list_sorted)):
    #         time_sum += click_pre_list_sorted[j]
    #     if(len(click_pre_list_sorted) != 0):
    #         return(time_sum / len(click_pre_list_sorted))
    #     else:
    #         return(0)

# クリックイベント直後のマウスのイベント数を返す関数
def mouse_event_click_rear(coordinates_ori=[], clicks_ori=[]):
    coordinates = coordinates_ori.copy()
    clicks = clicks_ori.copy()
    click_pre_list = []
    tmp = []
    time_close = 500
    time_tmp = coordinates[0]['time']
    for click in clicks:
        i = 0
        for coordinate in coordinates:
            if(coordinate['time'] >= click['time'] and coordinate['time'] <= click['time'] + time_close):
                if(coordinate['time'] - time_tmp <= 1000):
                    click_pre_list.append(coordinate['time'] - time_tmp)
                    tmp.append(coordinate['time'])
            if(coordinate['time'] > click['time'] + time_close):
                break
            time_tmp = coordinate['time']
            i += 1
        for j in range(i):
            del coordinates[0]
    # time_close以内のマウスイベントの数を返す
    return(len(click_pre_list))

# スクロールイベント直後のマウスのスピードを返す関数
def mouse_speed_scroll_rear(start_time, finish_time, coordinates_ori=[], scrolls_ori=[]):
    coordinates = coordinates_ori.copy()
    scrolls = scrolls_ori.copy()
    scroll_pre_list = []
    select_time = 100
    coordinate_time_tmp = coordinates[0]['time']
    scroll_time_tmp = scrolls[0]['time']
    for scroll in scrolls:
        i = 0
        if(scroll['time'] - scroll_time_tmp >= select_time):
            speed_pre = mouse_speed_period(1000, scroll_time_tmp + start_time, scroll_time_tmp + finish_time, coordinates, scrolls)
            if(speed_pre != None):
                scroll_pre_list.append(speed_pre)
            else:
                scroll_pre_list.append(0)
        scroll_time_tmp = scroll['time']
    # time_close以内のマウスイベントの数を返す
    # return(len(click_pre_list))

    # マウス速度の平均を返す
    # time_sum = 0
    # j = 0
    # for scroll_pre in scroll_pre_list:
    #     time_sum += scroll_pre
    #     j += 1
    # if(j != 0):
    #     return(time_sum / j)
    # else:
    #     return(0)
    
    # 最小のマウス速度pick_num個をピックし、その平均を返す
    pick_num = 10
    time_sum = 0
    scroll_pre_list_sorted = sorted(scroll_pre_list, reverse=False)
    if(len(scroll_pre_list_sorted) >= pick_num):
        for j in range(pick_num):
            time_sum += scroll_pre_list_sorted[j]
        return(time_sum / pick_num)
    else:
        for j in range(len(scroll_pre_list_sorted)):
            time_sum += scroll_pre_list_sorted[j]
        if(len(scroll_pre_list_sorted) != 0):
            return(time_sum / len(scroll_pre_list_sorted))
        else:
            return(0)

# スクロールイベント直後のマウスのイベント数を返す関数
def mouse_event_scroll_rear(coordinates_ori=[], scrolls_ori=[]):
    coordinates = coordinates_ori.copy()
    scrolls = scrolls_ori.copy()
    scroll_pre_list = []
    tmp = []
    time_close = 300
    coordinate_time_tmp = coordinates[0]['time']
    scroll_time_tmp = scrolls[0]['time']
    for scroll in scrolls:
        i = 0
        if(scroll['time'] - scroll_time_tmp <= 1000 and scroll['time'] - scroll_time_tmp != 0):
            for coordinate in coordinates:
                if(coordinate['time'] >= scroll['time'] and coordinate['time'] <= scroll['time'] + time_close):
                    if(coordinate['time'] - coordinate_time_tmp <= 1000):
                        scroll_pre_list.append(coordinate['time'] - coordinate_time_tmp)
                        tmp.append(coordinate['time'])
                if(coordinate['time'] > scroll['time'] + time_close):
                    break
                coordinate_time_tmp = coordinate['time']
                i += 1
            for j in range(i):
                del coordinates[0]
        scroll_time_tmp = scroll['time']
    # time_close以内のマウスイベントの数を返す
    return(len(scroll_pre_list))




def test():
    data_coordinate =  [{"event":"mousemove","x":1,"y":1,"time":1},
                        {"event":"mousemove","x":2,"y":6,"time":10},
                        {"event":"mousemove","x":5,"y":6,"time":20},
                        {"event":"mousemove","x":10,"y":10,"time":30},
                        {"event":"mousemove","x":20,"y":20,"time":35},
                        {"event":"mousemove","x":20,"y":20,"time":36}]
    
    data_scroll =  [{"event":"scroll","x":1,"y":1,"time":21},
                    {"event":"scroll","x":2,"y":2,"time":22},
                    {"event":"scroll","x":3,"y":3,"time":23},
                    {"event":"scroll","x":4,"y":4,"time":24},
                    {"event":"scroll","x":3,"y":3,"time":200},]
    
    data_click = [{"event":"click","x":5,"y":6,"time":21}]
    print(mouse_speed_scroll_rear(data_coordinate,  data_scroll))




















































# クリックイベント直前のマウスのスピードを返す関数
# def mouse_speed_click_pre(coordinates_ori=[], clicks_ori=[]):
#     coordinates = coordinates_ori.copy()
#     clicks = clicks_ori.copy()
#     click_pre_list = []
#     time_close = 500
#     time_tmp = coordinates[0]['time']
#     for click in clicks:
#         i = 0
#         for coordinate in coordinates:
#             if(coordinate['time'] <= click['time'] and coordinate['time'] >= click['time'] - time_close):
#                 if(coordinate['time'] - time_tmp <= 1000):
#                     click_pre_list.append(coordinate['time'] - time_tmp)
#             if(coordinate['time'] > click['time']):
#                 break
#             time_tmp = coordinate['time']
#             i += 1
#         for j in range(i):
#             del coordinates[0]
#         # print('click_pre_list : ', len(click_pre_list))
#         # print('coordinates_list : ', len(coordinates))
#         # print('----------------------------------')
#     # time_close以内のマウスイベントの数を返す
#     # return(len(click_pre_list))

#     # time_close以内のマウス速度の平均を返す
#     time_sum = 0
#     j = 0
#     for click_pre in click_pre_list:
#         time_sum += click_pre
#         j += 1
#     return(time_sum / j)