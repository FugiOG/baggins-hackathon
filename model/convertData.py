from constants import PHENOMENON_FIELD_MAP
from constants import SEDGES_FIELD_MAP
import pandas as pd


class ConvertDataService:
    @staticmethod
    def convertPhenomenonColumn(phenomenonColumn):
        return [PHENOMENON_FIELD_MAP[phenomenon] for phenomenon in phenomenonColumn]

    @staticmethod
    def convertDateColumn(dateColumn):
        return pd.to_datetime(dateColumn)

    @staticmethod
    def convertSedgesColumn(sedgesColumn):
        result = []
        for sedge in sedgesColumn:
            validSedge = sedge

            if isinstance(sedge, str):
                validSedge = SEDGES_FIELD_MAP[sedge]

            result.append(validSedge)

        return result


convertDataService = ConvertDataService()