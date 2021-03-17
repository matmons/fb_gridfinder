from osgeo import gdal, osr

def create_raster_from_array(original, output, array):
    """
    Creates a georeferenced raster of the predicted paths using the same parameters as the original brightness value
    file.
    @param original: String.
        The file-path to the original brightness value file for a country.
    @param output: String.
        The file-path of which the raster is to be saved
    @param array: A 2D array of ints.
        The predicted paths, outputs of pathfinder
    @return:
    """
    origin = gdal.Open(original)
    band = origin.GetRasterBand(1)

    geotransform = origin.GetGeoTransform()
    wkt = origin.GetProjection()

    # Create GeoTiff file
    driver = gdal.GetDriverByName("GTiff")

    dst_ds = driver.Create(output,
                           band.XSize,
                           band.YSize,
                           1,
                           gdal.GDT_Int16)

    # Writing output raster
    dst_ds.GetRasterBand(1).WriteArray(array)
    # setting nodata value
    dst_ds.GetRasterBand(1).SetNoDataValue(0)
    # setting extension of output raster
    # top left x, w-e pixel resolution, rotation, top left y, rotation, n-s pixel resolution
    dst_ds.SetGeoTransform(geotransform)
    # setting spatial reference of output raster
    srs = osr.SpatialReference()
    srs.ImportFromWkt(wkt)
    dst_ds.SetProjection(srs.ExportToWkt())
    # Close output raster dataset
    ds = None
    dst_ds = None