
from typing import List


class DomaingTranslatorWrapper:
    def __init__(self, wrapped):
        self.wrapped = wrapped

        self.trans_dict = {
            'RoomA' : 'IC Room 1',
            'Kitchen' : 'Respiratory Control',
            'navto': 'navigation',
            # 'wait': 'approach_person',
            'approach': 'approach_object',
            'load': 'deposit',
            'pick': 'pick_up',
            'open': 'manipulate_door',
            'retrieve': 'pick_up'
        }

    def get(self, label: str, *domain_qualifiers: List[str], context: str =None):
        if self.trans_dict.get(label):
            label = self.trans_dict[label]
        return self.wrapped.get(label, *domain_qualifiers)
