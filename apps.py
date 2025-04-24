import chainlit as cl
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.functions import kernel_function

from semantic_kernel.agents import ChatHistoryAgentThread
from app.agents_config import create_kernel, create_agents

@cl.set_starters
async def set_starters():
    return [
        cl.Starter(
            label="ask about electrical outages in a city of Chile",
            message="Can you tell me if there are electrical failures in a city?",
            icon="/public/idea.svg",
            ),

        cl.Starter(
            label="What crew is nearby?",
            message="I need you to tell me which squad is near my city.",
            icon="/public/truck.jpg",
            ),
        cl.Starter(
            label="Report a power failure",
            message="I need to report an electrical failure near where I live.",
            icon="/public/fault.png",
            ),
        cl.Starter(
            label="Ask about legal deadlines",
            message="According to Chilean regulations, how long can a utility company take to respond to an outage?",
            icon="/public/law.png",
            )
        ]


@cl.on_chat_start
async def on_chat_start():
    # Setup Semantic Kernel
    kernel = await create_kernel()
    agent = await create_agents(kernel)
  
    thread: ChatHistoryAgentThread = None
    cl.user_session.set("agent", agent)
    cl.user_session.set("thread", thread)

@cl.on_message
async def on_message(message: cl.Message):
    agent = cl.user_session.get("agent") 
    thread = cl.user_session.get("thread") # type: ChatHistoryAgentThread 

    answer = cl.Message(content="")

    async for response in agent.invoke_stream(messages=message.content, thread=thread):

        if response.content:
            await answer.stream_token(str(response.content))

        thread = response.thread
        cl.user_session.set("thread", thread)

    # Send the final message
    await answer.send()