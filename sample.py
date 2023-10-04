from src import parse
from src import search, statistics


file = "C:/Users/user1/Documents/카카오톡 받은 파일/KakaoTalk_20231004_1303_57_857_group.txt"
chats = parse(file)
query = { "start_date": "2023-01-01", "end_date": "2023-01-01", "speaker": "봉봉이", "max_line": 5}
test_results = search(chats, verbose=True, **query)
print("Chats>>\n", "\n".join(map(str, test_results)), sep="")

query = { "speaker": "봉봉이", "max_line": 1}
test_results = search(chats, verbose=True, **query)
print("Chats>>\n", "\n".join(map(str, test_results)), sep="")

print("\n\n")

query = { "start_date": "2023-10-04", "end_date": "2023-10-04", "message_contains": "헉"}
test_results = search(chats, verbose=True, **query)
print("Chats>>\n", "\n".join(map(str, test_results)), sep="")


query = { "start_date": "2023-10-01", "end_date": "2023-10-04"}
test_results = statistics(chats, verbose=True, **query)
print("Statistics>>")
print("Speakers:", test_results["speakers"])
print("Messages by speaker Top 5:")
for k, v in list(test_results["message_by_speaker"].items())[:5]:
    print(f"{k} : {v}")
print("Messages by date:")
for k, v in test_results["message_by_date"].items():
    print(f"{k} : {v:>5} ", "-"*int(v**0.5))
