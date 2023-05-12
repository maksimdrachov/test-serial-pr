from pycyphal.transport import MessageDataSpecifier
from pycyphal.transport import Priority
from pycyphal.transport.serial import SerialFrame

f = SerialFrame(
    priority=Priority.NOMINAL,
    transfer_id=0,
    index=0,  # Transmit zero. Drop frame if received non-zero.
    end_of_transfer=True,  # Transmit true. Drop frame if received false.
    payload=memoryview(b"012345678"),
    source_node_id=1234,
    destination_node_id=None,
    data_specifier=MessageDataSpecifier(1234),
    user_data=0,
)

buffer = bytearray(0 for _ in range(1000))
mv = f.compile_into(buffer)

print("mv: ", mv.tobytes())
print("len(mv): ", len(mv.tobytes()))  # in spec it has 42 bytes, but here it is 36

# starting delimiter
print("mv[0]: ", mv[0].to_bytes(1, byteorder="big"))

# COBS overhead byte
print("mv[1]: ", mv[1].to_bytes(1, byteorder="big"))

# 24 bytes of COBS encoded header
print("mv[2:26]: ", mv[2:26].tobytes())

# 11 bytes of COBS encoded payload (2 + 9)
print("mv[26:37]: ", mv[26:37].tobytes())

# 4 bytes COBS encoded transfer-CRC
print("mv[37:41]: ", mv[37:41].tobytes())

# 1 byte delimiter ending the frame
print("mv[41]: ", mv[41].to_bytes(1, byteorder="big"))
