import os
import datetime
import re

import json
from typing import List, Dict, Any, Optional
import typer

app = typer.Typer()

class PHRGenerator:
    def __init__(self, history_prompts_dir: str = "history/prompts"):
        self.history_prompts_dir = history_prompts_dir
        self.template_path = ".specify/templates/phr-template.prompt.md"

    def _get_next_id(self, stage_path: str) -> int:
        """Determines the next available ID for a PHR within a given stage path."""
        existing_ids = []
        if os.path.exists(stage_path):
            for filename in os.listdir(stage_path):
                match = re.match(r"(\d+)-.*\.prompt\.md", filename)
                if match:
                    existing_ids.append(int(match.group(1)))
        
        if not existing_ids:
            return 1
        return max(existing_ids) + 1

    def _create_slug(self, title: str) -> str:
        """Converts a title into a URL-friendly slug."""
        title = title.lower()
        title = re.sub(r"[^\w\s-]", "", title)
        title = re.sub(r"[\s_-]+", "-", title)
        return title.strip("-")

    def generate_phr(
        self,
        prompt_text: str,
        response_text: str,
        title: str,
        stage: str,
        feature: Optional[str] = None,
        model: str = "gemini-1.5-flash",
        branch: str = "main",
        user: str = "default_user",
        command: str = "",
        labels: List[str] = [],
        links: Dict[str, str] = {},
        files_yaml: List[str] = [],
        tests_yaml: List[str] = [],
        outcome_impact: str = "",
        tests_summary: str = "",
        files_summary: str = "",
        next_prompts: str = "",
        reflection_note: str = "",
        failure_modes: str = "",
        grader_results: str = "",
        prompt_variant_id: str = "",
        next_experiment: str = "",
    ) -> str:
        """
        Generates and writes a Prompt History Record (PHR) file.
        """
        date_iso = datetime.datetime.now().isoformat(timespec='seconds')

        # Determine the output directory based on stage and feature
        if stage == "constitution":
            output_dir = os.path.join(self.history_prompts_dir, "constitution")
        elif feature and stage in ["spec", "plan", "tasks", "red", "green", "refactor", "explainer", "misc"]:
            output_dir = os.path.join(self.history_prompts_dir, feature)
        else:
            output_dir = os.path.join(self.history_prompts_dir, "general")
        
        os.makedirs(output_dir, exist_ok=True)

        phr_id = self._get_next_id(output_dir)
        slug = self._create_slug(title)
        
        # Ensure ID is formatted with leading zeros for sorting if needed, e.g. 001
        phr_filename = f"{str(phr_id).zfill(3)}-{slug}.{stage}.prompt.md"
        phr_filepath = os.path.join(output_dir, phr_filename)

        with open(self.template_path, "r", encoding='utf-8') as f:
            template_content = f.read()

        # Prepare YAML lists for files and tests
        files_yaml_str = "\n".join([f"  - {f}" for f in files_yaml])
        tests_yaml_str = "\n".join([f"  - {t}" for t in tests_yaml])



        replacements = {
            "{{ID}}": str(phr_id),
            "{{TITLE}}": title,
            "{{STAGE}}": stage,
            "{{DATE_ISO}}": date_iso,
            "{{SURFACE}}": "agent",
            "{{MODEL}}": model,
            "{{FEATURE}}": feature if feature else "none",
            "{{BRANCH}}": branch,
            "{{USER}}": user,
            "{{COMMAND}}": command,
            "{{LABELS}}": ', '.join([f'"{label}"' for label in labels]) ,
            "{{LINKS_SPEC}}": links.get("spec") if links.get("spec") else "null",
            "{{LINKS_TICKET}}": links.get("ticket") if links.get("ticket") else "null",
            "{{LINKS_ADR}}": links.get("adr") if links.get("adr") else "null",
            "{{LINKS_PR}}": links.get("pr") if links.get("pr") else "null",
            "{{FILES_YAML}}": files_yaml_str if files_yaml_str else "  - none",
            "{{TESTS_YAML}}": tests_yaml_str if tests_yaml_str else "  - none",
            "{{PROMPT_TEXT}}": prompt_text,
            "{{RESPONSE_TEXT}}": response_text,
            "{{OUTCOME_IMPACT}}": outcome_impact,
            "{{TESTS_SUMMARY}}": tests_summary,
            "{{FILES_SUMMARY}}": files_summary,
            "{{NEXT_PROMPTS}}": next_prompts,
            "{{REFLECTION_NOTE}}": reflection_note,
            "{{FAILURE_MODES}}": failure_modes,
            "{{GRADER_RESULTS}}": grader_results,
            "{{PROMPT_VARIANT_ID}}": prompt_variant_id,
            "{{NEXT_EXPERIMENT}}": next_experiment,
        }

        for key, value in replacements.items():
            template_content = template_content.replace(key, value)
        
        # Write the PHR file
        with open(phr_filepath, "w", encoding='utf-8') as f:
            f.write(template_content)

        return phr_filepath

