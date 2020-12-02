import numpy as np

def find_nearest(array, value, output='value and index'):
    array = np.asarray(array)
    index = (np.abs(array - value)).argmin()
    if output == 'value':
        return array[index]
    elif output == 'index':
        return index
    else:
        return array[index], index