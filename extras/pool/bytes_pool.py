from ._mixins import BitPoolMixin as _BitPoolMixin
from .abc import BitPoolABC
import typing as ty


class BytesBitPool(_BitPoolMixin, BitPoolABC):
    def __init__(self, size: int) -> None:
        assert size > 0, "Size must be greater than zero, got %r" % size
        self._size = size
        slots = size // 8 + 1
        self._pool = bytearray(b"\0" * slots)

    @property
    def used(self) -> int:
        return sum(b.bit_count() for b in self._pool)

    def _idx2pos(self, index: int) -> tuple[int, int]:
        return divmod(index, 8)

    def _write_1(self, slot: int, offset: int):
        self._pool[slot] |= 1 << offset

    def _write_0(self, slot: int, offset: int):
        self._pool[slot] ^= self._pool[slot] & 1 << offset

    def _write(self, slot: int, offset: int, value: bool):
        (self._write_1 if value else self._write_0)(slot, offset)

    def _read(self, slot: int, offset: int) -> bool:
        return bool(self._pool[slot] >> offset & 1)

    def _flip(self, slot: int, offset: int):
        new_value = not self._read(slot, offset)
        self._write(slot, offset, new_value)
        return new_value

    def _to_str(self) -> str:
        return self._pool.hex()

    def flip_bit(self, index: int) -> bool:
        slot, offset = self._idx2pos(self._valid_index(index))
        return self._flip(slot, offset)

    def flip_bits(self, indices: ty.Iterable[int]) -> list[bool]:
        valid_indices = map(self._valid_index, indices)
        slot_offsets = map(self._idx2pos, valid_indices)
        return [self._flip(slot, offset) for slot, offset in slot_offsets]

    def write_bit(self, index: int, value: bool):
        slot, offset = self._idx2pos(self._valid_index(index))
        self._write(slot, offset, value)

    def write_bits(self, indices: ty.Iterable[tuple[int, bool]]):
        for index, value in indices:
            index = self._valid_index(index)
            slot, offset = self._idx2pos(index)
            self._write(slot, offset, value)

    def read_bit(self, index: int) -> bool:
        slot, offset = self._idx2pos(self._valid_index(index))
        return self._read(slot, offset)

    def read_bits(self, indices: ty.Iterable[int]) -> ty.Iterator[bool]:
        "Expand to get instant bit values. Lazy by default."
        valid_indices = map(self._valid_index, indices)
        slot_offsets = map(self._idx2pos, valid_indices)
        return (self._read(slot, offset) for slot, offset in slot_offsets)
