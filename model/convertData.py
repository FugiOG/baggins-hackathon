from constants import PHENOMENON_FIELD_MAP
import pandas as pd


class ConvertDataService:
    @staticmethod
    def convertPhenomenonColumn(phenomenonColumn):
        return [PHENOMENON_FIELD_MAP[phenomenon] for phenomenon in phenomenonColumn]

    @staticmethod
    def convertDateColumn(dateColumn):
        return pd.to_datetime(dateColumn)


convertDataService = ConvertDataService()
