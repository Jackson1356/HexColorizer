import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon

def hexagon_generator(edge_length, selected_area):
    """Generate hexagon centers within the specified area."""
    x_min, y_min, x_max, y_max = selected_area
    y_step = int(np.sqrt(3) * edge_length)
    for x in range(x_min, x_max, int(1.5 * edge_length)):
        for y in range(y_min, y_max, y_step):
            if (x // int(1.5 * edge_length)) % 2 == 1:
                current_y = y + y_step // 2
            else:
                current_y = y
            yield x, current_y

def apply_hexagonal_pixels(image_path, hex_size, output_path, selected_area):
    """Apply a hexagonal grid to a specified area of the image."""
    img = Image.open(image_path)
    img_array = np.array(img)
    dpi = 100
    fig, ax = plt.subplots(figsize=(img.width / dpi, img.height / dpi), dpi=dpi)
    ax.imshow(img)
    ax.axis('off')

    for x, y in hexagon_generator(hex_size, selected_area):
        hex = RegularPolygon((x, y), numVertices=6, radius=hex_size, orientation=np.pi/6,
                             facecolor=get_average_color(img_array, x, y, hex_size), edgecolor='none')
        ax.add_patch(hex)
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
    plt.show()

def get_average_color(img_array, x, y, size):
    """Compute the average color within the hexagonal area."""
    pixels = []
    for dx in range(-size, size + 1):
        for dy in range(-size, size + 1):
            dist = np.sqrt((dx ** 2) + (dy ** 2 * (2 / np.sqrt(3)) ** 2))
            if dist <= size:
                nx, ny = x + dx, y + dy
                if 0 <= nx < img_array.shape[1] and 0 <= ny < img_array.shape[0]:
                    pixels.append(img_array[ny][nx])
    if pixels:
        average_color = np.mean(pixels, axis=0)
        return (average_color / 255).tolist()
    return [0, 0, 0]

# Example usage
image_path = 'maine_cat.jpg'
hex_size = 8 # Size of the hexagons
output_path = 'Hex_Select_maine_cat.jpg'
selected_area = (420, 40,760, 400)  # The area to apply the hexagonal grid (x_min, y_min, x_max, y_max)

apply_hexagonal_pixels(image_path, hex_size, output_path, selected_area)
