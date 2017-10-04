
def chunks_by_el_count(arr, n):
    return [arr[i:i + n] for i in range(0, len(arr), n)]

import os
def GetDesktopPath():
    return os.path.join(os.path.expanduser("~"), 'Desktop')