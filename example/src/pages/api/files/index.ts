import { NextApiRequest, NextApiResponse } from 'next';
import fs from 'fs';
import path from 'path';

const FILES_DIR = path.join(process.cwd(), 'data', 'files');

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === 'GET') {
    try {
      const files = await fs.promises.readdir(FILES_DIR);
      const fileList = files.map(file => ({
        id: file.replace('.md', ''),
        name: file,
      }));
      res.status(200).json(fileList);
    } catch (error) {
      res.status(500).json({ message: 'ファイルリストの取得に失敗しました' });
    }
  } else if (req.method === 'POST') {
    try {
      const { name, content } = req.body;
      const id = Date.now().toString();
      const fileName = `${id}.md`;
      await fs.promises.writeFile(path.join(FILES_DIR, fileName), content);
      res.status(201).json({ id, name, message: 'ファイルが作成されました' });
    } catch (error) {
      res.status(500).json({ message: 'ファイルの作成に失敗しました' });
    }
  } else {
    res.setHeader('Allow', ['GET', 'POST']);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}
