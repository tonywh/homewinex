import struct

''' Read data from a BBC format a datafile
'''

def readFloat40(data, offset):
    ''' Read a 40-bit float from the data file
    '''
    # First 4-bytes are little-endian mantissa. The top bit which is always
    # set is overwritten by a sign bit.
    # Read the mantissa as an integer.
    mant = struct.unpack_from('<i', data, offset)[0]
    mant >>= 1                  # Make space for the top bit, sign bit extends
    mant = mant | 0x40000000    # Set the top bit, i.e. bit below the new sign bit

    # 5th byte is an exponent. Read the exponent as an integer and adjust it
    # to get the correct float value from the mantissa
    exp = struct.unpack_from('B', data, offset+4)[0]
    exp -= 158

    # Calculate the float value and round to 6 decimal places
    return round(float(mant) * 2**exp, 6), offset+5

def readString(data, offset):
    ''' Read a <CR> terminated string from the data file
    '''
    i = offset
    string = ''
    while data[i] != 0x0D:
        i += 1
    string += str(data[offset:i], 'utf-8')
    return string, i+1

def readRecord(data, offset):
    ''' Read one record from the data file
    '''
    record = {}
    i = offset
    record['Id'], i = readFloat40(data, i)
    record['Fruit'], i = readString(data, i)
    record['Variety'], i = readString(data, i)
    record['TA_pc'], i = readFloat40(data, i)
    record['Sugar_pc'], i = readFloat40(data, i)
    record['UnSugar_pc'], i = readFloat40(data, i)
    record['SoluSolid_pc'], i = readFloat40(data, i)
    record['BodyToAcid_pc'], i = readFloat40(data, i)
    record['Tannin_pc'], i = readFloat40(data, i)
    record['Pectin'], i = readString(data, i)
    record['Pectolaise'], i = readString(data, i)
    record['Redness'], i = readFloat40(data, i)
    record['Brownness'], i = readFloat40(data, i)
    record['Starch_pc'], i = readFloat40(data, i)
    record['Method'], i = readFloat40(data, i)
    record['Solid'], i = readString(data, i)
    record['SuggMax_g_gal'], i = readFloat40(data, i)
    return record, i
