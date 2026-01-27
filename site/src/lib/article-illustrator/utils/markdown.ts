/**
 * Markdown to HTML utility
 * 简单的 Markdown 转 HTML 工具
 */

/**
 * Convert Markdown to HTML
 * 使用简单的正则替换，支持基本 Markdown 语法
 */
export function markdownToHtml(markdown: string): string {
  let html = markdown;

  // Escape HTML entities first
  html = html
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');

  // Headers
  html = html.replace(/^### (.+)$/gm, '<h3>$1</h3>');
  html = html.replace(/^## (.+)$/gm, '<h2>$1</h2>');
  html = html.replace(/^# (.+)$/gm, '<h1>$1</h1>');

  // Bold and italic
  html = html.replace(/\*\*\*(.+?)\*\*\*/g, '<strong><em>$1</em></strong>');
  html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');

  // Links
  html = html.replace(/\[(.+?)\]\((.+?)\)/g, '<a href="$2">$1</a>');

  // Line breaks - convert double newlines to paragraphs
  const paragraphs = html.split(/\n\n+/);
  html = paragraphs
    .map((p) => {
      p = p.trim();
      if (!p) return '';
      // Don't wrap headers in <p>
      if (p.startsWith('<h')) return p;
      return `<p>${p.replace(/\n/g, '<br>')}</p>`;
    })
    .filter(Boolean)
    .join('\n');

  return html;
}

/**
 * Detect if input is Markdown or HTML
 */
export function isMarkdown(content: string): boolean {
  const trimmed = content.trim();

  // If it starts with HTML tags, treat as HTML
  if (trimmed.startsWith('<') && !trimmed.startsWith('<http')) {
    return false;
  }

  // Check for common Markdown patterns
  const markdownPatterns = [
    /^#+\s/m, // Headers
    /\*\*.+\*\*/, // Bold
    /\[.+\]\(.+\)/, // Links
    /^[-*]\s/m, // Lists
    /^>\s/m, // Blockquotes
  ];

  return markdownPatterns.some((pattern) => pattern.test(content));
}

/**
 * Convert content to HTML (auto-detect Markdown)
 */
export function toHtml(content: string): string {
  if (isMarkdown(content)) {
    return markdownToHtml(content);
  }
  return content;
}
