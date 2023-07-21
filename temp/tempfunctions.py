__author__ = "Nicolas Gutierrez"

# Standard libraries
from typing import Tuple
# Third party libraries
import pandas as pd
import numpy as np
# Custom libraries


def calculate_temp_and_ref(dfs_dict: pd.Series) -> Tuple[float, float]:
    # Time study
    final_time = dfs_dict.index.to_pydatetime()[-1]
    delta_time = dfs_dict.index.to_pydatetime()-final_time
    helper = np.vectorize(lambda x: x.total_seconds()/3600)
    delta_time_hours = helper(delta_time)

    # Fitting a line
    z = np.polyfit(
        delta_time_hours,
        dfs_dict.to_numpy().astype(float),
        1
    )

    # Returning values for the indicator + delta
    current_value = float(dfs_dict.iloc[-1])
    reference_value = current_value - np.around(z[0][0], 2)

    return current_value, reference_value
