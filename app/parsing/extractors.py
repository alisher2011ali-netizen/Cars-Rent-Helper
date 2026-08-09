"""
This module lists all extractor calsses available
It shall be edited with every new extractor class created
"""

from app.parsing.extractor import Extractor

extractors_list: list[type] = []

from .extractors_list.extractor_SBER_DEBIT_2107 import SBER_DEBIT_2107

extractors_list.append(SBER_DEBIT_2107)

from .extractors_list.extractor_SBER_DEBIT_2005 import SBER_DEBIT_2005

extractors_list.append(SBER_DEBIT_2005)

from .extractors_list.extractor_SBER_CREDIT_2110 import SBER_CREDIT_2110

extractors_list.append(SBER_CREDIT_2110)

from .extractors_list.extractor_SBER_PAYMENT_2407 import SBER_PAYMENT_2407

extractors_list.append(SBER_PAYMENT_2407)

from .extractors_list.extractor_SBER_PAYMENT_2406 import SBER_PAYMENT_2406

extractors_list.append(SBER_PAYMENT_2406)

from .extractors_list.extractor_SBER_PAYMENT_2212 import SBER_PAYMENT_2212

extractors_list.append(SBER_PAYMENT_2212)

from .extractors_list.extractor_SBER_PAYMENT_2208 import SBER_PAYMENT_2208

extractors_list.append(SBER_PAYMENT_2208)

from .extractors_list.extractor_SBER_DEBIT_2212 import SBER_DEBIT_2212

extractors_list.append(SBER_DEBIT_2212)

from .extractors_list.extractor_SBER_DEBIT_2408 import SBER_DEBIT_2408

extractors_list.append(SBER_DEBIT_2408)

from .extractors_list.extractor_SBER_SAVING_2303 import SBER_SAVING_2303

extractors_list.append(SBER_SAVING_2303)

from .extractors_list.extractor_SBER_SAVING_2407 import SBER_SAVING_2407

extractors_list.append(SBER_SAVING_2407)

from .extractors_list.extractor_SBER_DEBIT_2303_CHELYABINSK import (
    SBER_DEBIT_2303_CHELYABINSK,
)

extractors_list.append(SBER_DEBIT_2303_CHELYABINSK)

from .extractors_list.extractor_SBER_CREDIT_2409 import SBER_CREDIT_2409

extractors_list.append(SBER_CREDIT_2409)

from .extractors_list.extractor_SBER_DEBIT_2510 import SBER_DEBIT_2510

extractors_list.append(SBER_DEBIT_2510)

from .extractors_list.extractor_SBER_PAYMENT_2510 import SBER_PAYMENT_2510

extractors_list.append(SBER_PAYMENT_2510)

from .extractors_list.extractor_SBER_CREDIT_2511 import SBER_CREDIT_2511

extractors_list.append(SBER_CREDIT_2511)

from .extractors_list.extractor_SBER_DEBIT_2603 import SBER_DEBIT_2603

extractors_list.append(SBER_DEBIT_2603)

from .extractors_list.extractor_SBER_PAYMENT_2604 import SBER_PAYMENT_2604

extractors_list.append(SBER_PAYMENT_2604)

from .extractors_list.extractor_SBER_SAVING_2604 import SBER_SAVING_2604

extractors_list.append(SBER_SAVING_2604)

from .extractors_list.extractor_SBER_PAYMENT_DEBIT_2604b import SBER_PAYMENT_DEBIT_2604b

extractors_list.append(SBER_PAYMENT_DEBIT_2604b)

from .extractors_list.extractor_SBER_CREDIT_2605 import SBER_CREDIT_2605

extractors_list.append(SBER_CREDIT_2605)


def get_list_extractors_in_text():
    return [extractor.__name__ for extractor in extractors_list]
