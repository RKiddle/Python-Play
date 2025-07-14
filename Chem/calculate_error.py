def calculate_error(measured, actual):
    """
    Calculate the error and percent error between a measured and actual value.

    Parameters:
    measured (float): The measured or experimental value.
    actual (float): The actual or theoretical value.

    Returns:
    tuple: A tuple containing the error and percent error.
    """
    error = measured - actual
    percent_error = abs(error / actual) * 100
    print("Error:", error)
    print("Percent Error:", percent_error, "%")
    return error, percent_error

# Example usage:
measured_value = 9.8
actual_value = 10.0



