import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon

def hexagon_generator(edge_length, img_width, img_height):
    """Generate hexagon centers, properly covering the image dimensions."""
    y_step = int(np.sqrt(3) * edge_length)
    # Extend range to fully cover the image dimensions and a little beyond
    for x in range(-edge_length, img_width + edge_length, int(1.5 * edge_length)):
        for y in range(-y_step, img_height + y_step, y_step):
            # Apply y offset for alternate columns
            if (x // int(1.5 * edge_length)) % 2 == 1:
                current_y = y + y_step // 2
            else:
                current_y = y
            yield x, current_y

def apply_hexagonal_pixels(image_path, hex_size, output_path):
    """Apply a hexagonal grid to an image, ensuring complete coverage."""
    img = Image.open(image_path)
    img_array = np.array(img)
    dpi = 100
    fig, ax = plt.subplots(figsize=(img.width / dpi, img.height / dpi), dpi=dpi)
    ax.imshow(img)
    ax.axis('off')

    for x, y in hexagon_generator(hex_size, img.width, img.height):
        if -hex_size < x < img.width + hex_size and -hex_size < y < img.height + hex_size:
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
intput_img = "Lenna.png"
output = "Hex_Lenna.png"
apply_hexagonal_pixels(intput_img, 3, output)
