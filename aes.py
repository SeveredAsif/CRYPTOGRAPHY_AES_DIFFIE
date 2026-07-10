#target is, giving a plaintext and key and get the encrypted text after 10 rounds. implement a key generator module 
from aes_helpers import Sbox, InvSbox, Rcon, Mixer, InvMixer, gf_mult 
import random 
import time 

random.seed(42)

class Solution:
    def __init__(self,res,key_schedulers):
        self.res = res 
        self.key_schedulers = key_schedulers



class KeyScheduler:
  def __init__(self, key):
    self.key = key
    #start_time = time.perf_counter()
    self.key_list = _calculate_key(self.key)
    #end_time = time.perf_counter()
    #execution_time = end_time - start_time

    #print(f"The keyscheduler took {execution_time:.6f} seconds to execute.")
    #print(len(self.key_list))

  def get_key(self,round):
      start = round*4
      return_val= self.key_list[start:start+4]
      #self.start = self.start+4 
      return return_val
  
#   def get_key_in_reverse(self):
#       #print(f"FIRST START:{self.start},({self.start-4},{self.start-1})")
#       return_val= self.key_list[self.start-4:self.start]
#       self.start = self.start-4 
#       return return_val


def _calculate_key(key):
    key_init = transform_into_matrix(key)
    key_list = key_init.copy()
    #print(f"key list size:{len(key_list)},key_")
    for i in range(4,44):
        if(i%4==0):
            round = int(i/4)
            x = g(key_list)
            #print(x)
            #print(round,i)
            rcon_word = [Rcon[round], 0, 0, 0]
            for j in range(len(x)):
                #print(x[j])
                x[j] = hex(convert_hex_string_to_decimal(x[j]) ^ rcon_word[j])
            #print(x)
            #print(i,key_list)
            key_list.append(bit_by_bit_xor(x , key_list[i-4]))
            #print(key_list,i) 
        else:
            #print(key_list,i)
            key_list.append(bit_by_bit_xor(key_list[i-1],key_list[i-4]))
    #print(key_list)
    return key_list

def word_xor(x,y):
    flattened_words = []
    if isinstance(y[0], list):
        for i in y:
            for j in i:
                flattened_words.append(j)
    else:
        flattened_words = y.copy()
    #print(x)
    #print(flattened_words) 
    return bit_by_bit_xor(x,flattened_words)

def word_gf_mult(x,y):
    flattened_words = []
    if isinstance(y[0], list):
        for i in y:
            for j in i:
                flattened_words.append(j)
    else:
        #print(y)
        flattened_words = y
    #print(x)
    #print(flattened_words) 
    return bit_by_bit_gf(x,flattened_words)

def bit_by_bit_gf(x,y):
    #print(x,y)
    res = 0
    #print(f"x,y: {x,y}")
    for i in range(len(x)):
        res = res ^ gf_mult(convert_hex_string_to_decimal(x[i]),y[i])
    return hex(res)    

def bit_by_bit_xor(x,y):
    res = []
    #print(f"x,y: {x,y}")
    for i in range(len(x)):
        res.append(hex(convert_hex_string_to_decimal(x[i])^convert_hex_string_to_decimal(y[i])))
    return res 

def convert_hex_string_to_decimal(hex_num):
    #print(f"act: {hex_num}")
    entry = hex_num[2:]
    #print(f"entry: {entry}")
    left = entry[0]
    right = None 
    if(len(entry)>=2):
        right = entry[1]
    if(left>='a' and left<='f'):
        left = 10 + (ord(left) - ord('a'))
    if(right is not None and right>='a' and right<='f'):
        right = 10 + (ord(right) - ord('a'))
    left = int(left)
    if right is not None:
        right = int(right)
        return left*16+right 
    else: return left 

def matrix_multiply(a,b):
    matrix = [[0 for _ in range(4)] for _ in range(4)]
    #print(matrix)

    for i in range(len(b)):
        for j in range(len(a)):
            #print(a[j],b[i])
            matrix[j][i] = word_gf_mult(a[j],b[i])
    return matrix 
            


