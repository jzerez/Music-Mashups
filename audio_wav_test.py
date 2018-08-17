import wave
import struct
import matplotlib.pyplot as plt

def HexToByte( hexStr ):
    """
    Convert a string hex byte values into a byte string. The Hex Byte values may
    or may not be space separated.
    """
    # The list comprehension implementation is fractionally slower in this case
    #
    #    hexStr = ''.join( hexStr.split(" ") )
    #    return ''.join( ["%c" % chr( int ( hexStr[i:i+2],16 ) ) \
    #                                   for i in range(0, len( hexStr ), 2) ] )

    bytes = []

    hexStr = ''.join( hexStr.split(" ") )

    for i in range(0, len(hexStr), 2):
        bytes.append( chr( int (hexStr[i:i+2], 16 ) ) )

    return ''.join( bytes )

# 127249
CHUNK = 44100
#
f = wave.open('Loud_Pipes-BcoPKWzLjrE.wav', 'rb')
f.setpos(69000)
#
b = f.readframes(CHUNK)
print(b[0:50])
danny = struct.unpack(str(int(len(b)/2)) + 'h', b)

robbie = struct.unpack(str(int(len(b))) + 'b', b)
plt.plot(danny[::2])
plt.show()

print('DANNY')
print(danny[0:100])
print('raw data ', danny[0])
print('hexxed data ', hex(danny[0]))
print('byted data ???: ', hex(danny[0]).encode('utf-8'))
print(max(danny))
print(len(danny))

print('ROBERT')
robert = struct.pack('5'+'h', (*danny[0:5]))
print('robert type: ', type(robert))
print('robert len: ', len(robert))
print('one of robert: ', robert)

final = struct.pack(str(len(danny[::2])) + 'h', *danny[::2])


# print(b)
# print(len(b))
# print(struct.unpack('4b', f.readframes(1)))
# print(f.readframes(10000).decode('utf-8'))
# print(type(f.readframes(25)))
# t = ()
# for substring in (str(f.getparams()).split('(')[1].split(', ')):
#     t += (substring.split(')')[0].split('=')[1],)
# print(t)
# print(f.getparams())
# f.setpos(60000)
# # for i in range(30):
# #     b = f.readframes(1)
# #     data = struct.unpack(str(len(b)) + 'b', b)
# #     print(b)
# #     print(data)
#
# read_data = (f.readframes(44100))
# print(type(read_data))
# write_data1 = read_data[::4]
# write_data2 = read_data[1::4]
# write_data = [None] * (len(write_data1) + len(write_data2))
# write_data[::2] = write_data1
# write_data[1::2] = write_data2
#
# print(type(write_data[1]))


# help = struct.unpack(str(int(len(final)/4)) + 'i', final)
# print(help[:20])
# plt.plot(help)
# plt.show()
# for data in read_data[::2]:
#     if i % 2 == 0:
#         write_data += hex(data).encode('utf-8')
#         write_data += hex(read_data[i+1]).encode('utf-8')
#     i += 1

print(type(final))

testf = wave.open('test.wav', 'wb')
testf.setnchannels(1)
testf.setsampwidth(f.getsampwidth())
testf.setframerate(f.getframerate()/1)
testf.setnframes(len(danny[::2]))

print(testf.tell())
testf.writeframes(final*10)
print('hi')
