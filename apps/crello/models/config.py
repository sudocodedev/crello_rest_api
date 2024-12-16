from djchoices import ChoiceItem, DjangoChoices

class PriorityType(DjangoChoices):
    low = ChoiceItem('low', 'Low')
    lowest = ChoiceItem('lowest', 'Lowest')
    medium = ChoiceItem('medium', 'Medium')
    high = ChoiceItem('high', 'High')
    critical = ChoiceItem('critical', 'Critical')

PRIORITY = ['low', 'lowest', 'medium', 'high', 'critical',]

# image extensions & size supported by the app
ACCEPTABLE_IMAGE_EXTENSIONS = ['png', 'jpg', 'jpeg']
ACCEPTABLE_IMAGE_MAX_MEMORY_SIZE = 5242880 #5MB

# file extensions supported by the app
ACCEPTABLE_FILE_EXTENSIONS = ['pdf', 'docx', 'doc', 'xlsx', 'md', 'pptx']