def byte_left_shift(word,amount):
    shifted_arr = word.copy()
    for i in range(len(word)):
        shifted_arr[i-amount]=word[i]
    #print(word)
    #print(shifted_arr)
    return shifted_arr

def byte_right_shift(word,amount):
    shifted_arr = word.copy()
    for i in range(len(word)):
        shifted_arr[(i+amount)%len(word)]=word[i]
    #print(word)
    #print(shifted_arr)
    return shifted_arr

def find_Sbox_entry(entry):
    if(len(entry)<4):
        sbox_row=0
        if(entry[2]>='a' and entry[2]<='f'):
            sbox_col = 10 + ord(entry[2])-ord('a')
        else:
            sbox_col = int(entry[2])
    else:
        if(entry[3]>='a' and entry[3]<='f'):
            sbox_col = 10 + ord(entry[3])-ord('a')
        else:
            sbox_col = int(entry[3])
        if(entry[2]>='a' and entry[2]<='f'):
            sbox_row = 10 + ord(entry[2])-ord('a')
        else:
            sbox_row = int(entry[2])
    return sbox_row*16+sbox_col



def change_arr_using_sbox(arr):
    replaced_arr = []
    for entries in arr:
        #print(entries)
        replaced_arr.append(hex(Sbox[find_Sbox_entry(entries)]))
        #print(entries)
        #print(sbox_row,sbox_col,hex(Sbox[sbox_row*16+sbox_col]))
    #print(replaced_arr)
    return replaced_arr
def change_arr_using_inv_sbox(arr):
    replaced_arr = []
    for entries in arr:
        #print(entries)
        replaced_arr.append(hex(InvSbox[find_Sbox_entry(entries)]))
        #print(entries)
        #print(sbox_row,sbox_col,hex(Sbox[sbox_row*16+sbox_col]))
    #print(replaced_arr)
    return replaced_arr


def g(key_list):
    shifted_arr = byte_left_shift(key_list[-1],1)
    return change_arr_using_sbox(shifted_arr)
    

def translate_into_hex(text):
    number = []
    if(isinstance(text,int)):
        return (hex(text))
    for i in text:
        #print(hex(ord(i))) 
        if( isinstance(i,str)):
            number.append(hex(ord(i)))
        else:
            number.append(hex((i)))
    return number   

def transform_into_matrix(numbers):
    word = []
    matrix = [] 
    for i in numbers:
        word.append(i)
        if(len(word)%4==0):
            matrix.append(word) 
            word = []
    return matrix 

def view_matrix(matrix):
    row = []
    for i in range(4):
        for j in range(4):
            print(matrix[j][i], end=" ")
        print() 

def flatten_arr(rows):
    flattened_words = []
    for i in rows:
        for j in i:
            flattened_words.append(j)
    #print(flattened_words)
    return flattened_words

def unflatten_arr(cols):
    newcols= [[] for _ in range(4)]
    i = 0 
    for num,entry in enumerate(cols):
        newcols[i].append(entry)
        
        if(num%4==3):
            i = i+1
    return newcols 
 
def convert_to_row_major(arr):
    rows= [[] for _ in range(4)]
    i = 0
    #print(arr)
    for col in (arr):
        rows[i].append(col)
        i=i+1 
        if i==4:
            i=0 
    #print(rows)
    return rows 

def convert_to_col_major(arr):
    rows= [[] for _ in range(4)]
    i = 0
    #print(arr)
    for col in (arr):
        rows[i].append(col)
        i=i+1 
        if i==4:
            i=0 
    #print(rows)

    return flatten_arr(rows) 



