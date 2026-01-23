import os
import json
import re
from typing import List, Dict, Any
import config
from jinja2 import Template

class PromptAssembler:
    """Dynamic prompt assembler for Lumina Vision Engine using Jinja2."""
    
    def __init__(self):
        """Initialize the prompt assembler with template and configuration."""
        self.template_path = os.path.join(config.PROJECT_ROOT, 'schemas', 'prompts', config.LUMINA_TEMPLATE)
        self.role_path = os.path.join(config.PROJECT_ROOT, 'data', 'roles', config.LUMINA_ROLE)
        self.system_schema_path = os.path.join(config.PROJECT_ROOT, 'schemas', 'system_schema.json')
    
    def _get_axis_data(self, axis_name: str) -> Dict[str, Any]:
        """Extract definition and tags from axis vocabulary file.
        
        Args:
            axis_name: Name of the axis (e.g., 'domain', 'somatic')
            
        Returns:
            Dictionary with 'name', 'definition', and 'tags_list' keys
        """
        axis_file = os.path.join(config.PROJECT_ROOT, 'data', 'vocab', f'lumina_{axis_name}.md')
        
        if not os.path.exists(axis_file):
            raise FileNotFoundError(f"Axis vocabulary file not found: {axis_file}")
        
        with open(axis_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract definition from first blockquote
        definition_match = re.search(r'>\s*\*\*Definition\*\*:\s*(.+)', content)
        if not definition_match:
            raise ValueError(f"Definition not found in {axis_file}")
        
        definition = definition_match.group(1).strip()
        
        # Extract tags from bullet points
        tags_matches = re.findall(r'^-\s+([^\n]+)$', content, re.MULTILINE)
        tags = [tag.strip() for tag in tags_matches if tag.strip()]
        
        if not tags:
            raise ValueError(f"No tags found in {axis_file}")
        
        return {
            'name': axis_name,
            'definition': definition,
            'tags_list': ', '.join(tags)
        }
    
    def _load_role_description(self) -> str:
        """Load the role description from the architect file."""
        if not os.path.exists(self.role_path):
            raise FileNotFoundError(f"Role file not found: {self.role_path}")
        
        with open(self.role_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    
    def _load_system_schema(self) -> str:
        """Load the system schema JSON."""
        # Use the new minicpm response schema
        schema_path = os.path.join(config.PROJECT_ROOT, 'schemas', 'prompts', 'minicpm_response_v1.json')
        if not os.path.exists(schema_path):
            raise FileNotFoundError(f"Response schema file not found: {schema_path}")
        
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema = json.load(f)
        
        return json.dumps(schema, indent=2)
    
    def _load_template(self) -> str:
        """Load the template file."""
        if not os.path.exists(self.template_path):
            raise FileNotFoundError(f"Template file not found: {self.template_path}")
        
        with open(self.template_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def render_system_prompt(self, active_axes_list: List[str]) -> str:
        """Render the complete system prompt with dynamic content using Jinja2.
        
        Args:
            active_axes_list: List of axis names to include in the prompt
            
        Returns:
            Rendered system prompt string
        """
        # Load base components
        template_content = self._load_template()
        role_description = self._load_role_description()
        system_schema_json = self._load_system_schema()
        
        # Get axis data for active axes
        active_axes_data = []
        for axis_name in active_axes_list:
            try:
                axis_data = self._get_axis_data(axis_name)
                active_axes_data.append(axis_data)
            except Exception as e:
                raise ValueError(f"Failed to load axis data for '{axis_name}': {e}")
        
        # Create Jinja2 template
        template = Template(template_content)
        
        # Render template with context
        context = {
            'ROLE_DESCRIPTION': role_description,
            'ACTIVE_AXES': active_axes_data,
            'SYSTEM_SCHEMA_JSON': system_schema_json
        }
        
        prompt = template.render(context)
        
        return prompt.strip()

def log(message: str):
    """Simple logging function for the assembler."""
    from datetime import datetime
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] [PROMPT_ASSEMBLER] {message}")
