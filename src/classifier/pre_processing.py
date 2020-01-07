from PIL import Image

# Resize image
def resize_image(image, ratio):
  size = (int(ratio * image.size[0]), int(ratio * image.size[1]))
  return image.resize(size, Image.ANTIALIAS)


# Quantize image
def quantize_image(image, n_bits):
  num_colors = 2 ** n_bits
  return image.quantize(num_colors)