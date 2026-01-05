# KASP Primer Design Service - UI Optimization Plan

## Goal
Transform the current functional UI into a modern, professional, and visually appealing scientific tool. The design should convey precision, reliability, and ease of use.

## Design Principles
1.  **Scientific & Clean**: Use whitespace effectively to reduce cognitive load.
2.  **Modern**: Utilize soft shadows, rounded corners, and subtle gradients.
3.  **Responsive**: Ensure great experience on different screen sizes.
4.  **Feedback-Oriented**: Clear states for loading, success, and errors.

## Proposed Changes

### 1. Color Palette
Shift from default Element Plus colors to a curated scientific palette.

- **Primary**: `#0F766E` (Teal - for scientific/bio feel) or `#2563EB` (Royal Blue - classic trust). Let's go with **Teal/Emerald** mix for a fresh bio-tech look.
    - Primary: `#0d9488` (Teal 600)
    - Secondary: `#0f172a` (Slate 900)
    - Background: `#f8fafc` (Slate 50)
    - Surface: `#ffffff` (White)
    - Accent: `#f43f5e` (Rose - for alleles/highlights)

### 2. Typography
- **Headings**: `Inter` or `Plus Jakarta Sans` - Clean, geometric sans-serif for headings.
- **Body**: `Inter` or `system-ui` for high readability.
- **Code/Sequence**: `JetBrains Mono` or `Fira Code` for sequences (crucial for alignment visibility).

### 3. Component Enhancements

#### Hero Section (Header)
- Replace the simple dark header with a modern Hero section.
- Add a subtle background pattern (DNA helix or dot grid).
- Clear title and subtitle.

#### Input Card
- **Glassmorphism effect**: Subtle transparency or soft shadow depth.
- **Inputs**: Larger touch targets, custom focus rings.
- **Example Button**: Make it a secondary "ghost" button or a recognizable link action.
- **Submit Button**: Large, prominent CTA with pulse animation on hover.

#### Results Table
- **Interactive**: Row hover effects.
- **Visual Tags**:
    - Allele A/B: Color-coded badges (e.g., A=Green, G=Blue, T=Red, C=Yellow/Orange).
    - Score: Color scale (Green > Yellow > Red).
- **Copy Function**: Click-to-copy for primer sequences.

#### Loading State
- Replace standard spinner with a DNA-strand animation or a skeleton loader for the table.

## Implementation Steps

### Step 1: Design System Setup
- Import fonts (`Inter`, `JetBrains Mono`).
- Define CSS variables for the color palette.
- Update `style.css` with a reset and base typography.

### Step 2: Component Refactoring
- **App.vue**:
    - Refactor layout to use a centered container with max-width.
    - Apply new Card styling (remove default Element plus borders, use shadow).
    - Customize Element Plus theme variables if needed (or override with CSS).

### Step 3: Result Visualization
- Create a custom cell renderer for `Allele` columns to show badges.
- Add a "Quality Score" visual indicator (e.g., progress bar or colored circle).

### Step 4: Polish
- Add transitions for element appearance (`<TransitionGroup>`).
- Improve error message presentation (Toast vs Alert).

## Mockup Concepts

### Header
```
[ Logo/Icon ] KASP Design Service                             [About]
---------------------------------------------------------------------
"Precision Primer Design for SNP Genotyping"
```

### Table Row
| ID | Allele A | Allele B | Common | Score |
|----|----------|----------|--------|-------|
| 01 | [ACTG..] | [ACTG..] | [ACTG] | ★ 8.5 |
```
```
