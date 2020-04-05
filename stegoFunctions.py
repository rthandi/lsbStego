def bin_mask_generator(number):
    if number == 1:
        # 254 = 11111110
        return 254
    elif number == 2:
        # 252 = 11111100
        return 252
    elif number == 3:
        # 248 = 11111000
        return 248
    elif number == 4:
        # 240 = 11110000
        return 240
    elif number == 5:
        # 224 = 11100000
        return 224
    elif number == 6:
        # 192 = 11000000
        return 192
    else:
        # 218 = 10000000
        return 128


def compare_queue(queue1, queue2):
    return queue1.queue == queue2.queue
