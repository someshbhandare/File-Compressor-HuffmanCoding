import os
import heapq

class HuffmanCoding:
    def __init__(self) -> None:
        self.heap = []
        self.codes = {}
        self.reverseMapping = {}

    class HeapNode:
        def __init__(self, char, freq) -> None:
            self.char = char
            self.freq = freq
            self.left = None
            self.right = None

        def __lt__(self, other) -> bool:
            return self.freq < other.freq

        def __eq__(self, other) -> bool:
            if(other==None):
                return False
            if(not isinstance(other, self.HeapNode)):
                return False
            return self.freq == other.freq

    def make_frequency_dict(self, text):
        # make frequency dictionary
        frequency = {}
        for char in text:
            if not char in frequency:
                frequency[char] = 0
            frequency[char] += 1
        return frequency

    def make_heap(self, frequency):
        # make priority queue
        for i in frequency:
            node = self.HeapNode(i, frequency[i])
            heapq.heappush(self.heap, node)

    def merge_nodes(self):
        # build huffman tree (by merging 2 extracted nodes from pq) 
        # and save new node as root of 2 extracted node
        while(len(self.heap)>1):
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)

            merged = self.HeapNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2

            heapq.heappush(self.heap, merged)

    def make_codes_helper(self, node, current_code):
        if(node == None):
            return
        if(node.char != None):
            self.codes[node.char] = current_code
            self.reverseMapping[current_code] = node.char
        
        self.make_codes_helper(node.left, current_code+"0")
        self.make_codes_helper(node.right, current_code+"1")

    def make_codes(self):
        # assign '0' to left edges & '1' to right edges of Huffman Tree or/ vice versa
        # make codes (by traversing from root to character) for each character 
        # and save
        root = heapq.heappop(self.heap)
        current_code = ""
        self.make_codes_helper(root, current_code)
    
    def get_encoded_text(self, text):
        # return encoded text
        encoded_text = ""
        for char in text:
            encoded_text += self.codes[char]
        return encoded_text

    def padd_encoded_text(self, encoded_text):
        # add padding to encoded text when bit-stream is not multiple of 8
        extra_padding = 8 - len(encoded_text)%8
        for _ in range(extra_padding):
            encoded_text += "0"
        padded_info = "{0:8b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        return encoded_text

    def get_byte_array(self, padded_encoded_text):
        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i+8]
            b.append(int(byte, 2))
        return b


    def compress(self, input_path):
        filename, file_extension = os.path.splitext(input_path)
        output_path = f"{filename}.bin"  # filename + ".bin"

        with open(input_path, "r") as file, open(output_path, "wb") as output:
            text = file.read()
            text = text.rstrip()

            frequency = self.make_frequency_dict(text)
            
            self.make_heap(frequency)
            self.merge_nodes()
            self.make_codes()

            encoded_text = self.get_encoded_text(text)
            padded_encoded_text = self.padd_encoded_text(encoded_text)

            b = self.get_byte_array(padded_encoded_text)
            
            output.write(bytes(b))
            return output_path

    def remove_padding(self, bit_string):
        padding_info = bit_string[:8]
        extra_padding = int(padding_info, 2)

        bit_string = bit_string[8:]
        encoded_text = bit_string[:-1*extra_padding]
        return encoded_text

    def get_decoded_text(self, encoded_text):
        current_code = ""
        decoded_text = ""

        for bit in encoded_text:
            current_code += bit
            if(current_code in self.reverseMapping):
                decoded_text += self.reverseMapping[current_code]
                current_code = ""
        return decoded_text

    def decompress(self, input_path):
        filename, file_extension = os.path.splitext(input_path)
        output_path = filename + "_decompressed" + ".txt"

        with open(input_path, "rb") as file, open(output_path, "w") as output:
            bit_string = ""

            byte = file.read(1)
            while(len(byte)>0):
                byte = ord(byte)
                byte = bin(byte)[2:].rjust(8,"0")
                bit_string += byte
                byte = file.read(1)
            
            encoded_text = self.remove_padding(bit_string)
            decoded_text = self.get_decoded_text(encoded_text)
            output.write(decoded_text)
            return output_path

# if __name__ == "__main__":
#     huff = HuffmanCoding("sample.txt")
#     huff.compress()
#     huff.decompress("sample.bin")
