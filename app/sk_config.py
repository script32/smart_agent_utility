from semantic_kernel.kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
import os
from dotenv import load_dotenv

load_dotenv()

def create_kernel():
    kernel = Kernel()
    kernel.add_chat_service(
        "default",
        AzureChatCompletion(
            chat_deployment_name=os.getenv("OPENAI_DEPLOYMENT_NAME"),
            endpoint=os.getenv("OPENAI_ENDPOINT"),
            api_key=os.getenv("OPENAI_API_KEY")
        )
    )
    return kernel
