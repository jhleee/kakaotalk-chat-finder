import re
from .parser import Chat
from datetime import datetime
from collections import defaultdict
from typing import List, Optional, Dict, Tuple

def statistics(chats: Optional[List[Chat]],
                start_date: Optional[str] = None,
                end_date: Optional[str] = None,
                speaker: Optional[str] = None,
                verbose = False,
                message_contains: Optional[List[str]] = None) -> Dict[str, Dict]:

    # Use the search function to filter the chats based on given criteria
    filtered_chats = search(chats, start_date, end_date, speaker, message_contains, verbose=verbose)
    # Initialize dictionaries for the statistics
    speaker_counts = defaultdict(int)
    date_counts = defaultdict(int)
    # hour_counts = defaultdict(int)

    for chat in filtered_chats:
        # Count messages by speaker
        speaker_counts[chat.speaker] += 1

        # Count messages by date
        date_counts[chat.date] += 1

        # Count messages by hour (using regex to extract time)
        # time_match = re.search(r"\[(\d{1,2}:\d{1,2})\]", chat.message)
        # if time_match:
        #     hour = datetime.strptime(time_match.group(1), "%H:%M").hour
        #     hour_counts[hour] += 1

    # Sort the statistics
    speaker_counts_sorted = dict(sorted(speaker_counts.items(), key=lambda item: item[1], reverse=True))
    date_counts_sorted = dict(sorted(date_counts.items()))
    # hour_counts_sorted = dict(sorted(hour_counts.items()))

    # Compile the results
    stats = {
        "speakers": len(speaker_counts),
        "message_by_speaker": speaker_counts_sorted,
        "message_by_date": date_counts_sorted
    }

    return stats


def search(chats: Optional[List[Chat]],
            start_date: Optional[str] = None,
            end_date: Optional[str] = None,
            speaker: Optional[str] = None,
            message_contains: Optional[str] = None,
            max_line: Optional[int] = None,
            verbose: bool = False) -> List[Chat]:
    if type(message_contains) == "str":
        message_contains = [message_contains]
    if verbose:
        print(f" - Chat data length: {len(chats)}")
        start_date and print(f" - Start date: {start_date}")
        end_date and print(f" - End date: {end_date}")
        speaker and print(f" - Speaker: {speaker}")
        message_contains and print(f" - Message contains: {', '.join(message_contains)}")

    # Convert string dates to datetime.date objects if provided
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date() if start_date else None
    end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date() if end_date else None

    if verbose:
        stime = datetime.now()
        print(" * Searching ...")
    # Filter the indexed chats based on the given criteria
    filtered_chats = []
    for chat in chats:
        if max_line and len(filtered_chats) >= max_line:
            break
        if ((not start_date_obj or chat.date >= start_date_obj)
        and (not end_date_obj or chat.date <= end_date_obj)
        and (not speaker or chat.speaker == speaker)
        and (not message_contains or any(keyword in chat.message for keyword in message_contains))):
            filtered_chats.append(chat)


    if verbose:
        print(f" * Found ({len(filtered_chats)}) chats.")
        print(f" * Elapsed time: {datetime.now() - stime}")

    return filtered_chats