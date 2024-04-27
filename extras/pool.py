import typing as ty


class BitPool(ty.Protocol):
    def flip_bit(self, index: int) -> bool: ...
    def read_bit(self, index: int) -> bool: ...
    def write_bit(self, index: int, value: bool): ...
    def flip_bits(self, indices: ty.Iterable[int]) -> ty.Iterable[bool]: ...
    def read_bits(self, indices: ty.Iterable[int]) -> ty.Iterable[bool]: ...
    def write_bits(self, indices: ty.Iterable[tuple[int, bool]]): ...
    @property
    def used(self) -> int: ...
    @property
    def size(self) -> int: ...
    def __len__(self) -> int: ...


class _BitPoolMixin:
    _size: int
    used: property

    def _to_str(self) -> str:
        name = self.__class__.__name__
        raise NotImplementedError("%s did not implement %s._to_str()" % (name, name))

    @property
    def size(self) -> int:
        return self._size

    def __len__(self) -> int:
        return self._size

    def _valid_index(self, index: int) -> int:
        if abs(index) >= self._size:
            msg = "Out of range (-%r,%r), got %r"
            raise IndexError(msg % (self._size, self._size, index))
        return index % self._size

    def __str__(self):
        name = self.__class__.__name__
        capacity = self.used / self._size * 100
        return f"{name}(used={self.used}, size={self._size}, {capacity=:.1f}%)"

    def __repr__(self) -> str:
        name = self.__class__.__name__
        capcity = self.used / self._size * 100
        value = self._to_str()
        if len(value) > 13:
            value = f"{value[:5]}...{value[-5:]}"
        return (
            f"<{name}(used={self.used} size={self._size} {capcity=:.3f}% {value=!r})>"
        )


class IntegerBitPool(_BitPoolMixin, BitPool):
    def __init__(self, size: int) -> None:
        assert size > 0, "Size must be greater than zero, got %r" % size
        self._size = size
        self._pool = 0

    @property
    def used(self) -> int:
        return self._pool.bit_count()

    def _write_1(self, index: int):
        self._pool |= 1 << index

    def _write_0(self, index: int):
        self._pool ^= self._pool & (1 << index)

    def _write(self, index: int, value: bool):
        (self._write_1 if value else self._write_0)(index)

    def _read(self, index: int) -> bool:
        return bool((self._pool >> index) & 1)

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

    def read_bits(self, indices: ty.Iterable[int]) -> ty.Iterable[bool]:
        valid_indices = map(self._valid_index, indices)
        return (self._read(index) for index in valid_indices)

    def flip_bits(self, indices: ty.Iterable[int]) -> ty.Iterable[bool]:
        valid_indices = map(self._valid_index, indices)
        return [self._flip(index) for index in valid_indices]

    def flip_bit(self, index: int) -> bool:
        return self._flip(self._valid_index(index))

    def read_bit(self, index: int) -> bool:
        return self._read(self._valid_index(index))

    def write_bit(self, index: int, value: bool):
        self._write(self._valid_index(index), value)


class BytesBitPool(_BitPoolMixin, BitPool):
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
        self._pool[slot] ^= self._pool[slot] & (1 << offset)

    def _write(self, slot: int, offset: int, value: bool):
        (self._write_1 if value else self._write_0)(slot, offset)

    def _read(self, slot: int, offset: int):
        return bool((self._pool[slot] >> offset) & 1)

    def _flip(self, slot: int, offset: int):
        new_value = not self._read(slot, offset)
        self._write(slot, offset, new_value)
        return new_value

    def _to_str(self) -> str:
        return self._pool.hex()

    def write_bits(self, indices: ty.Iterable[tuple[int, bool]]):
        for index, value in indices:
            index = self._valid_index(index)
            slot, offset = self._idx2pos(index)
            self._write(slot, offset, value)

    def read_bits(self, indices: ty.Iterable[int]) -> ty.Iterable[bool]:
        valid_indices = map(self._valid_index, indices)
        slot_offsets = map(self._idx2pos, valid_indices)
        return (self._read(slot, offset) for slot, offset in slot_offsets)

    def flip_bits(self, indices: ty.Iterable[int]) -> ty.Iterable[bool]:
        valid_indices = map(self._valid_index, indices)
        slot_offsets = map(self._idx2pos, valid_indices)
        return [self._flip(slot, offset) for slot, offset in slot_offsets]

    def flip_bit(self, index: int) -> bool:
        slot, offset = self._idx2pos(self._valid_index(index))
        return self._flip(slot, offset)

    def write_bit(self, index: int, value: bool):
        slot, offset = self._idx2pos(self._valid_index(index))
        self._write(slot, offset, value)

    def read_bit(self, index: int) -> bool:
        slot, offset = self._idx2pos(self._valid_index(index))
        return self._read(slot, offset)
