import React from 'react';

interface ThemeToggleProps {
  theme: string;
  toggleTheme: () => void;
}

const ThemeToggle: React.FC<ThemeToggleProps> = ({ theme, toggleTheme }) => {
  return (
    <button
      className={`px-4 py-2 rounded ${theme === 'dark' ? 'bg-yellow-400 text-black' : 'bg-gray-800 text-white'}`}
      onClick={toggleTheme}
    >
      {theme === 'dark' ? '🌞 ライトモード' : '🌙 ダークモード'}
    </button>
  );
};

export default ThemeToggle;
