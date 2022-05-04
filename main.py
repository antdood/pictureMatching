import pathlib
from histogramImageComparer import isSimilar
import itertools
import os
from collections import defaultdict
import time

image_folder_name = "imagestest"

p = pathlib.Path('.')

images = p.glob(f'**/{image_folder_name}/*')

def generate_matching_pairs(images):
	image_combinations = itertools.combinations(images, 2)

	matched_images = defaultdict(list)

	for combination in image_combinations:
		if is_image_already_matched(combination[0], matched_images) or is_image_already_matched(combination[1], matched_images):
			continue

		if isSimilar(*combination):
			matched_images[combination[0]].append(combination[1])

	return matched_images

def create_grouped_folders(groups):
	for group in groups:
		os.mkdir(f"{image_folder_name}/{group.name.removesuffix(group.suffix)}")
		
def is_image_already_matched(image, groups):
	for group in groups.values():
		if image in group:
			return True

	return False

def move_images_into_group_folders(groups):
	for group, matches in groups.items():
		os.replace(group, f"{image_folder_name}/{group.name.removesuffix(group.suffix)}/{group.name}")
		for image in matches:
			os.replace(image, f"{image_folder_name}/{group.name.removesuffix(group.suffix)}/{image.name}")


start = time.time()

matches = generate_matching_pairs(images)
create_grouped_folders(matches)
move_images_into_group_folders(matches)

end = time.time()

print(f"done in {end - start} seconds")
