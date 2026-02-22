import sys
import time
import struct
from crc import Calculator, Crc32

magic_number = 0x27051956
empty_word = 0x00000000
calculator = Calculator(Crc32.CRC32, optimized=True)

def name_to_32bit(name:str):
    name = name.encode('ascii')
    if len(name) > 32:
        name = name[:31]
    else:
        name += b'\x00' * (32 - len(name))
    return name

def main(file):
    with open(file, "rb") as f:
        main_body = f.read()

    main_body_size = len(main_body)
    body = struct.pack('>II',
                        main_body_size,
                        empty_word) + main_body


    body_crc = calculator.checksum(body)
    body_len = len(body)

    epoch_time = int(time.time())

    # This parameters hardcoded for ARM linux for now   #TODO: maybe add parametrization?

    ih_os   = 5
    ih_arch = 2
    ih_type = 6
    ih_comp = 0

    name = "name"       # placeholder for now   #TODO: where should i get name?

    name = name_to_32bit(name)

    header_without_crc = struct.pack('>IIIIIIIBBBB32s',
                                     magic_number,
                                     empty_word,
                                     epoch_time,
                                     body_len,
                                     0,
                                     0,
                                     body_crc,
                                     ih_os,
                                     ih_arch,
                                     ih_type,
                                     ih_comp,
                                     name
                                     )

    empty_body_crc = calculator.checksum(header_without_crc)

    header_crc = struct.pack('>IIIIIIIBBBB32s',
                                     magic_number,
                                     empty_body_crc,
                                     epoch_time,
                                     body_len,
                                     0,
                                     0,
                                     body_crc,
                                     ih_os,
                                     ih_arch,
                                     ih_type,
                                     ih_comp,
                                     name
                                     )

    with open("test.txt", "wb") as f:
        f.write(header_crc + body)

if __name__ == "__main__":
    yaml_file = sys.argv[1]
    main(yaml_file)