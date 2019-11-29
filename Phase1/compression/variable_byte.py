
class VariableByteCompressor:

    @staticmethod
    def compress_to_file(dictionary):
        f = open("variable_byte.txt", "w")
        # positional indexing {t_id: {doc_id: [pos]}}
        sorted_dictionary = sorted(dictionary)
        f.write(str(len(sorted_dictionary)) + '\n')
        for t_id in sorted(dictionary):
            posting_dict = dictionary[t_id]
            doc_id_list = sorted(posting_dict)
            f.write(VariableByteCompressor.compress_posting_list(doc_id_list) + '\n')
            for doc_id in doc_id_list:
                f.write(VariableByteCompressor.compress_posting_list(posting_dict[doc_id]) + '\n')

    @staticmethod
    def compress_posting_list(posting_list):
        vbcode = ''
        if not len(posting_list):
            return vbcode
        vbcode += VariableByteCompressor.convert_int_to_vbcode(posting_list[0])
        for i in range(1, len(posting_list)):
            vbcode += VariableByteCompressor\
                .convert_int_to_vbcode(posting_list[i] - posting_list[i - 1])
        return vbcode

    @staticmethod
    def convert_int_to_vbcode(num):
        binary_str = format(num, 'b')
        end_ptr = len(binary_str)
        vbcode = ''
        continuation_bit = '1'
        while end_ptr > 0:
            start_ptr = max(0, end_ptr - 7)
            vbcode = VariableByteCompressor\
                         .fill_vb_8bits(binary_str[start_ptr:end_ptr], continuation_bit) \
                     + vbcode
            continuation_bit = '0'
            end_ptr = start_ptr
        return vbcode

    @staticmethod
    def fill_vb_8bits(binary_str, continuation_bit):
        if len(binary_str) > 7:
            raise Exception('wrong input argument!')
        return str(continuation_bit) + '0'*(7 - len(binary_str)) + binary_str

VariableByteCompressor.compress_to_file({0:
                                             {1: [824, 829, 215406],
                                              2: [824, 829, 215406]},
                                         1:
                                             {1: [824, 829, 215406],
                                              2: [824, 829, 215406]}
                                         })
# print(VariableByteCompressor.compress_posting_list([824, 829, 215406]))
# print(VariableByteCompressor.convert_int_to_vbcode(13))
# print(VariableByteCompressor.fill_vb_8bits('0010001', '0'))


class VariableByteDecompressor:

    @staticmethod
    def decompress_from_file():
        f = open("var.txt", "r")
        dictionary = {}
        tid_num = int(f.readline())
        for i in range(tid_num):
            tid_dict = {}
            doc_list = VariableByteDecompressor.decompress_posting_list(f.readline().strip('\n'))

            for doc_id in doc_list:
                posting_list = VariableByteDecompressor.decompress_posting_list(f.readline().strip('\n'))
                tid_dict[doc_id] = posting_list
            dictionary[i] = tid_dict
        return dictionary

    @staticmethod
    def decompress_posting_list(vbcode):
        vbcode = [vbcode[i:i+8] for i in range(0, len(vbcode), 8)]
        postings_list = []
        int_vbcode_list = []
        start_iterator = 0
        while start_iterator < len(vbcode):
            end_iterator = start_iterator + 1
            while vbcode[end_iterator - 1][0] == '0':
                end_iterator += 1
            int_vbcode_list.append(VariableByteDecompressor.
                                 convert_vbcode_to_int(vbcode[start_iterator:end_iterator]))
            start_iterator = end_iterator
        prev_num = 0
        for gap in int_vbcode_list:
            next_num = prev_num + gap
            postings_list.append(next_num)
            prev_num = next_num
        return postings_list

    @staticmethod
    def convert_vbcode_to_int(vbcode):
        for i in range(len(vbcode)):
            vbcode[i] = vbcode[i][1:]
        binary_str = ''.join(vbcode)
        return int(binary_str, 2)

print(VariableByteDecompressor.decompress_from_file())
# print(VariableByteDecompressor.decompress_posting_list(
#     ['00000110', '10111000', '10000101', '00001101', '00001100', '10110001']))
# print(VariableByteDecompressor.convert_vbcode_to_int(['100001', '0000100']))
