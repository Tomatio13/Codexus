import { NextApiRequest, NextApiResponse } from 'next';
import fs from 'fs';
import path from 'path';

const FILES_DIR = path.join(process.cwd(), 'data', 'files');

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const { id } = req.query;
  const filePath = path.join(FILES_DIR, `${id}.md`);

  if (req.method === 'GET') {
    try {
      const content = await fs.promises.readFile(filePath, 'utf-8');
      res.status(200).json({ id, content });
    } catch (error) {
      res.status(404).json({ message: 'ファイルが見つかりません' });
    }
  } else if (req.method === 'PUT') {
    try {
      const { content } = req.body;
      await fs.promises.writeFile(filePath, content);
      res.status(200).json({ message: 'ファイルが更新されました' });
    } catch (error) {
      res.status(500).json({ message: 'ファイルの更新に失敗しました' });
    }
  } else if (req.method === 'DELETE') {
    try {
      await fs.promises.unlink(filePath);
      res.status(200).json({ message: 'ファイルが削除されました' });
    } catch (error) {
      res.status(500).json({ message: 'ファイルの削除に失敗しました' });
    }
  } else {
    res.setHeader('Allow', ['GET', 'PUT', 'DELETE']);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}
