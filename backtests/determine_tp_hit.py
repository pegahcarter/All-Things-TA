
def determine_TP(signal, index, _open, _high, _low, cushion=0):
    if signal == 'Long':
        l_bounds = _low
        midrange = _open
        u_bounds = _high
        cushion = 1. + cushion
    else:   # signal == 'Short'
        l_bounds = -_high
        midrange = -_open
        u_bounds = -_low
        cushion = 1. - cushion

    purchase_price = midrange[index+1]
    stop_loss = min(l_bounds[index-10:index]) * cushion

    diff = abs(purchase_price) - abs(stop_loss)
    tp1 = purchase_price + diff/2.
    tp2 = purchase_price + diff
    tp3 = purchase_price + diff*2
    tp4 = purchase_price + diff*3

    tp_targets = [tp1, tp2, tp3, tp4]
    TP = 0

    for x in range(index+1, len(_open)):
        if TP > 0:
            stop_loss = purchase_price
        while TP != 4 and u_bounds[x] > tp_targets[TP]:
            TP += 1
        if TP == 4 or stop_loss > l_bounds[x]:
            break

    return TP
