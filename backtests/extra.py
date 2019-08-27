# ------------------------------------------------------------------------------
# 2018.08.20
# Example 1

tp1 = .25
tp2 = .25
tp3 = .25
tp4 = .25

# Tp1
a = (10100 - 10000) * .25 + (9800 - 10000) * .75
b = (10100 - 10000) * tp1 + (9800 - 10000) * (1. - tp1)
a/200.
b/200.
(tp1 / 2.) - (1 - tp1)

# Tp2
a = (10100 - 10000) * .25 + (10200 - 10000) * .25
b = (10100 - 10000) * tp1 + (10200 - 10000) * tp2
a/200.
b/200.
(tp1 / 2.) + tp2

# tp3
a = (10100 - 10000) * .25 + (10200 - 10000) * .25 + (10400 - 10000) * .25
b = 75 + (10400 - 10000) * tp3
a/200.
b/200.
0.375 + tp3 * 2

# tp4
a = (10100 - 10000) * .25 + (10200 - 10000) * .25 + (10400 - 10000) * .25 + (10600 - 10000) * .25
b = 175 + (10600 - 10000) * tp4
a/200.
b/200.
0.875 + tp4 * 3


# Example 2

tp1 = .4
tp2 = .2
tp3 = .2
tp4 = .2

# Tp1
a = (10100 - 10000) * .4 + (9800 - 10000) * .6
b = (10100 - 10000) * tp1 + (9800 - 10000) * (1. - tp1)
a/200.
b/200.
(tp1 / 2.) - (1 - tp1)

# Tp2
a = (10100 - 10000) * .4 + (10200 - 10000) * .2
b = (10100 - 10000) * tp1 + (10200 - 10000) * tp2
a/200.
b/200.
(tp1 / 2.) + tp2

# Tp3
a = (10100 - 10000) * .4 + (10200 - 10000) * .2 + (10400 - 10000) * .2
b = 80 + (10400 - 10000) * tp3
a/200.
b/200.
0.4 + tp3 * 2

# Tp4
a = (10100 - 10000) * .4 + (10200 - 10000) * .2 + (10400 - 10000) * .2 + (10600 - 10000) * .2
b = 160 + (10600 - 10000) * tp4
a/200.
b/200.
0.8 + tp4*3