def aes(state,keyScheduler):
    #key0 = translate_into_hex(key)
    # start_time = time.perf_counter()
    # #keyScheduler = KeyScheduler(key)
    # end_time = time.perf_counter()
    # execution_time = end_time - start_time

    # print(f"The keyscheduler took {execution_time:.6f} seconds to execute.")
    round_key = keyScheduler.get_key(0)
     
    #print(f"state:{state},len:{len(state)}")
    #print(f"round_key:{round_key}")
    state = word_xor(state,round_key)
    statetoshow = transform_into_matrix(state) 
    #view_matrix(statetoshow)
    for round in range(10):
        #print(f"round: {round+1}")
        #print(state)
        state = change_arr_using_sbox(state)
        #print(state)
        rows = convert_to_row_major(state)
        for i,_ in enumerate(rows):
            rows[i] = byte_left_shift(rows[i],i) 
        #print(rows)
        flattened_rows = flatten_arr(rows)
        state = convert_to_col_major(flattened_rows)
        #print(state)
        #mixer_flattened = flatten_arr(Mixer)
        #print(Mixer)
        unflattened_state = unflatten_arr(state)
        #print(unflatten_arr(state))
        #print(matrix_multiply(unflattened_state,Mixer))

        if(round!=9):
            state = matrix_multiply(unflattened_state,Mixer)
            state = flatten_arr(state)
        round_key = keyScheduler.get_key(round+1)
        state = word_xor(state,round_key)
        statetoshow = transform_into_matrix(state) 
        #view_matrix(statetoshow)
        
    return state     

def aes_decrypt(state,keyScheduler):
    #key0 = translate_into_hex(key)

    round_key = keyScheduler.get_key(10)
    state = word_xor(state,round_key)
     
    #print(f"state:{state},len:{len(state)}")
    #print(f"round_key:{round_key}")
    #state = word_xor(state,round_key)
    statetoshow = transform_into_matrix(state) 
    #view_matrix(statetoshow)
    for round in range(10):
        #print(f"round: {round+1}")
        #print(state)
        #print(state)
        rows = convert_to_row_major(state)
        for i,_ in enumerate(rows):
            rows[i] = byte_right_shift(rows[i],i) 
        #print(rows)
        flattened_rows = flatten_arr(rows)
        state = convert_to_col_major(flattened_rows)
        state = change_arr_using_inv_sbox(state)
        #print(state)
        #mixer_flattened = flatten_arr(Mixer)
        #print(Mixer)
        
        round_key = keyScheduler.get_key(9-round)
        state = word_xor(state,round_key)

        unflattened_state = unflatten_arr(state)
        #print(unflatten_arr(state))
        #print(matrix_multiply(unflattened_state,Mixer))
        if(round!=9):
            state = matrix_multiply(unflattened_state,InvMixer)
            state = flatten_arr(state)

        statetoshow = transform_into_matrix(state) 
        #view_matrix(statetoshow)
        
    return state    


def pkcs_7(hex_text):
    #print(f"len: {len(hex_text)}")
    bytes_needed = 16 - len(hex_text)%16
    for _ in range(bytes_needed):
        hex_text.append(hex(bytes_needed))
    #print(f"curr: {hex_text}, len: {len(hex_text)}")
    return hex_text 



def ecb_mode_encrypt(text,key):
    solution = Solution(1,2)
    key_schedulers = []
    key0 = translate_into_hex(key)
    #print(len(key0))
    if(len(key0)>16): #truncating key 
        key0 = key0[0:16]
        #print(len(key0))
    if(len(key0)<16):
        key0 = key0.ljust(16, '0')
    #print(key0)
    start_time = time.perf_counter()
    #keyScheduler = KeyScheduler(key)
    keyScheduler = KeyScheduler(key0)
    end_time = time.perf_counter()
    execution_time = end_time - start_time

    print(f"The keyscheduler took {execution_time:.6f} seconds to execute.")
    state = translate_into_hex(text)
    #if(len(state)%16!=0):
    state = pkcs_7(state)
    old_state = state.copy()
    #print(f"state len is : {len(state)}")
    # import random
    # random.seed(42)
    final_res = []
    #print(state)
    #print(IV_rand)
    
    if(len(state)<=16):
     #print("here")
        res = aes(state,keyScheduler)
        #key_schedulers.append(key_sched)
        final_res.append(res)
    else:
        start = 0 
        #print("to the big")
        while(start+16<=len(old_state)):
            #print(start)
            #print(f"follow here: {old_state[start:start+16]},,end")
            state = old_state[start:start+16]
            res = aes(state,keyScheduler)
            #key_schedulers.append(key_sched)
            final_res.append(res)
            start = start + 16
            #print(f"start: {start}") 
        # state = word_xor(IV_rand,state[start:]) #have to do padding here
        # res = aes(state,key0)
        # final_res.append(res)
    solution.res = final_res
    #solution.key_schedulers = key_schedulers
    return solution


