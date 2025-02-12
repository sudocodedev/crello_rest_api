from djchoices import ChoiceItem, DjangoChoices


class PriorityChoices(DjangoChoices):
    """Choices for Priority type."""

    lowest = ChoiceItem("lowest", "Lowest")
    low = ChoiceItem("low", "Low")
    medium = ChoiceItem("medium", "Medium")
    high = ChoiceItem("high", "High")
    critical = ChoiceItem("critical", "Critical")
