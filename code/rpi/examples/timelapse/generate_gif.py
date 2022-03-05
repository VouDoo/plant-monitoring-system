import glob
from PIL import Image

images = [
    Image.open(f)
    for f in sorted(glob.glob("*.jpg"))
]
images[0].save(
    fp="timelapse.jpg",
    format="GIF",
    save_all=True,
    append_images=images,
    duration=200,
    loop=0,
)
