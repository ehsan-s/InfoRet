
class VariableByteCompressor:

    @staticmethod
    def compress(postings_list):
        vbcode = []
        if not len(postings_list):
            return vbcode
        vbcode.extend(VariableByteCompressor.convert_int_to_vbcode(postings_list[0]))
        for i in range(1, len(postings_list)):
            vbcode.extend(VariableByteCompressor.
                          convert_int_to_vbcode(postings_list[i] - postings_list[i-1]))
        return vbcode

    @staticmethod
    def convert_int_to_vbcode(num):
        binary_str = format(num, 'b')
        end_ptr = len(binary_str)
        vbcode = []
        continuation_bit = '1'
        while end_ptr > 0:
            start_ptr = max(0, end_ptr - 7)
            vbcode.insert(0, VariableByteCompressor.
                          fill_vb_8bits(binary_str[start_ptr:end_ptr], continuation_bit))
            continuation_bit = '0'
            end_ptr = start_ptr
        return vbcode

    @staticmethod
    def fill_vb_8bits(binary_str, continuation_bit):
        if len(binary_str) > 7:
            raise Exception('wrong input argument!')
        return str(continuation_bit) + '0'*(7 - len(binary_str)) + binary_str


print(VariableByteCompressor.compress([824, 829, 215406]))
print(VariableByteCompressor.convert_int_to_vbcode(13))
print(VariableByteCompressor.fill_vb_8bits('0010001', '0'))


class VariableByteDecompressor:

    @staticmethod
    def decompress(vbcode):
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


print(VariableByteDecompressor.decompress(
    ['00000110', '10111000', '10000101', '00001101', '00001100', '10110001']))
print(VariableByteDecompressor.convert_vbcode_to_int(['100001', '0000100']))
