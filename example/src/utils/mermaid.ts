import mermaid from 'mermaid';

export function renderMermaidDiagram() {
  mermaid.init(undefined, document.querySelectorAll('.language-mermaid'));
}
