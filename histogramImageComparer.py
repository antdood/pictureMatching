from PIL import Image
from functools import cache

from numpy.linalg import norm
from numpy import square, subtract

max_colour_scale = 255
bucket_count = 10

error_threshold = 0.001

cached_buckets = {}

@cache
def generate_bucket_boundaries(max_scale, bucket_count):
	leftover_digits_after_bucket_allocation = max_scale % bucket_count

	base_bucket_allocation = int(max_scale/bucket_count)

	base_buckets = [base_bucket_allocation * (bucket_number + 1) for bucket_number in range(bucket_count - leftover_digits_after_bucket_allocation)]
	bigger_buckets = [((base_bucket_allocation + 1) * (bucket_number + 1)) + (base_bucket_allocation * (bucket_count - leftover_digits_after_bucket_allocation)) for bucket_number in range(leftover_digits_after_bucket_allocation)]

	return base_buckets + bigger_buckets

def generate_rgb_bucket_allocation(pixels, bucket_boundaries):
	buckets = [[0 for _ in range(len(bucket_boundaries))] for _ in range(3)]

	for pixel in pixels:				
		for colour_index, colour_value in enumerate(pixel):	
			buckets[colour_index][get_bucket_index(colour_value, bucket_boundaries)] += 1

	return buckets


def get_bucket_index(value, bucket_boundaries):
	for index, boundary in enumerate(bucket_boundaries):
		if value < boundary:
			return index
	return 0

def normalize_buckets(buckets):
	return [bucket / norm(bucket) for bucket in buckets]

def convert_image_to_rgb_pixels(image_path):
	print(image_path)
	
	image = Image.open(image_path, 'r')
	return image.getdata().convert("RGB")

def get_bucket_error(buckets1, buckets2):
	errors = []
	for bucket1, bucket2 in zip(buckets1, buckets2):
		mean_squared_error = square(subtract(bucket1, bucket2)).mean()
		errors.append(mean_squared_error)

	return sum(errors)

def get_image_error(image_path_1, image_path_2):
	bucket_boundaries = generate_bucket_boundaries(max_colour_scale, bucket_count)

	if image_path_1 in cached_buckets:
		normalized_buckets_1 = cached_buckets[image_path_1]
	else:
		pixels_1 = convert_image_to_rgb_pixels(image_path_1)
		normalized_buckets_1 = normalize_buckets(generate_rgb_bucket_allocation(pixels_1, bucket_boundaries))

		cached_buckets[image_path_1] = normalized_buckets_1

	if image_path_2 in cached_buckets:
		normalized_buckets_2 = cached_buckets[image_path_2]
	else:
		pixels_2 = convert_image_to_rgb_pixels(image_path_2)
		normalized_buckets_2 = normalize_buckets(generate_rgb_bucket_allocation(pixels_2, bucket_boundaries))

		cached_buckets[image_path_2] = normalized_buckets_2

	return get_bucket_error(normalized_buckets_1, normalized_buckets_2)

def isSimilar(image_path_1, image_path_2):
	return get_image_error(image_path_1, image_path_2) < error_threshold
