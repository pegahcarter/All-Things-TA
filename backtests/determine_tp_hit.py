

def determine_tp(signal, index, _open, _high, _low, cushion=0):
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
