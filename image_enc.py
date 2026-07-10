import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from aes import (
    cbc_mode_encrypt,
    cbc_mode_decrypt,
    ecb_mode_encrypt,
    ecb_mode_decrypt,
)

def hexlist_to_ints(blocks):
    return [int(b, 16) for block in blocks for b in block]

img = Image.open("logo1.webp").convert("RGB")
img_array = np.array(img)

height, width, channels = img_array.shape
plain_bytes = img_array.flatten().tolist()

key = "Thats my Kung Fu"

ecb_solution = ecb_mode_encrypt(plain_bytes, key)

ecb_cipher = np.array(
    hexlist_to_ints(ecb_solution.res[1:])[:len(plain_bytes)],
    dtype=np.uint8
).reshape(height, width, channels)

ecb_plain = np.array(
    hexlist_to_ints(ecb_mode_decrypt(ecb_solution, key))[:len(plain_bytes)],
    dtype=np.uint8
).reshape(height, width, channels)

cbc_solution = cbc_mode_encrypt(plain_bytes, key)

cbc_cipher = np.array(
    hexlist_to_ints(cbc_solution.res[1:])[:len(plain_bytes)],
    dtype=np.uint8
).reshape(height, width, channels)

cbc_plain = np.array(
    hexlist_to_ints(cbc_mode_decrypt(cbc_solution, key))[:len(plain_bytes)],
    dtype=np.uint8
).reshape(height, width, channels)

plt.figure(figsize=(18, 10))

plt.subplot(2, 3, 1)
plt.imshow(img_array)
plt.title("Original")
plt.axis("off")

plt.subplot(2, 3, 2)
plt.imshow(ecb_cipher)
plt.title("ECB Encrypted")
plt.axis("off")

plt.subplot(2, 3, 3)
plt.imshow(ecb_plain)
plt.title("ECB Decrypted")
plt.axis("off")

plt.subplot(2, 3, 4)
plt.imshow(img_array)
plt.title("Original")
plt.axis("off")

plt.subplot(2, 3, 5)
plt.imshow(cbc_cipher)
plt.title("CBC Encrypted")
plt.axis("off")

plt.subplot(2, 3, 6)
plt.imshow(cbc_plain)
plt.title("CBC Decrypted")
plt.axis("off")

plt.tight_layout()
plt.savefig("ecb_cbc_comparison.png", dpi=300)
plt.show()