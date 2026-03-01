from flowing.runtime import FlowingRuntime
from flowing.llm_wrapper import call_llm


def fake_llm(prompt):
    return f"Processed: {prompt}"


def run_workflow(runtime):
    decision_id = "planner-1"

    prompt = "Research quantum networking"

    output = call_llm(
        runtime=runtime,
        decision_id=decision_id,
        agent_id="planner",
        prompt=prompt,
        real_llm_call=fake_llm
    )

    print("FINAL OUTPUT:", output)


if __name__ == "__main__":
    runtime = FlowingRuntime(mode="record")
    run_workflow(runtime)
