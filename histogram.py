from PIL import Image

max_colour_scale = 255
bucket_count = 10

im = Image.open("image.jpg", 'r')
width, height = im.size
pixel_values = list(im.getdata())

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
	
print(generate_rgb_bucket_allocation(pixel_values, generate_bucket_boundaries(max_colour_scale, bucket_count)))