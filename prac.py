# from PIL import Image
# import numpy as np
# from aes import ecb_mode_encrypt, ecb_mode_decrypt

# # Build a truly flat grayscale image in-memory (no file, no compression, no antialiasing)
# height, width = 64, 64
# img_array = np.full((height, width), 200, dtype=np.uint8)  # every pixel exactly 200
# print("unique pixel values:", np.unique(img_array))         # should print just [200]

# plain_bytes = img_array.flatten().tolist()
# key = "Thats my Kung Fu"

# solution = ecb_mode_encrypt(plain_bytes, key)
# blocks = solution.res
# unique_blocks = set(tuple(b) for b in blocks)
# print("total blocks:", len(blocks), " unique ciphertext blocks:", len(unique_blocks))

# img = Image.open("red.png").convert("L")
# img_array = np.array(img)
# print(img_array.shape)              # should be (H, W) -- 2D, no channel axis
# print(np.unique(img_array))         # if this prints more than one value, that's your answer

from PIL import Image
import numpy as np

height, width = 64, 64
img_array = np.full((height, width), 200, dtype=np.uint8)
Image.fromarray(img_array, mode="L").save("flat_test.png")