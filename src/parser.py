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
    chat_date_pattern = re.compile(r"\d{4}년 \d{1,2}월 \d{1,2}일 .요일")
    chat_pattern = re.compile(r"\[(.*?)\] \[(오전|오후) (\d{1,2}:\d{1,2})\]")
    system_message_pattern = re.compile(r".+님이 들어왔습니다\.|.+님이 나갔습니다\.")

    current_date = None
    current_speaker = None
    current_time = None
    current_message = []

    chats = []
    current_date = None

    # Iterate through the content and extract chats
    for line in content:
        # Check if the line has the date format
        date_match = re.search(r"\d{4}년 \d{1,2}월 \d{1,2}일", line)
        if date_match:
            date_str = date_match.group()
            current_date = datetime.strptime(date_str, "%Y년 %m월 %d일").date()
            continue

        # Check for system messages and skip them
        if "님이 들어왔습니다." in line or "님이 나갔습니다." in line:
            continue

        # Extract chat messages
        chat_match = re.search(r"\[(.*?)\] \[(.*?)\] (.*)", line)
        if chat_match:
            speaker, _, message = chat_match.groups()
            chats.append(Chat(current_date, speaker, message))
        else:
            # If the current line is not a new chat, it's a continuation of the previous message
            if chats:
                chats[-1].message += "\n" + line.strip()

    return chats
