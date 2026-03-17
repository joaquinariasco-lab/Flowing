from flowing import trace_agent

@trace_agent
def reviewer_agent(code):
    return f"Reviewed: {code}"
