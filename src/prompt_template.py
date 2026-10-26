from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

PROMPTS_DIR = Path(__file__).resolve().parents[1] / "prompts"


def render_assistant_messages(
    *,
    customer_text: str,
    intent_names: list[str],
    variant: str = "constraint_based",
    include_tool: bool = False,
    few_shot_block: str = "",
    output_rules: str | None = None,
) -> list[dict]:
    env = Environment(
        loader=FileSystemLoader(str(PROMPTS_DIR)),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template("assistant_template.jinja2")
    rendered = template.render(
        customer_text=customer_text,
        intent_names=intent_names,
        variant=variant,
        include_tool=include_tool,
        few_shot_block=few_shot_block,
        output_rules=output_rules,
    )
    return json_loads_messages(rendered)


def json_loads_messages(rendered: str) -> list[dict]:
    import json

    return json.loads(rendered)
