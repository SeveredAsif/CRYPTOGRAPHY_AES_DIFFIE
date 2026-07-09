#target is, giving a plaintext and key and get the encrypted text after 10 rounds. implement a key generator module 
from aes_helpers import Sbox, InvSbox, Rcon, Mixer, InvMixer, gf_mult 
import random 
class KeyScheduler:
  def __init__(self, key):
    self.key = key
    self.start = 0
    self.key_list = _calculate_key(self.key)
    #print(len(self.key_list))

  def get_key(self):
      return_val= self.key_list[self.start:self.start+4]
      self.start = self.start+4 
      return return_val
  


def _calculate_key(key):
    key_init = transform_into_matrix(key)
    key_list = key_init.copy()
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
            #print(key_list) 
        else:
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

def g(key_list):
    shifted_arr = byte_left_shift(key_list[-1],1)
    return change_arr_using_sbox(shifted_arr)
    

def translate_into_hex(text:str):
    number = []
    
    for i in text:
        #print(hex(ord(i))) 
        number.append(hex(ord(i)))
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



def aes(state,key):
    #key0 = translate_into_hex(key)
    keyScheduler = KeyScheduler(key)
    round_key = keyScheduler.get_key()
     
    print(f"state:{state},len:{len(state)}")
    #print(f"round_key:{round_key}")
    state = word_xor(state,round_key)
    statetoshow = transform_into_matrix(state) 
    #view_matrix(statetoshow)
    for round in range(10):
        print(f"round: {round+1}")
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
        round_key = keyScheduler.get_key()
        state = word_xor(state,round_key)
        statetoshow = transform_into_matrix(state) 
        #view_matrix(statetoshow)
        
    return state    


def cbc_mode(text,key):
    key0 = translate_into_hex(key)
    #print(len(key0))
    if(len(key0)>16): #truncating key 
        key0 = key0[0:16]
        #print(len(key0))
    state = translate_into_hex(text)
    old_state = state.copy()
    print(f"state len is : {len(state)}")
    random.seed(42)

    IV_rand = [random.randint(0, 255) for _ in range(16)]
    IV_rand = [hex(i) for i in IV_rand]
    IV_start = IV_rand.copy()
    final_res = []
    #print(state)
    #print(IV_rand)
    
    if(len(state)<=16):
     print("here")
     state = word_xor(IV_rand,state) 
     aes(state,key0)
    else:
        start = 0 
        print("to the big")
        while(start+16<len(old_state)):
            print(start)
            state = word_xor(IV_rand,old_state[start:start+16])
            res = aes(state,key0)
            final_res.append(res)
            IV_rand = res 
            start = start + 16
            print(f"start: {start}") 
        # state = word_xor(IV_rand,state[start:]) #have to do padding here
        # res = aes(state,key0)
        # final_res.append(res)

   
numbers = translate_into_hex("Thats my Kung Fu")
#print(numbers)
matrix = transform_into_matrix(numbers)
#print(matrix)
cbc_mode("Two One Nine Two Two One Nine Two Two One Nine Two Two One Nine Two Two One Nine Two Two One Nine Two","Thats my Kung Fu")
#view_matrix(matrix)
#aes("Two One Nine Two","Thats my Kung Fu")