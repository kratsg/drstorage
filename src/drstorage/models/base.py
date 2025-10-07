from __future__ import annotations

from construct import (
    Bytes,
    Checksum,
    Computed,
    Const,
    Int16ub,
    OneOf,
    Padding,
    RawCopy,
    Struct,
    Terminated,
)


def DrStorageFactory(model_number=None):
    model = Const(model_number) if model_number else Bytes(2)
    thestruct = Struct(
        "_fields"
        / RawCopy(
            Struct(
                Const(b"\xab\xab"),
                "raw_humidity" / Int16ub,
                OneOf(Bytes(1), [b"\x12", b"\x10"]),
                "raw_temperature" / Int16ub,
                Const(b"\x12"),
                "raw_humidity_precise" / Int16ub,
                Padding(7),
                Const(b"\x0a"),
                Const(b"\x10"),
                "model" / model,
                Const(b"\x10"),
                Padding(6),
            )
        ),
        "humidity" / Computed(lambda ctx: ctx._fields.value.raw_humidity / 10.0),
        "temperature" / Computed(lambda ctx: ctx._fields.value.raw_temperature / 10.0),
        "model" / Computed(lambda ctx: int.from_bytes(ctx._fields.value.model, "big")),
        Checksum(
            Bytes(1),
            lambda data: bytes([sum(data) % 256]),
            lambda ctx: ctx._fields.data,
        ),
        Const(b"\x0d\x0a"),
        Terminated,
    )
    thestruct.size = 31
    return thestruct


generic = DrStorageFactory()
