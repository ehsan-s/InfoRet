class GammaCodeCompressor:

    @staticmethod
    def compress_to_file(dictionary, file='gamma_index.txt'):
        f = open(file, "w")
        # positional indexing {t_id: {doc_id: [pos]}}
        sorted_dictionary = sorted(dictionary)
        f.write(str(len(sorted_dictionary)) + '\n')
        for t_id in sorted(dictionary):
            posting_dict = dictionary[t_id]
            doc_id_list = sorted(posting_dict)
            print(doc_id_list)
            f.write(GammaCodeCompressor.__compress_posting_list(doc_id_list) + '\n')
            for doc_id in doc_id_list:
                f.write(GammaCodeCompressor.__compress_posting_list(posting_dict[doc_id]) + '\n')

    @staticmethod
    def __compress_posting_list(posting_list):
        gamma_code = ''
        if not len(posting_list):
            return gamma_code
        gamma_code += GammaCodeCompressor.__convert_int_to_gamma_code(posting_list[0])
        for i in range(1, len(posting_list)):
            gamma_code += GammaCodeCompressor. \
                __convert_int_to_gamma_code(posting_list[i] - posting_list[i - 1])
        return gamma_code

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
    def decompress_from_file(file='gamma_index.txt'):
        f = open(file, "r")
        dictionary = {}
        tid_num = int(f.readline())
        for i in range(tid_num):
            tid_dict = {}
            doc_list = GammaCodeDecompressor.__decompress_posting_list(f.readline().strip('\n'))

            for doc_id in doc_list:
                posting_list = GammaCodeDecompressor.__decompress_posting_list(f.readline().strip('\n'))
                tid_dict[doc_id] = posting_list
            dictionary[i] = tid_dict
        return dictionary

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

        return postings_list
