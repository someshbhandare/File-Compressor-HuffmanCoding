import os
from HuffmanCoding import HuffmanCoding

print("\n++++++++++++++++++++++++++++++++++++ File Zipper ++++++++++++++++++++++++++++++++++++")
print("1. Compress")
print("2. Decompress")

h = HuffmanCoding()
while True:
    choice = input("\nEnter your Choice(Press any key to exit): ")

    if(choice.strip() == "1"):
        path = r""+ input("Enter Path: ")
        output_path = h.compress(path)
        print("Compressed file path - " + output_path)

    elif(choice.strip() == "2"):
        path = r""+ input("Enter Path: ")
        output_path = h.decompress(path)
        print("Decompressed file path - " + output_path)

    else:
        break
