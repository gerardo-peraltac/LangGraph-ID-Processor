class ConversationState:
    def __init__(self):
        self.expected_docs = 2
        self.submitted_files = []
        self.parsed_guests = []

    def all_documents_received(self):
        return len(self.parsed_guests) == self.expected_docs

    def missing_count(self):
        return self.expected_docs - len(self.parsed_guests)
