def calculate_reorder_quantity(current_stock, minimum_stock):
    """
    Calculate how many units need to be reordered.
    """

    if current_stock < minimum_stock:
        return minimum_stock - current_stock

    return 0


def calculate_percentage_difference(value1, value2):
    """
    Calculate percentage difference between two values.
    """

    if value2 == 0:
        return 0

    return abs(value1 - value2) / value2 * 100