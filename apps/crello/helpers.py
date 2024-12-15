from apps.crello.models import Card


def check_instance(email:str) -> bool:
    cards = Card.objects.filter(assignee__email=email, is_deleted=False)
    return False if len(cards) == 0 else True

def get_data(email:str) -> dict:
    cards = Card.objects.filter(assignee__email=email, is_deleted=False)

    data = {}

    for card in cards:
        list_name = card.card_list.name
        board_name = card.card_list.board.name

        if board_name not in data:
            data[board_name] = {}
        if list_name not in data[board_name]:
            data[board_name][list_name] = []
        
        data[board_name][list_name].append(card)

    return data

def get_message(data:dict) -> str:
    message = ""

    for board, lists in data.items():
        message += f"Board: {board}\n\n"
        for list_name, cards in lists.items():
            message += f"  List: {list_name}\n"
            
            for card in cards:
                message += f"   - {card.name} | (Priority: {card.priority} | Due Date: {card.due_date})\n"

    return message


