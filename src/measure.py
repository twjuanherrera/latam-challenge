import time

def measure_notebook_elapsed_time(
    start_time: str
) -> float:
    """
    Calculates the elapsed time since the provided start time and returns it as a float.

    Args:
        start_time (float): The start time captured previously using time.time().

    Returns:
        float: The elapsed time in seconds.
    """

    end_time = time.time()
    elapsed_time = end_time - float(start_time)
    return elapsed_time  # Return the elapsed time for further use

def print_notebook_elapsed_time(
    elapsed_time: float
) -> None:
    """
    Prints the elapsed time in a user-friendly format (seconds, minutes, or hours).

    Args:
        elapsed_time (float): The elapsed time in seconds.
    """

    time_unit = "seconds"
    if elapsed_time >= 60:
        elapsed_time /= 60
        time_unit = "minutes"
        if elapsed_time >= 60:
            elapsed_time /= 60
            time_unit = "hours"

    print(f"Elapsed time in the notebook: {elapsed_time:.2f} {time_unit}")