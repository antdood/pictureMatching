import pathlib
from histogramImageComparer import isSimilar

image_folder_name = "images"

p = pathlib.Path('.')

images = list(p.glob(f'**/{image_folder_name}/*'))

