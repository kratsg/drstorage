from construct import (
    Struct,
    RawCopy,
    Bytes,
    Const,
    Int16ub,
    Padding,
    Computed,
    Checksum,
    Terminated,
)

F1_600 = Struct(
    "_fields"
    / RawCopy(
        Struct(
            Const(b"\xab\xab"),
            "raw_humidity" / Int16ub,
            Const(b"\x12"),
            "raw_temperature" / Int16ub,
            Const(b"\x12"),
            "raw_humidity_precise" / Int16ub,
            Padding(7),
            Const(b"\x0a"),
            Const(b"\x10\x02"),
            Const(b"\x58\x10"),
            Padding(6),
        )
    ),
    "humidity" / Computed(lambda ctx: ctx._fields.value.raw_humidity / 10.0),
    "temperature" / Computed(lambda ctx: ctx._fields.value.raw_temperature / 10.0),
    Checksum(
        Bytes(1), lambda data: bytes([sum(data) % 256]), lambda ctx: ctx._fields.data
    ),
    Const(b"\x0d\x0a"),
    Terminated,
)
