# マウスの平均スピードを返す関数
def mouse_speed(coordinates=[]):
    sum_mous = 0
    i = 0
    time_tmp  = coordinates[0]['time']
    for coordinate in coordinates:
        if(coordinate['time'] - time_tmp <= 1000):             # １秒以内でイベントが発生している場合、マウスが連続で動いていると考える
            sum_mous += coordinate['time'] - time_tmp
            i += 1
        time_tmp  = coordinate['time']
    return(sum_mous/i)


# クリックイベント直前のマウスのスピードを返す関数
def mouse_speed_click_pre(coordinates_ori=[], clicks_ori=[]):
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
        # print('click_pre_list : ', len(click_pre_list))
        # print('coordinates_list : ', len(coordinates))
        # print('----------------------------------')
    # time_close以内のマウスイベントの数を返す
    # return(len(click_pre_list))

    # time_close以内のマウス速度の平均を返す
    time_sum = 0
    j = 0
    for click_pre in click_pre_list:
        time_sum += click_pre
        j += 1
    return(time_sum / j)

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
def mouse_speed_click_rear(coordinates_ori=[], clicks_ori=[]):
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
    # return(len(click_pre_list))

    # time_close以内のマウス速度の平均を返す
    time_sum = 0
    j = 0
    for click_pre in click_pre_list:
        time_sum += click_pre
        j += 1
    return(time_sum / j)

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
def mouse_speed_scroll_rear(coordinates_ori=[], scrolls_ori=[]):
    coordinates = coordinates_ori.copy()
    scrolls = scrolls_ori.copy()
    scroll_pre_list = []
    tmp = []
    time_close = 500
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
    # return(len(click_pre_list))

    # time_close以内のマウス速度の平均を返す
    time_sum = 0
    j = 0
    for scroll_pre in scroll_pre_list:
        time_sum += scroll_pre
        j += 1
    return(time_sum / j)

# スクロールイベント直後のマウスのイベント数を返す関数
def mouse_event_scroll_rear(coordinates_ori=[], scrolls_ori=[]):
    coordinates = coordinates_ori.copy()
    scrolls = scrolls_ori.copy()
    scroll_pre_list = []
    tmp = []
    time_close = 500
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