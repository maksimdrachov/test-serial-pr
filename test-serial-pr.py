import typing
from pycyphal.transport import InputSessionSpecifier, MessageDataSpecifier, Priority
from pycyphal.transport.serial import SerialFrame

prio = Priority.NOMINAL
dst_nid = 1  # TODO: Not specified in doc?

# Transfer kind: message with the subject ID 1234
session_spec = InputSessionSpecifier(MessageDataSpecifier(1234), None)


def mk_frame(
    transfer_id: int,
    index: int,
    end_of_transfer: bool,
    payload: typing.Union[bytes, memoryview],
    source_node_id: typing.Optional[int],
) -> SerialFrame:
    return SerialFrame(
        priority=prio,
        transfer_id=transfer_id,
        index=index,
        end_of_transfer=end_of_transfer,
        payload=memoryview(payload),
        source_node_id=source_node_id,
        destination_node_id=dst_nid,
        data_specifier=session_spec.data_specifier,
        user_data=0,
    )


## Fist example

serial_frame = mk_frame(
    transfer_id=0,  # Transfer ID 0
    index=0,  # Transmit zero. Drop frame if received non-zero.
    end_of_transfer=True,  # Transmit True. Drop frame if received False.
    payload=b"012345678",  # Transfer payload containing string "012345678"
    source_node_id=1234,  # Source node ID 1234
)

print("serial_frame: ", serial_frame)

out_buffer: bytearray = bytearray(1024)
memoryview_output = serial_frame.compile_into(out_buffer=out_buffer)

print("memoryview_output: ", memoryview_output.tobytes())

memoryview_bytes = memoryview_output.tobytes()

print(
    "(starting delimiter) memoryview_bytes[0]: ", memoryview_bytes[0].to_bytes(1, "big")
)
print(
    "(COBS overhead byte) memoryview_bytes[1]: ", memoryview_bytes[1].to_bytes(1, "big")
)
print("(header) memoryview_bytes[2:2+24]: ")
for single_byte in memoryview_bytes[2 : 2 + 24]:
    print(single_byte.to_bytes(1, "big"))
print("(payload) memoryview_bytes[27:27+11]: ")
for single_byte in memoryview_bytes[27 : 27 + 11]:
    print(single_byte.to_bytes(1, "big"))
print("COBS-encoded transfer-CRC", memoryview_bytes[39 : 39 + 4])
for single_byte in memoryview_bytes[39 : 39 + 4]:
    print(single_byte.to_bytes(1, "big"))
print(
    "(ending delimiter) memoryview_bytes[44]: ", memoryview_bytes[44].to_bytes(1, "big")
)
