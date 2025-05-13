import os
import llm
from client import fetch_ticket_conversation


@llm.hookimpl
def register_fragment_loaders(register):
    register("zohoticket", zohoticket_loader)


def zohoticket_loader(argument: str) -> llm.Fragment:
    """
    Load a Zoho Ticket as a fragment.

    Argument is the ticket ID.
    """

    client_id = os.getenv("ZOHODESK_CLIENT_ID", "")
    client_secret = os.getenv("ZOHODESK_CLIENT_SECRET", "")
    org_id = os.getenv("ZOHODESK_ORG_ID", "")

    messages = fetch_ticket_conversation(org_id, client_id, client_secret, argument)
    fragment = llm.Fragment(
        "\n".join(f"{message.actor}: {message.content}" for message in messages),
        source=f"Conversation for ticket {argument}",
    )
    return fragment
