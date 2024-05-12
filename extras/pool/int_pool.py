from ._mixins import BitPoolMixin as _BitPoolMixin
from .abc import BitPoolABC
import typing as ty


class IntBitPool(_BitPoolMixin, BitPoolABC):
    def __init__(self, size: int | ty.SupportsInt) -> None:
        size = int(size)
        assert size > 0, "Size must be greater than zero, got %r" % size
        self._size = size
        self._pool = 0

    @property
    def used(self) -> int:
        return self._pool.bit_count()

    def _write_1(self, index: int):
        self._pool |= 1 << index

    def _write_0(self, index: int):
        self._pool ^= self._pool & 1 << index

    def _write(self, index: int, value: bool):
        (self._write_1 if value else self._write_0)(index)

    def _read(self, index: int) -> bool:
        return bool(self._pool >> index & 1)

    def _flip(self, index: int) -> bool:
        new_value = not self._read(index)
        self._write(index, new_value)
        return new_value

    def _to_str(self) -> str:
        return self._pool.to_bytes(self._size // 8 + 1).hex()

    def write_bits(self, indices: ty.Iterable[tuple[int, bool]]):
        for index, value in indices:
            index = self._valid_index(index)
            self._write(index, value)

    def read_bits(self, indices: ty.Iterable[int]) -> ty.Iterator[bool]:
        "This is lazy, expand to get instant bit values."
        valid_indices = map(self._valid_index, indices)
        return map(self._read, valid_indices)

    def flip_bits(self, indices: ty.Iterable[int]) -> list[bool]:
        valid_indices = map(self._valid_index, indices)
        return [self._flip(index) for index in valid_indices]

    def flip_bit(self, index: int) -> bool:
        return self._flip(self._valid_index(index))

    def read_bit(self, index: int) -> bool:
        return self._read(self._valid_index(index))

    def write_bit(self, index: int, value: bool):
        self._write(self._valid_index(index), value)
