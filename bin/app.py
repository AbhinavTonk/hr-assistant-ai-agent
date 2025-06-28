import gradio as gr

from ai_agents import hr_agent


# --- Core logic ---------------------------------------------------------------
def ask_hr_assistant_ai_agent(query: str) -> str:
    response = hr_agent.ask_hr_assistant_ai_agent(query)
    return f"<h3>HR Agent Response:</h3>{response}"


# --- Gradio UI ----------------------------------------------------------------
custom_css = """
/* Target the primary button (Submit) */
button[class*="primary"] {
    background-color: #cce6ff !important;  /* light blue */
    color: black !important;               /* text color */
    border: none !important;
}

/* Optional: Add hover effect */
button[class*="primary"]:hover {
    background-color: #b3daff !important;
}
"""

demo = gr.Interface(
    fn=ask_hr_assistant_ai_agent,  # function to run
    inputs=gr.Textbox(
        label="Ask",
        placeholder="Type your HR Policy related question here…",
        lines=2,
    ),
    outputs=gr.HTML(label="Response"),
    title="👩‍💼👨‍💼 HR Assistant AI Agent 👩‍💼👨‍💼",  # page title
    description='''<h5 style="color: #2c3e50; font-family: Arial; font-weight: bold;">
                    Ask me anything about HR ‒ policies
                    </h5    >''',
    css=custom_css
)

# --- Run locally --------------------------------------------------------------
if __name__ == "__main__":
    demo.launch()
