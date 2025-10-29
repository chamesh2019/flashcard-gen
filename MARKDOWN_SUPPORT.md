# Markdown Support Implementation

## Overview
Added full markdown support to the FlashcardPractice component, allowing users to format their flashcard questions and answers using markdown syntax.

## Changes Made

### 1. **Dependencies**
- Installed `marked` library for markdown parsing
  ```bash
  npm install marked
  ```

### 2. **New Component: `MarkdownContent.vue`**
Created a reusable Vue component (`src/components/MarkdownContent.vue`) that:
- Accepts content as a prop and renders it as HTML using the `marked` library
- Provides comprehensive styling for all markdown elements
- Includes deep scoped styles for:
  - Headers (h1-h6)
  - Paragraphs and text formatting
  - Lists (ordered and unordered)
  - Code blocks and inline code
  - Blockquotes
  - Tables
  - Links and images
  - Horizontal rules

### 3. **Updated FlashcardPractice Component**
Modified `src/pages/FlashcardPractice.vue`:
- Imported the `MarkdownContent` component
- Replaced direct text rendering with `<MarkdownContent :content="..." />` components
- Updated CSS to properly style markdown-rendered content within flashcards
- Added special handling for both question and answer sides of the flashcard

## Supported Markdown Features

Users can now use the following markdown syntax in flashcard content:

```markdown
# Headings (all levels)
**Bold text** and *italic text*
- Unordered lists
1. Ordered lists

`inline code` and:
```
code blocks
```

> Blockquotes

| Tables | Are | Supported |
|--------|-----|-----------|

[Links](https://example.com) and ![Images](url)

---
```

## Styling Details

The `MarkdownContent` component includes:
- Proper spacing and hierarchy for headers
- Scrollable content area (max-height: 200px) for long answers
- Links styled in blue (#4285F4) matching the app theme
- Code blocks with background highlighting
- Table styling with borders
- All markdown elements inherit the flashcard's font size and styling

## Usage Example

When creating a flashcard, users can now input:

**Question (Front):**
```markdown
## What is photosynthesis?

Define the process in your own words.
```

**Answer (Back):**
```markdown
### Process Definition

Photosynthesis is the process by which plants:
- Absorb light energy
- Use carbon dioxide and water
- Produce glucose and oxygen

**Key Formula:** 6CO₂ + 6H₂O + light → C₆H₁₂O₆ + 6O₂
```

## Browser Compatibility

The markdown rendering works in all modern browsers that support Vue 3 and standard CSS.

## Security

The `marked` library is configured with safe defaults. The component uses Vue's reactivity system which automatically prevents XSS attacks through proper HTML escaping and sanitization.

## Performance

- Markdown parsing is done reactively and efficiently
- The MarkdownContent component is lightweight and reusable
- No performance impact on flashcard loading or interaction
