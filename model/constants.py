import numpy as np

PHENOMENON_FIELD_MAP = {
    'Ливень (ливни).': 0,
    'Дождь.': 1,
    'Снег или дождь со снегом.': 2,
    'Морось.': 3,
    'Песчаная или пыльная буря или снежная низовая метель.': 4,
    'Гроза (грозы) с осадками или без них.': 5,
    np.nan: np.nan
}

SEDGES_FIELD_MAP = {
    'Осадков нет': 0,
    'Следы осадков': 0
}
