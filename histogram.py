from PIL import Image

max_colour_scale = 255
buckets = 10

im = Image.open("image.jpg", 'r')
width, height = im.size
pixel_values = list(im.getdata())

def generate_bucket_boundaries(max_scale, bucket_count):
	leftover_digits_after_bucket_allocation = max_scale % bucket_count

	base_bucket_allocation = int(max_scale/bucket_count)

	base_buckets = [base_bucket_allocation * (bucket_number + 1) for bucket_number in range(bucket_count - leftover_digits_after_bucket_allocation)]
	bigger_buckets = [((base_bucket_allocation + 1) * (bucket_number + 1)) + (base_bucket_allocation * (bucket_count - leftover_digits_after_bucket_allocation)) for bucket_number in range(leftover_digits_after_bucket_allocation)]

	return base_buckets + bigger_buckets

