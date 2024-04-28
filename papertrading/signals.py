

def is_harami(first, second):
    if second['close'].tolist() < first['open'].tolist() and \
       second['open'].tolist() > first['close'].tolist() and \
       second['high'].tolist() < first['high'].tolist() and \
       second['low'].tolist() > first['low'].tolist() and \
       second['open'].tolist() < second['close'].tolist() and \
       first['open'].tolist() > first['close'].tolist():
        return True
    return False


def is_doppelganger(first, second, third):
    if first['close'].tolist() < first['open'].tolist() and \
       second['close'].tolist() < first['open'].tolist() and \
       third['high'].tolist() == second['high'].tolist() and \
       round(third['low'].tolist()) == round(second['low'].tolist()):
        return True
    return False
