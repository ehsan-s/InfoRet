class VariableByteCompressor:

    @staticmethod
    def compress_to_binary_file(dictionary, file='var_index.txt'):
        f = open(file, "wb")
        # positional indexing {t_id: {doc_id: [pos]}}
        sorted_dictionary = sorted(dictionary)
        f.write(int(len(sorted_dictionary)).to_bytes(4, 'little'))
        for t_id in sorted_dictionary:
            posting_dict = dictionary[t_id]
            doc_id_list = sorted(posting_dict)
            variable_byte = VariableByteCompressor.__compress_posting_list(doc_id_list)
            VariableByteCompressor.__write_variable_byte(f, variable_byte)
            for doc_id in doc_id_list:
                variable_byte = VariableByteCompressor.__compress_posting_list(posting_dict[doc_id])
                VariableByteCompressor.__write_variable_byte(f, variable_byte)

    @staticmethod
    def __write_variable_byte(f, variable_byte):
        f.write(int(len(variable_byte)).to_bytes(4, 'little'))
        for i in range(len(variable_byte)):
            f.write(variable_byte[i])
            f.flush()

    @staticmethod
    def __compress_posting_list(posting_list):
        vbcode = []
        if not len(posting_list):
            return vbcode
        vbcode.extend(VariableByteCompressor.__convert_int_to_vbcode(posting_list[0]))
        for i in range(1, len(posting_list)):
            vbcode.extend(VariableByteCompressor.
                          __convert_int_to_vbcode(posting_list[i] - posting_list[i - 1]))
        return vbcode

    @staticmethod
    def __convert_int_to_vbcode(num):
        binary_str = format(num, 'b')
        end_ptr = len(binary_str)
        vbcode = []
        continuation_bit = '1'
        while end_ptr > 0:
            start_ptr = max(0, end_ptr - 7)
            vbcode.insert(0, VariableByteCompressor.
                          __fill_vb_8bits(binary_str[start_ptr:end_ptr], continuation_bit))
            continuation_bit = '0'
            end_ptr = start_ptr
        return vbcode

    @staticmethod
    def __fill_vb_8bits(binary_str, continuation_bit):
        if len(binary_str) > 7:
            raise Exception('wrong input argument!')
        byte = str(continuation_bit) + '0' * (7 - len(binary_str)) + binary_str
        return int(byte, 2).to_bytes(1, 'little')


class VariableByteDecompressor:

    @staticmethod
    def decompress_from_binary_file(file='var_index.txt'):
        f = open(file, "rb")
        dictionary = {}
        tid_num = int(format(int.from_bytes(f.read(4), 'little')))
        for i in range(tid_num):
            tid_dict = {}
            doc_list = VariableByteDecompressor.read_posting_list(f)
            for doc_id in doc_list:
                posting_list = VariableByteDecompressor.read_posting_list(f)
                tid_dict[doc_id] = posting_list
            dictionary[i] = tid_dict
        return dictionary

    @staticmethod
    def read_posting_list(f):
        length = int(format(int.from_bytes(f.read(4), 'little')))
        posting_byte = f.read(length)
        variable_byte = []
        for byte in posting_byte:
            variable_byte.append(format(byte, '08b'))
        return VariableByteDecompressor.__decompress_posting_list(variable_byte)

    @staticmethod
    def __decompress_posting_list(vbcode):
        postings_list = []
        int_vbcode_list = []
        start_iterator = 0
        while start_iterator < len(vbcode):
            end_iterator = start_iterator + 1
            while vbcode[end_iterator - 1][0] == '0':
                end_iterator += 1
            int_vbcode_list.append(VariableByteDecompressor.
                                   __convert_vbcode_to_int(vbcode[start_iterator:end_iterator]))
            start_iterator = end_iterator
        prev_num = 0
        for gap in int_vbcode_list:
            next_num = prev_num + gap
            postings_list.append(next_num)
            prev_num = next_num
        return postings_list

    @staticmethod
    def __convert_vbcode_to_int(vbcode):
        for i in range(len(vbcode)):
            vbcode[i] = vbcode[i][1:]
        binary_str = ''.join(vbcode)
        return int(binary_str, 2)
