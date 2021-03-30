

def read_contacts():
    with open("./data/contacts.txt", "r") as f:
        answer = ""
        lines = f.readlines()
        for line in lines:
            answer += line
        return answer


def read_delivery():
    with open("./data/delivery.txt", "r") as f:
        answer = ""
        lines = f.readlines()
        for line in lines:
            answer += line
        return answer


def write_contacts(text):
    with open("./data/contacts.txt", "w") as f:
        f.write(text)


def write_delivery(text):
    with open("./data/delivery.txt", "w") as f:
        f.write(text)