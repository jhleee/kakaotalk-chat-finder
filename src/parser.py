import re
from datetime import datetime

# Define the chat structure
class Chat:
    def __init__(self, date, speaker, message):
        self.date = date
        self.speaker = speaker
        self.message = message

    def __repr__(self):
        return f"{self.date} - {self.speaker}: {self.message}"

    __str__ = __repr__

def parse(filename, max_line=None):
    with open(filename, "r", encoding="utf-8") as f:
        content = f.readlines()
        return parse_text(content[:(max_line or -1)])

# Extract chats from the given content
def parse_text(content):
    chats = []
    current_date = None

    # Define regex patterns
    date_pattern = re.compile(r"--------------- (\d{4}년 \d{1,2}월 \d{1,2}일) .+? ---------------")
    chat_pattern = re.compile(r"\[(.+?)\] \[\w+? (\d{1,2}:\d{1,2})\] (.+)")

    for line in content:
        date_match = date_pattern.match(line)
        chat_match = chat_pattern.match(line)

        if date_match:  # Update the current date if a date line is found
            date_str = date_match[1]
            current_date = datetime.strptime(date_str, "%Y년 %m월 %d일").date()
        elif chat_match and current_date:  # Extract chat details if a chat line is found
            speaker = chat_match[1]
            time_str = chat_match[2]
            message = chat_match[3]
            chats.append(Chat(current_date, speaker, message))

    return chats
