import asyncio
import json


with open("data.json", encoding="utf-8") as file:
    datas = json.load(file)


async def handler(event, context):
    result = {"response": {}, "session_state": {}}
    request = event["request"]

    if "state" in request:
        cur_stage = request["state"]["session"]["stage"]
    else:
        result["session_state"]["stage"] = "0.0"
        result["response"]["text"] = datas[0][0]["text"]

        return result

    last_deep, last_node = map(int, cur_stage.split("."))

    next_stage = None

    for answer in datas[last_deep][last_node]["answers"]:
        if answer["command"] == request["command"].lower():
            next_stage = answer["next_stage"]
            break

    if not next_stage:
        result["response"]["text"] = "Не нашел"
        result["session_state"]["stage"] = cur_stage
        return result

    deep, node = map(int, next_stage.split("."))

    result["session_state"]["stage"] = next_stage
    result["response"]["text"] = datas[deep][node]["text"]

    return result


if __name__ == "__main__":
    data = {
        "version": "0.0.1",
        "request": {"command": ""},
    }

    while (inp := input("Enter zapros for Asisa: ")) != "exit":
        data["request"]["command"] = inp
        resp = asyncio.run(handler(data, {}))

        data["request"]["state"] = {}
        data["request"]["state"]["session"] = resp["session_state"]

        print("Server asnwer:", resp["response"]["text"])
