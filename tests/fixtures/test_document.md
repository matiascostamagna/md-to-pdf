# MD to PDF — Demo Document

## Text Formatting

This is a **bold text** and this is *italic text*. You can have ~~strikethrough~~ and ==highlighted== text. Here's a [link to GitHub](https://github.com).

## Code Blocks

### Python

```python
import asyncio
from pathlib import Path

async def count_lines(path: Path) -> int:
    content = await asyncio.to_thread(path.read_text)
    return len(content.splitlines())

result = asyncio.run(count_lines(Path("file.txt")))
print(f"Lines: {result}")
```

### JavaScript

```javascript
function fibonacci(n) {
  if (n <= 1) return n;
  let a = 0, b = 1;
  for (let i = 2; i <= n; i++) {
    [a, b] = [b, a + b];
  }
  return b;
}

console.log(fibonacci(10)); // 55
```

### SQL

```sql
SELECT
  u.name,
  COUNT(o.id) AS total_orders,
  SUM(o.amount) AS total_spent
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE o.created_at >= '2025-01-01'
GROUP BY u.name
HAVING COUNT(o.id) > 5
ORDER BY total_spent DESC
LIMIT 10;
```

## Blockquotes

> This is a blockquote with multiple paragraphs.
>
> Second paragraph inside the blockquote. It can contain **bold** and other formatting.

> [!NOTE]
> This is an info-style callout. Use it for helpful hints.

> [!WARNING]
> This is a warning callout. Pay attention to this content.

## Tables

| Feature | Support | Performance | Complexity |
|---------|:-------:|------------:|-----------:|
| Markdown rendering | Full | Excellent | Low |
| Syntax highlighting | Full | Very good | Medium |
| Image embedding | Full | Good | Low |
| LaTeX math | MathJax | Good | Medium |
| Page breaks | `\newpage` | N/A | Low |

## Task Lists

- [x] Implement Markdown parser
- [x] Add syntax highlighting
- [x] Support embedded images
- [ ] Add live preview reload
- [ ] Implement dark mode for GUI

## Definition Lists

Markdown
: A lightweight markup language for creating formatted text.

WeasyPrint
: A Python library for generating PDF from HTML and CSS.

PyMdown Extensions
: A collection of extensions for Python-Markdown providing advanced features.

## Math Formulas

Inline math: $E = mc^2$

Block math:

$$
\int_{-\infty}^{\infty} e^{-x^2} \, dx = \sqrt{\pi}
$$

The quadratic formula:

$$
x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
$$

Matrix notation:

$$
\begin{bmatrix}
a_{11} & a_{12} & a_{13} \\
a_{21} & a_{22} & a_{23} \\
a_{31} & a_{32} & a_{33}
\end{bmatrix}
$$

## Keyboard Keys

Press <kbd>Ctrl</kbd> + <kbd>S</kbd> to save, or <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd> to open the command palette.

## Footnotes

Here's a sentence with a footnote[^1]. And another one[^2].

[^1]: This is the first footnote. It can contain **formatting** and even code: `print("hello")`.
[^2]: This is the second footnote. Multiple paragraphs are allowed too.

## Abbreviations

The HTML specification is maintained by W3C.

*[HTML]: HyperText Markup Language
*[W3C]: World Wide Web Consortium

## Emoji

Here are some emojis: :smile: :rocket: :fire: :heart: :zap: :star:

## Details / Collapsible Sections

??? info "Click to see more information"
    This content is hidden by default.

    ```python
    print("Hello from collapsed section!")
    ```

## Horizontal Rules

Above the line.

---

Below the line.

## Ordered and Nested Lists

1. First item
   1. Nested item one
   2. Nested item two
2. Second item
   - Unordered nested
   - Another unordered
3. Third item

## Page Break

\newpage

## Next Page Content

This content appears on a new page after the page break above. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.

Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.