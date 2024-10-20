import React, { useEffect } from 'react';
import { remark } from 'remark';
import html from 'remark-html';
import { renderMermaidDiagram } from '../utils/mermaid';

interface MarkdownPreviewProps {
  markdown: string;
}

const MarkdownPreview: React.FC<MarkdownPreviewProps> = ({ markdown }) => {
  const [renderedContent, setRenderedContent] = React.useState('');

  useEffect(() => {
    const renderMarkdown = async () => {
      const processedContent = await remark()
        .use(html)
        .process(markdown);
      setRenderedContent(processedContent.toString());
    };

    renderMarkdown();
  }, [markdown]);

  useEffect(() => {
    renderMermaidDiagram();
  }, [renderedContent]);

  return (
    <div
      className="w-full h-full p-4 border border-gray-300 rounded-md overflow-auto"
      dangerouslySetInnerHTML={{ __html: renderedContent }}
    />
  );
};

export default MarkdownPreview;
