__author__ = "Nicolas Gutierrez"

# Standard libraries
from typing import Tuple
# Third party libraries
from pythonping import ping
# Custom libraries


def ping_function(target: str) -> Tuple[float, str]:
    response = ping(target, count=1, verbose=False)
    return response.rtt_avg_ms, "ms"
