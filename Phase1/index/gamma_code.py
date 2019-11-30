class GammaCodeCompressor:

    @staticmethod
    def compress_to_binary_file(dictionary, file='gamma_index.txt'):
        f = open(file, "wb")
        # positional indexing {t_id: {doc_id: [pos]}}
        sorted_dictionary = sorted(dictionary)
        f.write(int(len(sorted_dictionary)).to_bytes(4, 'little') + b'\n')
        for t_id in sorted(dictionary):
            posting_dict = dictionary[t_id]
            doc_id_list = sorted(posting_dict)
            gamma_code = GammaCodeCompressor.__compress_posting_list(doc_id_list)
            GammaCodeCompressor.__write_gamma_code(f, gamma_code)
            for doc_id in doc_id_list:
                gamma_code = GammaCodeCompressor.__compress_posting_list(posting_dict[doc_id])
                GammaCodeCompressor.__write_gamma_code(f, gamma_code)

    @staticmethod
    def compress_to_binary_file(dictionary, file='gamma_index.txt'):
        f = open(file, "wb")
        # positional indexing {t_id: {doc_id: [pos]}}
        sorted_dictionary = sorted(dictionary)
        f.write(int(len(sorted_dictionary)).to_bytes(4, 'little'))
        for t_id in sorted_dictionary:
            posting_dict = dictionary[t_id]
            doc_id_list = sorted(posting_dict)
            variable_byte = GammaCodeCompressor.__compress_posting_list(doc_id_list)
            GammaCodeCompressor.__write_gamma_code(f, variable_byte)
            for doc_id in doc_id_list:
                variable_byte = GammaCodeCompressor.__compress_posting_list(posting_dict[doc_id])
                GammaCodeCompressor.__write_gamma_code(f, variable_byte)

    @staticmethod
    def __write_gamma_code(f, gamma_code):
        gamma_code = '0' * (8 - (len(gamma_code) % 8)) + gamma_code
        f.write(int(len(gamma_code)/8).to_bytes(4, 'little'))
        for i in range(0, len(gamma_code), 8):
            f.write(int(gamma_code[i:i + 8], 2)
                    .to_bytes(1, 'little'))

    @staticmethod
    def __compress_posting_list(posting_list):
        posting_list = GammaCodeCompressor.__preprocess_posting_list(posting_list)
        gamma_code = ''
        if not len(posting_list):
            return gamma_code
        gamma_code += GammaCodeCompressor.__convert_int_to_gamma_code(posting_list[0])
        for i in range(1, len(posting_list)):
            gamma_code += GammaCodeCompressor. \
                __convert_int_to_gamma_code(posting_list[i] - posting_list[i - 1])
        return gamma_code

    @staticmethod
    def __preprocess_posting_list(posting_list):
        result_list = []
        for num in posting_list:
            result_list.append(num + 1)
        return result_list

    @staticmethod
    def __convert_int_to_gamma_code(num):
        offset = GammaCodeCompressor.__binary_offset(num)
        unary = GammaCodeCompressor.__unary_code(len(offset))
        return unary + offset

    @staticmethod
    def __unary_code(length):
        return '1' * length + '0'

    @staticmethod
    def __binary_offset(num):
        return format(num, 'b')[1:]


class GammaCodeDecompressor:

    @staticmethod
    def decompress_from_binary_file(file='gamma_index.txt'):
        f = open(file, "rb")
        dictionary = {}
        tid_num = int(format(int.from_bytes(f.read(4), 'little')))
        for i in range(tid_num):
            tid_dict = {}
            doc_list = GammaCodeDecompressor.read_posting_list(f)
            for doc_id in doc_list:
                posting_list = GammaCodeDecompressor.read_posting_list(f)
                tid_dict[doc_id] = posting_list
            dictionary[i] = tid_dict
        return dictionary

    @staticmethod
    def read_posting_list(f):
        length = int(format(int.from_bytes(f.read(4), 'little')))
        posting_byte = f.read(length)
        gamma_code = ''
        for byte in posting_byte:
            gamma_code += format(byte, '08b')
        gamma_code = gamma_code.lstrip('0')
        return GammaCodeDecompressor.__decompress_posting_list(gamma_code)

    @staticmethod
    def __decompress_posting_list(gamma_code):
        start_ptr = 0
        postings_list = []
        prev_num = 0
        while start_ptr < len(gamma_code):
            end_unary_ptr = start_ptr
            while gamma_code[end_unary_ptr] == '1':
                end_unary_ptr += 1
            offset_length = end_unary_ptr - start_ptr
            offset = '1' + gamma_code[end_unary_ptr + 1:end_unary_ptr + offset_length + 1]
            start_ptr = end_unary_ptr + offset_length + 1
            cur_num = int(offset, 2) + prev_num
            postings_list.append(cur_num)
            prev_num = cur_num
        return GammaCodeDecompressor.__preprocess_posting_list(postings_list)

    @staticmethod
    def __preprocess_posting_list(posting_list):
        result_list = []
        for num in posting_list:
            result_list.append(num - 1)
        return result_list