def ecb_mode_decrypt(solution,key0):
    enc = solution.res
    # bytes_to_remove = convert_hex_string_to_decimal(enc[-1][-1])
    # for i in range(len(enc[-1])-1,len(enc[-1])-bytes_to_remove-1,-1):
    if(len(key0)>16): #truncating key 
        key0 = key0[0:16]
        #print(len(key0))
    if(len(key0)<16):
        key0 = key0.ljust(16, '0')
    keyScheduler = KeyScheduler(key0)
    #print(f"enc is: {enc}!!!")
    old_enc = enc.copy()
    decrypted_text = [] 
    round = len(solution.res)
    index = 0
    #print(f"enc len: {len(enc)}")
    for i in range(round-1,-1,-1):
        index = round - (i+1)
        #print(index)
        dec = aes_decrypt(enc[index],keyScheduler)
        decrypted_text.append(dec)
        #print(f"printingg:{IV}")
    return decrypted_text 


def cbc_mode_encrypt(text,key):
    key_schedulers = []
    print(f"shared key in cbc encrypt: {key}")
    key0 = translate_into_hex(key)
    solution = Solution(1,2)
    #print(len(key0))
    if(len(key0)>16): #truncating key 
        key0 = key0[0:16]
        #print(len(key0))
    if(len(key0)<16):
        key0 = key0 + ['0x00'] * (16 - len(key0))
    state = translate_into_hex(text)

    #print(key0)
    start_time = time.perf_counter()
    #keyScheduler = KeyScheduler(key)
    keyScheduler = KeyScheduler(key0)
    end_time = time.perf_counter()
    execution_time = end_time - start_time

    print(f"The keyscheduler took {execution_time:.6f} seconds to execute.")
    #if(len(state)%16!=0):
    state = pkcs_7(state)
    old_state = state.copy()
    #print(f"state len is : {len(state)}")
    #random.seed(42)

    IV_rand = [random.randint(0, 255) for _ in range(16)]
    IV_rand = [hex(i) for i in IV_rand]
    IV_start = IV_rand.copy()
    final_res = []
    final_res.append(IV_start)
    #print(state)
    #print(IV_rand)
    
    if(len(state)<=16):
     #print("here")
     state = word_xor(IV_rand,state) 
     res = aes(state,keyScheduler)
     #key_schedulers.append(key_sched)
     final_res.append(res)
    else:
        start = 0 
        #print("to the big")
        while(start+16<=len(old_state)):
            #print(start)
            #print(f"follow here: {old_state[start:start+16]},,end")
            state = word_xor(IV_rand,old_state[start:start+16])
            res = aes(state,keyScheduler)
            #key_schedulers.append(key_sched)
            final_res.append(res)
            IV_rand = res 
            start = start + 16
            #print(f"start: {start}") 
        # state = word_xor(IV_rand,state[start:]) #have to do padding here
        # res = aes(state,key0)
        # final_res.append(res)

    solution.res = final_res
    #solution.key_schedulers = key_schedulers
    return solution

def cbc_mode_decrypt(solution,key0):
    IV = solution[0] #first 16 items are IV 
    enc = solution[1:]
    print(f"shared key in cbc decrypt: {key0}")
    key0 = translate_into_hex(key0)
    if(len(key0)>16): #truncating key 
        key0 = key0[0:16]
        #print(len(key0))
    if(len(key0)<16):
        key0 = key0 + ['0x00'] * (16 - len(key0))
    # bytes_to_remove = convert_hex_string_to_decimal(enc[-1][-1])
    # for i in range(len(enc[-1])-1,len(enc[-1])-bytes_to_remove-1,-1):
    keyScheduler = KeyScheduler(key0)
    #print(f"enc is: {enc}!!!")
    old_enc = enc.copy()
    decrypted_text = [] 
    round = len(solution)
    index = 0
    print(round)
    for i in range(round-1,0,-1):
        index = round - (i+1)
        dec = aes_decrypt(enc[index],keyScheduler)
        dec = word_xor(dec,IV)
        decrypted_text.append(dec)
        IV = old_enc[index]
        #print(f"printingg:{IV}")
    return decrypted_text 

