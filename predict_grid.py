import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
from PIL import Image
from pathfinder import seek
from weighting import update_weights_with_roads, update_weights_with_grid
from validate import validate

def predict_grid(
        bv_file,
        bv_threshold=1,
        existing_grid=None,
        validation_grid=None,
        road_weighting=None,
        road_dir=None,
        film=False,
        input_origin=None
):
    """

    @param bv_file:
        String. Path to brightness value file
    @param bv_threshold:
        Float. Value of threshold
    @param existing_grid:
        String. Path of existing gridlines (HV-lines) file
    @param validation_grid:
        String. Path to the validation grid file.
    @param road_weighting:
        Dict. Configuration of road weighting
    @param road_dir:
        String. Path to the directory containing all road geotiff files / rasters.
    @param film:
        Boolean. If a visualization of iterations are to be saved as images during runthrough.
    @param input_origin:
        Tuple. (Int, Int) Index of the origin, start point, of a country.
    @return:
        results, the predicted paths, the distances and a rendering of distances.
        validation metrics, precision, accuracy and iou for the predicted grid.
    """
    brightness_values = Image.open(bv_file)
    brightness_values = np.array(brightness_values)
    targets = (lambda x: x > bv_threshold)(brightness_values) * 1

    origin = np.zeros(targets.shape)
    if input_origin:
        origin[input_origin[0]][input_origin[1]] = 1
    else:
        for i in range(int(targets.shape[0] / 2),
                       targets.shape[0]):  # Origin is set to the first target point found, somewhere close to center
            for j in range(int(targets.shape[1] / 2), targets.shape[1]):
                if targets[i][j]:
                    origin[i][j] = 1
                    break

    weights = np.ones(targets.shape)
    if road_dir:
        roads_list = [path for path in os.listdir(road_dir) if path[-3:] == 'tif']
        for road_type in roads_list:
            r = Image.open(road_dir + road_type)
            r = np.array(r)
            r = (lambda x: x == 1)(r) * 1
            update_weights_with_roads(weights, r, road_weighting[road_type[:-4]])

    if existing_grid:
        grid = Image.open(existing_grid)
        grid = np.array(grid)
        update_weights_with_grid(weights, grid)

    results = seek(
        origin,
        targets=targets,
        weights=weights,
        film=film
    )

    if validation_grid:
        validation = Image.open(validation_grid)
        validation = np.array(validation)
        validation = (lambda x: x > 0)(validation) * 1
        precision, accuracy, iou = validate(validation, results['paths'])
        return results, precision, accuracy, iou
    return results