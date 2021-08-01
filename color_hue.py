from PIL import Image

side_x = 255
side_y = 255 
img = Image.new("HSV", (side_x, side_y))

pixels = []

for j in range(side_y):
    for i in range(side_x):
        pixels.append((i , j, 255))

img.putdata(pixels)
new_img = img.convert(mode = "RGB")
new_img.save("desktop/color_hue.png")