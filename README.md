# kakaotalk-chat-finder
카카오톡 채팅방 대화 내역을 파싱하고 검색할 수 있습니다.

# 사용 방법

## 대화 내역 파싱

카카오톡 대화 내보내기로 txt 파일을 파싱합니다.

오픈채팅의 경우 파일의 모양은 아래와 같습니다.

```
어쩌구 저쩌구 채팅방 님과 카카오톡 대화
저장한 날짜 : 2023-10-04 13:03:59

--------------- 2021년 12월 14일 화요일 ---------------
지나가던사람님이 들어왔습니다.운영정책을 위반한 메시지로 신고 접수 시 카카오톡 이용에 제한이 있을 수 있습니다.
불법촬영물등 식별 및 게재제한 조치 안내
그룹 오픈채팅방에서 동영상・압축파일 전송 시 전기통신사업법에 따라 방송통신심의위원회에서 불법촬영물등으로 심의・의결한 정보에 해당하는지를 비교・식별 후 전송을 제한하는 조치가 적용됩니다. 불법촬영물등을 전송할 경우 관련 법령에 따라 처벌받을 수 있사오니 서비스 이용 시 유의하여 주시기 바랍니다.
[지나가던사람] [오후 4:17] 안녕하세요 새내기 개발자입니다
[행인A] [오후 4:17] 안녕하세요~
행인B님이 들어왔습니다.
```

아래와 같이 파일을 입력하여 파싱할 수 있습니다.

```python
from parser import parse

filepath = "data/KakaoTalk_20231004_xxxxxxxx_group.txt"
chats = parse(filepath)
```

혹은 텍스트 리스트로 직접 파싱할 수도 있습니다.

```python
from parser import parse

with open(filename, "r", encoding="utf-8") as f:
    content = f.readlines()
    chats = parse_text(content)
```

## 대화 내용 검색

파싱된 채팅 내역을 기간, 유저, 발화내용으로 검색할 수 있습니다.

### 특정 기간 동안 특정 유저의 대화 내용을 최대 5개만 검색

`2023-01-01` ~ `2023-01-01` 하루 동안 `봉봉이` 라는 발화자의 대화 내역을 검색

코드
```python
query = { "start_date": "2023-01-01", "end_date": "2023-01-01", "speaker": "봉봉이" }
test_results = search(chats, verbose=True, **query)
print("Chats>>\n", "\n".join(map(str, test_results)), sep="")
```

결과
```
 - Chat data length: 247088
 - Start date: 2023-01-01
 - End date: 2023-01-01
 - Speaker: 봉봉이
 * Searching ...
 * Found (2) chats.
 * Elapsed time: 0:00:00.016006
Chats>>
2023-01-01 - 봉봉이: 새해복많이받으세요!!
2023-01-01 - 봉봉이: 2023년도에는 술을 마시지 않겠습니다 제발 반드시
```

### 유저의 최초 발언 검색

기간을 입력하지 않으면 전체 내역을 검색합니다.

코드
```python
query = { "speaker": "봉봉이", "max_line": 1}
test_results = search(chats, verbose=True, **query)
print("Chats>>\n", "\n".join(map(str, test_results)), sep="")
```
결과
```
 - Chat data length: 247088
 - Speaker: 봉봉이
 * Searching ...
 * Found (1) chats.
 * Elapsed time: 0:00:00
Chats>>
2021-12-14 - 봉봉이: 와아 어디신가요?
```

## 통계

단순한 통계를 낼 수 있습니다. 조건은 대화 내용 검색과 같습니다.

### 특정 기간동안의 통계

`2023-10-01` ~ `2023-01-04` 동안 대화 내역에 대한 통계

```python
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
```

결과
```
 - Chat data length: 247088
 - Start date: 2023-10-01
 - End date: 2023-10-04
 * Searching ...
 * Found (482) chats.
 * Elapsed time: 0:00:00.009923
Statistics>>
Speakers: 28
Messages by speaker Top 5:
유저A : 140
지나가는 행인 : 73
유저인척하는 봇 : 40
화가난 네오 : 34
화가 안난 네오 : 25
Messages by date:
2023-10-02 :   221  --------------
2023-10-03 :   158  ------------
2023-10-04 :   103  ----------
```