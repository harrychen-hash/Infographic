/**
 * HTML Utilities for Article Illustrator
 * 用于解析 HTML 和插入 SVG
 */

/**
 * Insert SVG after a specific element in HTML
 * @param html - The original HTML string
 * @param selector - CSS selector to find the target element
 * @param svg - The SVG string to insert
 * @returns Updated HTML string
 */
export function insertSvgAfter(
  html: string,
  selector: string,
  svg: string
): string {
  // Wrap SVG in a container div for styling
  const wrappedSvg = `<div class="article-infographic" data-selector="${escapeHtml(selector)}">${svg}</div>`;

  try {
    const { parseHTML } = require('linkedom') as typeof import('linkedom');
    const { document } = parseHTML(html);

    const target = resolveTarget(document, selector);
    if (target) {
      if (typeof target.insertAdjacentHTML === 'function') {
        target.insertAdjacentHTML('afterend', wrappedSvg);
      } else if (target.parentNode) {
        const wrapper = document.createElement('div');
        wrapper.innerHTML = wrappedSvg;
        const node = wrapper.firstChild;
        if (node) {
          target.parentNode.insertBefore(node, target.nextSibling);
        }
      }
      return document.toString();
    }
  } catch (error) {
    console.warn(`Failed to parse HTML for selector "${selector}":`, error);
  }

  // Fallback: try to find by tag and append at end
  console.warn(`Unsupported selector format: ${selector}, appending at end`);
  return html + '\n' + wrappedSvg;
}

/**
 * Insert content after the nth occurrence of a tag
 */
function resolveTarget(document: Document, selector: string): Element | null {
  if (!selector) return null;

  // ID selector: #paragraph-1
  if (selector.startsWith('#')) {
    return document.getElementById(selector.slice(1));
  }

  // nth-of-type selector: p:nth-of-type(3)
  const nthMatch = selector.match(/^(\w+):nth-of-type\((\d+)\)$/);
  if (nthMatch) {
    const [, tag, indexStr] = nthMatch;
    const index = parseInt(indexStr, 10);
    const nodes = document.querySelectorAll(tag);
    return nodes[index - 1] || null;
  }

  // contains selector: h2:contains("Title")
  if (selector.includes(':contains(') && selector.endsWith(')')) {
    const containsIndex = selector.indexOf(':contains(');
    const tag = selector.slice(0, containsIndex).trim();
    const raw = selector.slice(containsIndex + 10, -1).trim(); // inside parentheses
    const text = raw.replace(/^['"]|['"]$/g, '');
    if (tag) {
      const nodes = document.querySelectorAll(tag);
      for (const node of nodes) {
        if ((node.textContent || '').includes(text)) {
          return node as Element;
        }
      }
    }
  }

  // Fallback: try standard selector
  try {
    return document.querySelector(selector);
  } catch {
    return null;
  }
}

/**
 * Escape special characters for HTML
 */
function escapeHtml(str: string): string {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

/**
 * Escape special characters for regex
 */
/**
 * Generate CSS styles for infographic containers
 */
export function getInfographicStyles(): string {
  return `
<style>
.article-infographic {
  margin: 24px 0;
  padding: 16px;
  background: #f9fafb;
  border-radius: 8px;
  display: flex;
  justify-content: center;
  align-items: center;
}
.article-infographic svg {
  max-width: 100%;
  height: auto;
}
</style>
`;
}
