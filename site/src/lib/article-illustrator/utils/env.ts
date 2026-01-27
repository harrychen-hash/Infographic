import fs from 'fs';
import path from 'path';

let cachedKey: string | null = null;

function isPlaceholder(value: string) {
  const lower = value.toLowerCase();
  return lower.includes('your-api') || lower.includes('replace-me');
}

function stripQuotes(value: string) {
  if (
    (value.startsWith('"') && value.endsWith('"')) ||
    (value.startsWith("'") && value.endsWith("'"))
  ) {
    return value.slice(1, -1);
  }
  return value;
}

function readEnvValueFromFile(filePath: string, key: string) {
  if (!fs.existsSync(filePath)) return null;
  const content = fs.readFileSync(filePath, 'utf8');
  for (const line of content.split(/\r?\n/)) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const idx = trimmed.indexOf('=');
    if (idx === -1) continue;
    const k = trimmed.slice(0, idx).trim();
    if (k !== key) continue;
    const v = stripQuotes(trimmed.slice(idx + 1).trim());
    return v || null;
  }
  return null;
}

export function getOpenAIKey() {
  if (cachedKey) return cachedKey;

  let key = process.env.OPENAI_API_KEY || '';
  if (!key || isPlaceholder(key)) {
    const candidates = [
      path.resolve(process.cwd(), '.env.local'),
      path.resolve(process.cwd(), 'site', '.env.local'),
    ];
    for (const envPath of candidates) {
      const fromFile = readEnvValueFromFile(envPath, 'OPENAI_API_KEY');
      if (fromFile) {
        process.env.OPENAI_API_KEY = fromFile;
        key = fromFile;
        break;
      }
    }
  }

  if (!key || isPlaceholder(key)) {
    throw new Error(
      'OPENAI_API_KEY is missing or invalid. Set it in site/.env.local and restart the server.'
    );
  }

  cachedKey = key;
  return key;
}

export function getOpenAIModel() {
  return (
    process.env.OPENAI_ARTICLE_ILLUSTRATOR_MODEL ||
    process.env.OPENAI_MODEL ||
    'gpt-4o-2024-08-06'
  );
}
