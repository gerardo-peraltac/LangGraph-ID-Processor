from langgraph.graph import StateGraph
from agents import parse_id_document_with_llm, is_document_submission
from reservation_mock import mock_reservation, send_guest_data_via_email
from state import ConversationState

# === LangGraph Node Functions ===
def start_node(state: ConversationState, config: dict):
    print("Hi! Please upload ID documents for both guests (2 total).")
    return {"next": "awaiting_documents", "value": state}

def awaiting_documents(state: ConversationState, config: dict):
    user_input = config["input"]
    if is_document_submission(user_input):
        print(f"Document received: {user_input}")
        parsed = parse_id_document_with_llm(user_input)
        state.submitted_files.append(user_input)
        state.parsed_guests.append(parsed)
        return {"next": "check_completion", "value": state}
    else:
        return {"next": "remind_missing_docs", "value": state}

def remind_missing_docs(state: ConversationState, config: dict):
    print(f"Still waiting for {state.missing_count()} document(s). Please upload remaining ID(s).")
    return {"next": "awaiting_documents", "value": state}

def check_completion(state: ConversationState, config: dict):
    if state.all_documents_received():
        return {"next": "submit_data", "value": state}
    return {"next": "awaiting_documents", "value": state}

def submit_data(state: ConversationState, config: dict):
    if not getattr(state, "submitted", False):
        send_guest_data_via_email(mock_reservation["email"], state.parsed_guests)
        state.submitted = True
    return {"next": "thank_user", "value": state}

def thank_user(state: ConversationState, config: dict):
    if not getattr(state, "_thanked", False):
        print("Thanks! All guest information has been successfully processed.")
        state._thanked = True
    return {"next": None, "value": state}  # Modified to return dict instead of None

# === Build LangGraph ===
graph = StateGraph(ConversationState)
graph.add_node("start", start_node)
graph.add_node("awaiting_documents", awaiting_documents)
graph.add_node("remind_missing_docs", remind_missing_docs)
graph.add_node("check_completion", check_completion)
graph.add_node("submit_data", submit_data)
graph.add_node("thank_user", thank_user)

graph.set_entry_point("start")
graph.set_finish_point("thank_user")

machine = graph.compile()

# === Simulated User Inputs ===
state = ConversationState()
inputs = ["./mock_ids/id_1.png", "Just checking in", "./mock_ids/id_2.png"]

# Manually step through graph node-by-node
step = "start"
node_map = {
    "start": start_node,
    "awaiting_documents": awaiting_documents,
    "remind_missing_docs": remind_missing_docs,
    "check_completion": check_completion,
    "submit_data": submit_data,
    "thank_user": thank_user,
}

for user_msg in [None] + inputs:
    if user_msg is not None:
        print(f"\n[USER] {user_msg}")
    node_fn = node_map[step]
    try:
        result = node_fn(state, {"input": user_msg})
        if result is None or result["next"] is None:
            break
        step = result["next"]
        state = result["value"]
    except Exception as e:
        print("[ERROR]", e)
        break

# Final step (in case thank_user needs to run post-input)
while step and step != "thank_user":
    node_fn = node_map[step]
    result = node_fn(state, {"input": None})
    if result is None or result["next"] is None:
        break
    step = result["next"]
    state = result["value"]

# One last execution if we're at thank_user
if step == "thank_user":
    node_map[step](state, {"input": None})
