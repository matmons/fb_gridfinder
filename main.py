import numpy as np
import os
import matplotlib.pyplot as plt
from PIL import Image

import predict_grid
import create_raster_from_array

road_weights = {
    'primary': 0.1,
    'secondary': 0.25,
    'tertiary': 0.4,
    'service': 0.8,
    'unclassified': 0.6
}
countries = ['uganda', 'namibia']
origins = [(940, 740), (1360, 1295)]
datasets = ['bv_ww_062020', 'bv_ave_ww_2020']
thresholds = [0.40, 0.60, 1.00]

for dataset in datasets:
    for country, origin in zip(countries, origins):
        road_dir = f'datasets/{country}/roads/'
        existing_grid = f'datasets/{country}/hv_lines.tif'
        validation_grid = f'datasets/{country}/grid.tif'
        bv_path = f'datasets/{country}/{dataset}.tif'
        for bv_threshold in thresholds:
            results, precision, accuracy, iou = predict_grid(
                bv_path,
                bv_threshold=bv_threshold,
                road_weighting=road_weights,
                existing_grid=existing_grid,
                validation_grid=validation_grid,
                road_dir=road_dir,
                input_origin=origin
            )
            result_line = f'\n{country},{dataset},{bv_threshold},{round(precision, 2)},{round(accuracy, 2)},{round(iou, 2)}'
            try:
                os.mkdir('results')
            except Exception:
                # NBD
                pass
            try:
                os.mkdir(f'results/{country}')
            except Exception:
                # NBD
                pass

            # Create blank txt file called 'results.txt' if running for the first time.
            file = open(f'results/{country}/results.txt', 'a')
            file.write(result_line)
            file.close()

            # Create GeoTIFF
            output = f'results/{country}/{bv_threshold}_pred_paths.tif'
            create_raster_from_array(bv_path, output, results['paths'])

            # Create plot comparison of predicted grid and validation grid
            valid_plot = np.array(Image.open(f'datasets/{country}/grid.tif'))
            valid_plot = (lambda x: x > 0)(valid_plot) * 1
            plt.figure(figsize=(20, 12))
            plt.title("Predicted Grid vs. Actual Grid")
            plt.subplot(121)
            plt.imshow(results['paths'])
            plt.subplot(122)
            plt.imshow(valid_plot)
            plt.savefig(
                f"results/{country}/{dataset}_predicted_grid_vs_actual_grid{str(bv_threshold).replace('.', '_')}.png")
            plt.close()