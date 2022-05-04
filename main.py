import pathlib
from histogramImageComparer import isSimilar
import itertools

image_folder_name = "images"

p = pathlib.Path('.')

images = p.glob(f'**/{image_folder_name}/*')

def generate_matching_pairs(images):
	image_combinations = itertools.combinations(images, 2)

	matched_images = {}

	for combination in image_combinations:
		if (combination[0] in matched_images) or (combination[1] in matched_images):
			continue

		if isSimilar(*combination):
			matched_images[combination[1]] = combination[0]

	return matched_images


