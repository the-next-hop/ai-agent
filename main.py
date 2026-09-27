from ollama import Client
from tools import run_show_command, run_set_command, get_all_devices

client = Client()

messages = [
  {
    'role': 'system',
    'content': "youre a network assistant for a lab with two Arista switches called SW1 and SW2, you can run read only show commands and set commands too, and if you don't know something, say so. Dont do anything stupid!"
  },
  {
    'role': 'user',
    'content': 'tell me how many switches do we have in our estate',
  },
]


dispatch_dictionary = {
    "run_show_command" : run_show_command,
    "run_set_command" : run_set_command,
    "get_all_devices" : get_all_devices,
}

while True:
    chat = client.chat(
        'qwen3:14b', 
        messages=messages, 
        tools=[run_show_command, get_all_devices],
        think=False,
        )

    reply = chat.message


    if reply.tool_calls is not None:
        messages.append(reply)
        tool_calls = reply.tool_calls

        for tool in tool_calls:#
            tool_name = tool.function.name
            args = tool.function.arguments
            print(f"[DEBUG]: NAME = {tool_name} \n ARGS: {args} \n DISPATCH_DICT = {dispatch_dictionary}")

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
        print("No further (or any) tool calls found.")
        print(reply.content)
        break

    # print(chat.message)
