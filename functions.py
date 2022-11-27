import numpy as np

def minmax(val, min_val, max_val):
    return min(max_val, max(min_val, val))

def remap(x, in_min, in_max, out_min, out_max):
  return minmax(
    (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min,
    out_min,
    out_max,
  )

def reject_outliers(data: list[float | int], max_deviations = 2.):
  nparr = np.array(data)
  mean = np.mean(nparr)
  standard_deviation = np.std(nparr)
  distance_from_mean = abs(nparr - mean)
  not_outlier = distance_from_mean < max_deviations * standard_deviation
  return nparr[not_outlier]