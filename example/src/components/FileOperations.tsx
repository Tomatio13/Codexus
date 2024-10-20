import React, { useState, useEffect } from 'react';

interface File {
  id: string;
  name: string;
}

const FileOperations: React.FC = () => {
  const [files, setFiles] = useState<File[]>([]);
  const [selectedFile, setSelectedFile] = useState<string>('');

  useEffect(() => {
    fetchFiles();
  }, []);

  const fetchFiles = async () => {
    const response = await fetch('/api/files');
    const data = await response.json();
    setFiles(data);
  };

  const handleSave = async () => {
    // ファイル保存のロジックを実装
  };

  const handleLoad = async () => {
    if (selectedFile) {
      const response = await fetch(`/api/files/${selectedFile}`);
      const data = await response.json();
      // ロードしたファイルの内容を親コンポーネントに渡す処理を実装
    }
  };

  const handleNew = () => {
    // 新規ファイル作成のロジックを実装
  };

  return (
    <div className="flex space-x-2">
      <button
        className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        onClick={handleSave}
      >
        保存
      </button>
      <select
        className="px-4 py-2 border border-gray-300 rounded"
        value={selectedFile}
        onChange={(e) => setSelectedFile(e.target.value)}
      >
        <option value="">ファイルを選択</option>
        {files.map((file) => (
          <option key={file.id} value={file.id}>
            {file.name}
          </option>
        ))}
      </select>
      <button
        className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
        onClick={handleLoad}
      >
        読み込み
      </button>
      <button
        className="px-4 py-2 bg-yellow-500 text-white rounded hover:bg-yellow-600"
        onClick={handleNew}
      >
        新規
      </button>
    </div>
  );
};

export default FileOperations;
