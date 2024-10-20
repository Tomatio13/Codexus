import React, { useState } from 'react';
import MarkdownEditor from '../components/MarkdownEditor';
import MarkdownPreview from '../components/MarkdownPreview';
import FileOperations from '../components/FileOperations';
import ThemeToggle from '../components/ThemeToggle';
import useLocalStorage from '../hooks/useLocalStorage';

const Home: React.FC = () => {
  const [markdown, setMarkdown] = useState('');
  const [theme, setTheme] = useLocalStorage('theme', 'light');

  const handleMarkdownChange = (value: string) => {
    setMarkdown(value);
  };

  const toggleTheme = () => {
    setTheme(theme === 'light' ? 'dark' : 'light');
  };

  return (
    <div className={`min-h-screen ${theme === 'dark' ? 'bg-gray-900 text-white' : 'bg-white text-black'}`}>
      <div className="container mx-auto p-4">
        <div className="flex justify-between mb-4">
          <FileOperations />
          <ThemeToggle theme={theme} toggleTheme={toggleTheme} />
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <MarkdownEditor value={markdown} onChange={handleMarkdownChange} />
          <MarkdownPreview markdown={markdown} />
        </div>
      </div>
    </div>
  );
};

export default Home;
