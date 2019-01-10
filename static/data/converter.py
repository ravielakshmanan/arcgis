from osgeo import gdal
import datetime

input_base = '/home/pankhuri/Downloads/downloadWaterDatasets/change_'
output_base = '/home/pankhuri/Downloads/image_tif/change_'

i = -180
while i < 180:
    print(datetime.datetime.now())
    for j in range(-20, 90, 10):
        print(i , j)
        input_file = input_base + str(abs(i)) + ('W' if i < 0 else 'E') + '_' + str(abs(j)) + ('S' if j < 0 else 'N') + '.tif'
        output_file = output_base + str(abs(i)) + ('W' if i < 0 else 'E') + '_' + str(abs(j)) + ('S' if j < 0 else 'N') + '.png'

        gdal.Translate(output_file, input_file, format = 'PNG')
    i += 10