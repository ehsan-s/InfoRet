

class GammaCodeCompressor:

    @staticmethod
    def compress(postings_list):
        gamma_code = ''
        if not len(postings_list):
            return gamma_code
        gamma_code += GammaCodeCompressor.convert_int_to_gamma_code(postings_list[0])
        for i in range(1, len(postings_list)):
            gamma_code += GammaCodeCompressor.\
                convert_int_to_gamma_code(postings_list[i] - postings_list[i - 1])
        return gamma_code

    @staticmethod
    def convert_int_to_gamma_code(num):
        offset = GammaCodeCompressor.binary_offset(num)
        unary = GammaCodeCompressor.unary_code(len(offset))
        return unary + offset

    @staticmethod
    def unary_code(length):
        return '1'*length + '0'

    @staticmethod
    def binary_offset(num):
        return format(num, 'b')[1:]

print(GammaCodeCompressor.compress([2, 5, 14, 1039]))
print(GammaCodeCompressor.compress([824, 829, 215406]))
print(GammaCodeCompressor.convert_int_to_gamma_code(1024))
print(GammaCodeCompressor.convert_int_to_gamma_code(1023))
print(GammaCodeCompressor.convert_int_to_gamma_code(1025))
print(GammaCodeCompressor.unary_code(10))
print(GammaCodeCompressor.binary_offset(1024) + " " +
      GammaCodeCompressor.binary_offset(1025) + " " +
      GammaCodeCompressor.binary_offset(1023))


class GammaCodeDecompressor:

    @staticmethod
    def decompress(gamma_code):
        start_ptr = 0
        postings_list = []
        prev_num = 0
        while start_ptr < len(gamma_code):
            end_unary_ptr = start_ptr
            while gamma_code[end_unary_ptr] == '1':
                end_unary_ptr += 1
            offset_length = end_unary_ptr - start_ptr
            offset = '1' + gamma_code[end_unary_ptr+1:end_unary_ptr+offset_length+1]
            start_ptr = end_unary_ptr + offset_length + 1
            cur_num = int(offset, 2) + prev_num
            postings_list.append(cur_num)
            prev_num = cur_num

        return postings_list

print(GammaCodeDecompressor.decompress('1001011110001111111111100000000001'))
print(GammaCodeDecompressor.decompress('11111111101001110001100111111111111111111010100011000110001'))
