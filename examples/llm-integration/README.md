# CoreGX LLM Integration Examples

This folder contains examples showing ways to integrate a large language model (LLM) with CoreGX. 

The examples demonstrate how an LLM can generate CoreGX programs from natural language prompts while CoreGX handles the underlying geometric constraints and rendering. Some small LLMs have smaller context windows and may require shorter prompts or reduced examples. The prompt size may need to be adjusted depending on the model being used.

The included examples include:

- A constrained example with a prompt focused on the four bar linkage. 
- A constrained example with a prompt focused on triangles. 
- A full pipeline example with a longer prompt covering multiple CoreGX features.

The example pipelines as-is are designed to work with LLM systems that provide an OpenAI-compatible API, including local model servers such as LM Studio. 

## Usage

To use these examples:

1. Run an LLM service of your choice.
2. Set the required API key and API URL.
3. Run the pipeline script.
4. Review the generated CoreGX program.

Individual folders contain additional README files with more specific instructions.

## Developer applications

These examples can be adapted to create custom systems where natural language is converted into CoreGX diagrams for a particular domain or workflow.

By modifying the prompts, developers can create domain-specific generation systems for areas such as mechanical linkages, geometry education, or other constrained diagram generation tasks.

CoreGX evaluates the generated programs using real mathematical and geometric constraints rather than relying only on visual generation. This allows AI-integrated workflows to use natural language generation while still producing diagrams based on explicit geometric rules.

The same approach can also be used with local models, allowing for offline natural language-to-CoreGX workflows depending on the capabilities of the selected LLM and local setup.