import random
import string


BAD_VALUES = {
    0x432, 0x4B1, 0x518, 0x1648, 0x1666, 0x175E, 0x19F6,
    0x5490, 0x55E3, 0x56E6, 0x5787, 0x5815, 0x592C, 0x5AC2,
    0x5B37, 0x5B72, 0x5CD7, 0x5EDC, 0x5FEA, 0x62B6, 0x630D,
    0x647B, 0x651B, 0x653E, 0x6595, 0x6E2A, 0x7DB8, 0x83A6,
    0x85A7, 0x8880, 0x8BE4, 0x8CB5, 0x8DAF, 0x91A9, 0x95A3,
    0x95F8, 0x99A7, 0x9AB8, 0xA0A7, 0xA0F8, 0xA128, 0xA2E7,
    0xA5D9, 0xA680, 0xA80C, 0xA870, 0xA8FC, 0xAB42, 0xAC39,
    0xAC44, 0xACC7, 0xAD73, 0xAEA8, 0xB59D, 0xB8C2, 0xB956,
    0xBB41, 0xBD16, 0xBD20, 0xBD26, 0xBE90, 0xC100, 0xC2F3,
    0xC75D, 0xC87E, 0xC935, 0xCB9C, 0xD1CB, 0xD75F, 0xDCCE,
    0xE70F, 0xECCF, 0xEF12, 0xF194, 0xF323, 0xF32C, 0xF5D2,
    0xFB6E, 0x122CE, 0x12920, 0x12B54, 0x12F4B, 0x12F9E,
    0x132CD, 0x13B91, 0x13D63, 0x145A5, 0x15514, 0x15A44,
    0x15B4F, 0x15CBE, 0x15E6C,
}


def blacklist_value(s: str) -> int:
    c = lambda i: ord(s[i])

    esi = c(2) + 10 * c(13) - 738 + (c(9) - ord("B")) * 1000
    ecx = (c(8) * 100 + c(11)) * 5 - 0x8835
    ecx = c(20) + ecx * 2
    esi += ecx * 10

    edx = c(3) + c(4) * 0x1F40 + c(1)
    if esi != edx:
        esi = 0

    esi += c(6) - ord("F")
    esi += (c(17) - ord("C")) * 100
    return esi + 10 * (c(2) - 0x12027 + 100 * (c(11) * 10 + c(10)))


def is_valid(s: str) -> bool:
    if len(s) != 24:
        return False
    if s[0] not in "ST":
        return False
    if any(i in (4, 9, 14, 19) and s[i] != "-" for i in range(24)):
        return False

    c = lambda i: ord(s[i])
    if (c(5) + c(6) + c(7) + c(8) + c(10) + c(11)) % 11 != c(3) - ord("B"):
        return False
    if (c(15) + c(18) + c(20)) % 19 + ord("A") != c(21):
        return False
    if (c(11) + c(10) + c(2) + c(8)) % 18 + ord("B") != c(22):
        return False
    if not ("C" <= s[2] <= "L" and "F" <= s[6] <= "O" and "C" <= s[10] <= "L"):
        return False
    if not ("B" <= s[11] <= "K" and "C" <= s[17] <= "L"):
        return False

    total = sum(ord(ch) - ord("A") for ch in s[:23])
    if total % 21 != c(23) - ord("D"):
        return False

    return blacklist_value(s) not in BAD_VALUES


def generate() -> str:
    letters = string.ascii_uppercase
    while True:
        chars = list("SAAA-AAAA-AAAA-AAAA-AAAA")
        chars[0] = random.choice("ST")

        fixed = {0, 3, 4, 9, 14, 19, 21, 22, 23}
        for i in range(24):
            if i not in fixed:
                pools = {
                    2: "CDEFGHIJKL",
                    6: "FGHIJKLMNO",
                    10: "CDEFGHIJKL",
                    11: "BCDEFGHIJK",
                    17: "CDEFGHIJKL",
                }
                chars[i] = random.choice(pools.get(i, letters))

        chars[3] = chr(ord("B") + (sum(ord(chars[i]) for i in (5, 6, 7, 8, 10, 11)) % 11))
        chars[21] = chr(ord("A") + (sum(ord(chars[i]) for i in (15, 18, 20)) % 19))
        chars[22] = chr(ord("B") + (sum(ord(chars[i]) for i in (11, 10, 2, 8)) % 18))
        chars[23] = chr(ord("D") + (sum(ord(ch) - ord("A") for ch in chars[:23]) % 21))

        serial = "".join(chars)
        if is_valid(serial):
            return serial


if __name__ == "__main__":
    for _ in range(10):
        print(generate())
