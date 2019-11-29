

class GammaCodeCompressor:

    @staticmethod
    def compress_to_file(dictionary):
        f = open("gamma_code.txt", "w")
        # positional indexing {t_id: {doc_id: [pos]}}
        sorted_dictionary = sorted(dictionary)
        f.write(str(len(sorted_dictionary)) + '\n')
        for t_id in sorted(dictionary):
            posting_dict = dictionary[t_id]
            doc_id_list = sorted(posting_dict)
            print(doc_id_list)
            f.write(GammaCodeCompressor.compress_posting_list(doc_id_list) + '\n')
            for doc_id in doc_id_list:
                f.write(GammaCodeCompressor.compress_posting_list(posting_dict[doc_id]) + '\n')

    @staticmethod
    def compress_posting_list(posting_list):
        gamma_code = ''
        if not len(posting_list):
            return gamma_code
        gamma_code += GammaCodeCompressor.convert_int_to_gamma_code(posting_list[0])
        for i in range(1, len(posting_list)):
            gamma_code += GammaCodeCompressor.\
                convert_int_to_gamma_code(posting_list[i] - posting_list[i - 1])
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

GammaCodeCompressor.compress_to_file({0:
                                             {1: [824, 829, 215406],
                                              2: [824, 829, 215406]},
                                         1:
                                             {1: [824, 829, 215406],
                                              2: [824, 829, 215406]}
                                         })

# print(GammaCodeCompressor.compress_posting_list([2, 5, 14, 1039]))
# print(GammaCodeCompressor.compress_posting_list([824, 829, 215406]))
# print(GammaCodeCompressor.convert_int_to_gamma_code(1024))
# print(GammaCodeCompressor.convert_int_to_gamma_code(1023))
# print(GammaCodeCompressor.convert_int_to_gamma_code(1025))
# print(GammaCodeCompressor.unary_code(10))
# print(GammaCodeCompressor.binary_offset(1024) + " " +
#       GammaCodeCompressor.binary_offset(1025) + " " +
#       GammaCodeCompressor.binary_offset(1023))


class GammaCodeDecompressor:

    @staticmethod
    def decompress_from_file():
        f = open("gamma_code.txt", "r")
        dictionary = {}
        tid_num = int(f.readline())
        for i in range(tid_num):
            tid_dict = {}
            doc_list = GammaCodeDecompressor.decompress_posting_list(f.readline().strip('\n'))

            for doc_id in doc_list:
                posting_list = GammaCodeDecompressor.decompress_posting_list(f.readline().strip('\n'))
                tid_dict[doc_id] = posting_list
            dictionary[i] = tid_dict
        return dictionary

    @staticmethod
    def decompress_posting_list(gamma_code):
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

print(GammaCodeDecompressor.decompress_from_file())
# print(GammaCodeDecompressor.decompress_posting_list('1001011110001111111111100000000001'))
# print(GammaCodeDecompressor.decompress_posting_list('11111111101001110001100111111111111111111010100011000110001'))