def hex_to_ascii(hex_text):
    text = []
    for txt in hex_text:
        dec = convert_hex_string_to_decimal(txt)
        letter = chr(dec)  
        text.append(letter)
    return "".join(text)
    

def user_encrypt(text,key):

#numbers = translate_into_hex("Thats my Kung Fu")
#print(numbers)
#matrix = transform_into_matrix(numbers)
#print(matrix)
    solution = Solution(1,2)
    start_time = time.perf_counter()
    #key = "BUET CSE20 Batch"
    solution = cbc_mode_encrypt(text,key)
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(f"The encryption took {execution_time:.6f} seconds to execute.")
    print(f"key: {key}")
    print(f"Encypted text: {solution.res}")
    return solution
    # view_matrix(matrix)
    # enc,ks = aes(translate_into_hex("Two One Nine Two"),translate_into_hex("Thats my Kung Fu"))
    # print(enc)
    # print(ks)

    #print(solution.res)

def user_decrypt(solution,key):
    start_time = time.perf_counter()
    dec = cbc_mode_decrypt(solution,key)
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(f"The decryption took {execution_time:.6f} seconds to execute.")
    print(dec)
    pad = convert_hex_string_to_decimal(dec[-1][-1])
    dec[-1] = dec[-1][:-pad]
    
    print(f"decrypted in Hex:{dec}")
    result = ""
    print("Decrypted in text: ")
    for texts in dec:
        result += hex_to_ascii(texts)
        #print(hex_to_ascii(texts),end="")
    return result 

# enc = user_encrypt("Asif","Bhaat")
# print(user_decrypt(enc.res,"Bhaat"))

# dec = ecb_mode_decrypt(solution)
# print(dec[-1])
# pad = convert_hex_string_to_decimal(dec[-1][-1])
# dec[-1] = dec[-1][:-pad]
# print(dec[-1])
# for texts in dec:
#     print(hex_to_ascii(texts),end="")

# dec = aes_decrypt(enc,ks)
# print(dec)
# print(hex_to_ascii(dec))

# import matplotlib.pyplot as plt
# from PIL import Image
# import numpy as np

# # -----------------------------
# # Read image
# # -----------------------------
# img = Image.open("sampleio.png").convert("RGB")
# img_array = np.array(img)

# height, width, channels = img_array.shape

# # Flatten into bytes
# plain_bytes = img_array.flatten().tolist()

# # ---------------------------------
# # Encrypt using your AES CBC
# # ---------------------------------
# key = "Thats my Kung Fu"

# encrypted_bytes = cbc_mode_encrypt(plain_bytes, key)
# # encrypt_bytes_cbc should return a list of integers (0-255)

# encrypted_array = np.array(encrypted_bytes[:len(plain_bytes)],
#                            dtype=np.uint8).reshape(height, width, channels)

# # ---------------------------------
# # Decrypt
# # ---------------------------------
# decrypted_bytes = cbc_mode_decrypt(encrypted_bytes, key)

# decrypted_array = np.array(decrypted_bytes[:len(plain_bytes)],
#                            dtype=np.uint8).reshape(height, width, channels)

# # ---------------------------------
# # Display
# # ---------------------------------
# plt.figure(figsize=(15,5))

# plt.subplot(1,3,1)
# plt.imshow(img_array)
# plt.title("Original")
# plt.axis("off")

# plt.subplot(1,3,2)
# plt.imshow(encrypted_array)
# plt.title("Encrypted")
# plt.axis("off")

# plt.subplot(1,3,3)
# plt.imshow(decrypted_array)
# plt.title("Decrypted")
# plt.axis("off")

# plt.show()