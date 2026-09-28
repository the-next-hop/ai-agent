# Local AI Network Agent

A minimal AI agent, built from scratch in Python, that answers questions about your network by running show commands on real devices. The language model runs locally through Ollama, and Netmiko handles the SSH side. No frameworks, no cloud APIs, and nothing leaves your network.

This repository accompanies the article on [The Next Hop](https://the-next-hop.co.uk): **[Local AI Meets Netmiko: Build Your Own Network Agent](LINK-TO-ARTICLE)**.

## Example

```
venv ❯ python main.py
The firmware version (software image version) for both SW1 and SW2 is:

- **SW1**: `4.32.0F-36401836.4320F (engineering build)`
- **SW2**: `4.32.0F-36401836.4320F (engineering build)`

Both switches are running the same firmware version.
```

## How it works

The model never touches your devices. When it needs data, it replies with a request to run a tool (for example, `show version` on SW1). The script runs the actual function, sends the output back to the model, and repeats until the model has enough to answer.

1. Your question and a system prompt are sent to the model, along with a description of the available tools.
2. The model responds with a tool call instead of an answer.
3. `main.py` looks up the matching function in `tools.py` and runs it via Netmiko.
4. The output is added to the conversation as a `tool` message and sent back to the model.
5. Once the model replies without any tool calls, the final answer is printed.

## Project structure

| File | Purpose |
|---|---|
| `main.py` | The agent: Ollama client, system prompt, messages and the tool-calling loop |
| `tools.py` | Network helpers: credentials, device inventory and `run_show_command` |

## Prerequisites

- A GPU with enough VRAM for your chosen model (the article uses `qwen3:14b` on a 16 GB card)
- [Ollama](https://ollama.com/download) installed and running
- Python 3.10 or newer
- Network devices reachable over SSH. The article uses Arista cEOS in Containerlab, but physical devices work just as well.

## Setup

Clone the repository and create a virtual environment:

```bash
git clone https://github.com/the-next-hop/ai-agent.git
cd ai-agent
python3 -m venv venv
source venv/bin/activate
pip install ollama netmiko
```

Pull the model:

```bash
ollama pull qwen3:14b
```

Set your device credentials as environment variables:

```bash
export ARISTA_USERNAME=admin
export ARISTA_PASSWORD=admin
```

On fish, use `set -x ARISTA_USERNAME admin` instead.

Update the device inventory in `tools.py` with your own device names and management IPs:

```python
DEVICES = {
    "SW1" : "10.0.101.11",
    "SW2" : "10.0.101.12",
}
```

If you use different device names, update the system prompt in `main.py` to match.

## Usage

Edit the user message in `main.py` with your question, then run:

```bash
python main.py
```

## Notes

- The agent is **read-only** by design. It only has access to a show command tool. Pushing configuration from an AI agent needs proper safety controls (least-privilege accounts, command validation, human approval), which are covered separately.
- Credentials stay in your Python code and are never sent to the model.
- `think=False` in the chat call disables the model's reasoning step for faster responses. Set it to `True` to see how the model decides which tool to call.
- To use a different platform, change `device_type` in `tools.py` to any [Netmiko-supported platform](https://github.com/ktbyers/netmiko/blob/develop/PLATFORMS.md).b
