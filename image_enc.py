import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from aes import cbc_mode_encrypt, cbc_mode_decrypt

def hexlist_to_ints(blocks):
    """Flatten a list of blocks (each a list of '0x..' strings) into a flat list of ints."""
    return [int(b, 16) for block in blocks for b in block]


img = Image.open("img.png").convert("RGB")
img_array = np.array(img)

height, width, channels = img_array.shape

# Flatten into bytes (list of ints 0-255) -- translate_into_hex handles this fine
# since each element is already an int, not a str.
plain_bytes = img_array.flatten().tolist()

# ---------------------------------
# Encrypt using your AES CBC
# ---------------------------------
key = "Thats my Kung Fu"

solution = cbc_mode_encrypt(plain_bytes, key)

# solution.res = [IV, block1, block2, ...]. Drop the IV -- it's not image data --
# then flatten the remaining ciphertext blocks into a flat int list.
cipher_blocks = solution.res[1:]
encrypted_bytes = hexlist_to_ints(cipher_blocks)

# PKCS#7 padding appends up to 16 extra bytes before encryption, so ciphertext
# is longer than the original image. Trim back to the original length so it
# reshapes cleanly.
encrypted_array = np.array(encrypted_bytes[:len(plain_bytes)],
                            dtype=np.uint8).reshape(height, width, channels)

# ---------------------------------
# Decrypt
# ---------------------------------
decrypted_blocks = cbc_mode_decrypt(solution, key)   # takes the Solution object + key
decrypted_bytes = hexlist_to_ints(decrypted_blocks)

decrypted_array = np.array(decrypted_bytes[:len(plain_bytes)],
                            dtype=np.uint8).reshape(height, width, channels)

# ---------------------------------
# Display
# ---------------------------------
plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
plt.imshow(img_array)
plt.title("Original")
plt.axis("off")

plt.subplot(1, 3, 2)
plt.imshow(encrypted_array)
plt.title("Encrypted (CBC)")
plt.axis("off")

plt.subplot(1, 3, 3)
plt.imshow(decrypted_array)
plt.title("Decrypted")
plt.axis("off")

plt.show()