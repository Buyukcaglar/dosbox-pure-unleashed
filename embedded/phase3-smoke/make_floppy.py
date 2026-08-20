from pathlib import Path
import struct


BYTES_PER_SECTOR = 512
TOTAL_SECTORS = 2880
SECTORS_PER_FAT = 9
ROOT_ENTRIES = 224
ROOT_SECTORS = 14
FAT_COUNT = 2
FIRST_DATA_SECTOR = 1 + FAT_COUNT * SECTORS_PER_FAT + ROOT_SECTORS


def set_fat12_entry(fat: bytearray, cluster: int, value: int) -> None:
    offset = cluster + cluster // 2
    if cluster & 1:
        fat[offset] = (fat[offset] & 0x0F) | ((value << 4) & 0xF0)
        fat[offset + 1] = (value >> 4) & 0xFF
    else:
        fat[offset] = value & 0xFF
        fat[offset + 1] = (fat[offset + 1] & 0xF0) | ((value >> 8) & 0x0F)


def main() -> None:
    fixture_dir = Path(__file__).resolve().parent
    payload = (fixture_dir / "IMAGE.OK").read_text(encoding="ascii").strip().encode("ascii") + b"\r\n"
    image = bytearray(BYTES_PER_SECTOR * TOTAL_SECTORS)

    image[0:3] = b"\xEB\x3C\x90"
    image[3:11] = b"MSDOS5.0"
    struct.pack_into(
        "<HBHBHHBHHHII",
        image,
        11,
        BYTES_PER_SECTOR,
        1,
        1,
        FAT_COUNT,
        ROOT_ENTRIES,
        TOTAL_SECTORS,
        0xF0,
        SECTORS_PER_FAT,
        18,
        2,
        0,
        0,
    )
    image[36] = 0
    image[37] = 0
    image[38] = 0x29
    struct.pack_into("<I", image, 39, 0x20260820)
    image[43:54] = b"DBPTEST    "
    image[54:62] = b"FAT12   "
    image[510:512] = b"\x55\xAA"

    fat = bytearray(BYTES_PER_SECTOR * SECTORS_PER_FAT)
    fat[0:3] = b"\xF0\xFF\xFF"
    set_fat12_entry(fat, 2, 0xFFF)
    first_fat = BYTES_PER_SECTOR
    image[first_fat:first_fat + len(fat)] = fat
    second_fat = first_fat + len(fat)
    image[second_fat:second_fat + len(fat)] = fat

    root_offset = (1 + FAT_COUNT * SECTORS_PER_FAT) * BYTES_PER_SECTOR
    image[root_offset:root_offset + 11] = b"IMAGE   OK "
    image[root_offset + 11] = 0x20
    fat_date = ((2026 - 1980) << 9) | (8 << 5) | 20
    struct.pack_into("<HHH", image, root_offset + 14, 0, fat_date, fat_date)
    struct.pack_into("<HHHHI", image, root_offset + 20, 0, 0, fat_date, 2, len(payload))

    data_offset = FIRST_DATA_SECTOR * BYTES_PER_SECTOR
    image[data_offset:data_offset + len(payload)] = payload
    (fixture_dir / "DISK.IMA").write_bytes(image)


if __name__ == "__main__":
    main()
