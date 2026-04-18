import tiktoken

enc=tiktoken.encoding_for_model("gpt-4o")

text=input("hey there what is your name:")
tokens=enc.encode(text)                          #tokenniztion

                         
#tokens [82, 5848, 280, 2667, 38610]
print("tokens: ",tokens)                


decoded = enc.decode( )

print("decoded token : ",decoded)