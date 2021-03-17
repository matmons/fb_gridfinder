def update_weights_with_roads(weights, roads, weight):
    """
    Updates the current set of weights with a given set of roads and corresponding weights. Returns a modified version
    of the weights variable.
    @param weights: A 2D numpy array of floats
    @param roads: A 2D numpy array of ints
    @param weight: A float between 0.0 and 1.0. Varies with that road category.
    @return: weights: A 2D numpy array of floats
    """
    assert weights.shape == roads.shape
    for i in range(roads.shape[0]):
        for j in range(roads.shape[1]):
            if roads[i][j] == 1:
                weights[i][j] = min(weights[i][j], weight)
    return weights


def update_weights_with_grid(weights, grid):
    """
    Updates the current set of weights with the high voltage line in a country. Returns a modified version
    of the weights variable where all cells containing a grid is given weight 0.000000001.
    @param weights: A 2D numpy array of floats
    @param grid: A 2D numpy array of ints
    @return: weights: A 2D numpy array of floats
    """
    assert weights.shape == grid.shape
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i][j] > 0:
                weights[i][j] = min(weights[i][j], 0.000000001)
    return weights