# Typer command for generating PHRs
@app.command()
def generate(
    prompt_text_path: str = typer.Option(..., help="Path to the full prompt text file."),
    response_text_path: str = typer.Option(..., help="Path to the agent's response text file."),
    title: str = typer.Option(..., help="Title of the PHR."),
    stage: str = typer.Option(..., help="Stage of the PHR (e.g., general, constitution)."),
    feature: Optional[str] = typer.Option(None, help="Feature name if applicable."),
    model: str = typer.Option("gemini-1.5-flash", help="Model used."),
    branch: str = typer.Option("main", help="Current git branch."),
    user: str = typer.Option("default_user", help="User who initiated the prompt."),
    command: str = typer.Option("", help="Command that triggered the PHR."),
    labels_path: str = typer.Option("[]", help="Path to JSON string of labels."),
    links_path: str = typer.Option("{}", help="Path to JSON string of links."),
    files_yaml_path: str = typer.Option("[]", help="Path to the JSON string of files modified/created."),
    tests_yaml_path: str = typer.Option("[]", help="Path to JSON string of tests run/created."),
    outcome_impact: str = typer.Option("", help="Summary of outcome/impact."),
    tests_summary: str = typer.Option("", help="Summary of tests."),
    files_summary: str = typer.Option("", help="Summary of files."),
    next_prompts: str = typer.Option("", help="Suggested next prompts."),
    reflection_note: str = typer.Option("", help="Reflection note."),
    failure_modes: str = typer.Option("", help="Failure modes observed."),
    grader_results: str = typer.Option("", help="Grader results."),
    prompt_variant_id: str = typer.Option("", help="Prompt variant ID."),
    next_experiment: str = typer.Option("", help="Next experiment."),
):
    generator = PHRGenerator()

    with open(prompt_text_path, "r", encoding='utf-8') as f:
        prompt_text = f.read()
    with open(response_text_path, "r", encoding='utf-8') as f:
        response_text = f.read()
    
    if files_yaml_path:
        with open(files_yaml_path, "r", encoding='utf-8') as f:
            files_yaml_content = f.read()
        files_yaml_list = json.loads(files_yaml_content)
    else:
        files_yaml_list = []

    if labels_path:
        with open(labels_path, "r", encoding='utf-8') as f:
            labels_content = f.read()
        labels_list = json.loads(labels_content)
    else:
        labels_list = []
    
    if links_path:
        with open(links_path, "r", encoding='utf-8') as f:
            links_content = f.read()
        links_dict = json.loads(links_content)
    else:
        links_dict = {}

    if tests_yaml_path:
        with open(tests_yaml_path, "r", encoding='utf-8') as f:
            tests_yaml_content = f.read()
        tests_yaml_list = json.loads(tests_yaml_content)
    else:
        tests_yaml_list = []
    
    phr_path = generator.generate_phr(
        prompt_text=prompt_text,
        response_text=response_text,
        title=title,
        stage=stage,
        feature=feature,
        model=model,
        branch=branch,
        user=user,
        command=command,
        labels=labels_list,
        links=links_dict,
        files_yaml=files_yaml_list,
        tests_yaml=tests_yaml_list,
        outcome_impact=outcome_impact,
        tests_summary=tests_summary,
        files_summary=files_summary,
        next_prompts=next_prompts,
        reflection_note=reflection_note,
        failure_modes=failure_modes,
        grader_results=grader_results,
        prompt_variant_id=prompt_variant_id,
        next_experiment=next_experiment,
    )
    print(f"Generated PHR at: {phr_path}")

if __name__ == "__main__":
    app()
