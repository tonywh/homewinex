class Solid:
    KG = 0
    G = 1
    LB = 2
    OZ = 3
    UNITS = (
        (KG, 'kg'),
        (G, 'g'),
        (LB, 'lb'),
        (OZ, 'oz'),
    )
    CONV = [1.0, 1000.0, 2.2046226, 35.273961]
    STEP = [0.005, 5.0, 0.0125, 0.2]
    DECIMALS = [3, 0, 4, 1]

    def __init__(self, val, unit=KG):
        self.val = Val
        self.unit = unit

    def get(unit=KG):
        return self.val * CONV[unit] / CONV[self.unit]

class Liquid:
    L = 0
    ML = 1
    USGAL = 2
    IMPGAL = 3
    USFLOZ = 4
    IMPFLOZ = 5
    UNITS = (
        (L, 'L'),
        (ML, 'ml'),
        (USGAL, 'gal-US'),
        (IMPGAL, 'gal-Imp'),
        (USFLOZ, 'floz-US'),
        (IMPFLOZ, 'floz-Imp'),
    )
    CONV = [1.0, 1000.0, 0.26417205, 0.21996925, 33.814023, 35.195079]
    STEP = [0.005, 5.0, 0.0015625, 0.00125, 0.2, 0.2]
    DECIMALS = [3, 0, 4, 4, 1, 1]

    def __init__(self, val, unit=L):
        self.val = Val
        self.unit = unit

    def get(unit=L):
        return self.val * CONV[unit] / CONV[self.unit]
