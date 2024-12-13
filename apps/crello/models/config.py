from djchoices import ChoiceItem, DjangoChoices

class PriorityType(DjangoChoices):
    low = ChoiceItem('low', 'Low')
    lowest = ChoiceItem('lowest', 'Lowest')
    medium = ChoiceItem('medium', 'Medium')
    high = ChoiceItem('high', 'High')
    critical = ChoiceItem('critical', 'Critical')
