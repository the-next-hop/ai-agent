from ollama import Client
from tools import run_show_command, run_set_command, get_all_devices

client = Client()

messages = [
  {
    'role': 'system',
    'content': "youre a network assistant for a lab with two Arista switches called SW1 and SW2, you can run read only show commands and if you don't know something, say so."
  },
  
  {
    'role': 'user',
    'content': 'what is the firmware verison of SW1 and SW2',
  },
]


dispatch_dictionary = {
    "run_show_command" : run_show_command,
}

while True:
    chat = client.chat(
        'qwen3:14b', 
        messages=messages, 
        tools=[run_show_command],
        think=False,
        )

    reply = chat.message


    if reply.tool_calls is not None:
        messages.append(reply)
        tool_calls = reply.tool_calls

        for tool in tool_calls:#
            tool_name = tool.function.name
            args = tool.function.arguments

            try:
                funct_name = dispatch_dictionary.get(tool_name, "n/a")
                output = funct_name(**args)
                message = {
                    "role": "tool",
                    "content": output,
                    "tool_name": tool_name,
                }
                messages.append(message)


            except Exception as e:
                print(f"[ERROR] : {e}")

    else:
        print(reply.content)
        break
