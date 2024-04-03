from typing import List, Tuple
import datetime

def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]:
    print("Ejecutando q1_time con file_path:", file_path)
    dummy_data = [
        (datetime.date(2022, 1, 1), 'Registro 1'),
        (datetime.date(2022, 1, 2), 'Registro 2')
    ]

    return dummy_data