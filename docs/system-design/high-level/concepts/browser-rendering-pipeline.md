# Browser Rendering Pipeline

## Theory

### What is The Browser Rendering Pipeline?

The browser rendering pipeline is the sequence of steps a browser takes to convert HTML, CSS, and JavaScript into the pixels you see on screen. Understanding this pipeline is essential for building performant web applications.

**The Pipeline (Critical Rendering Path):**

```
1. Parse HTML → DOM Tree
2. Parse CSS → CSSOM Tree
3. Combine → Render Tree
4. Layout (Reflow) → Calculate positions and sizes
5. Paint → Fill in pixels (colors, borders, shadows)
6. Composite → Layer composition and display

  HTML ──→ DOM ──┐
                 ├──→ Render Tree ──→ Layout ──→ Paint ──→ Composite ──→ Pixels
  CSS ───→ CSSOM ┘
                ↑
            JavaScript (can modify DOM/CSSOM at any step)
```

### Step-by-Step Breakdown

**1. HTML Parsing → DOM (Document Object Model)**
The browser reads the HTML byte stream and converts it into a tree of nodes:
```
<html>
  <body>
    <h1>Hello</h1>
    <p>World</p>
  </body>
</html>

Becomes:
  Document
   └─ html
       └─ body
           ├─ h1 → "Hello"
           └─ p  → "World"
```
- Parser works **top-to-bottom**
- Encountering a `<script>` tag **blocks** parsing (unless `async` or `defer`)
- Encountering `<link rel="stylesheet">` **blocks rendering** (not parsing)

**2. CSS Parsing → CSSOM (CSS Object Model)**
CSS is parsed into its own tree. Every node inherits styles from its parent:
```
body { font-size: 16px; }
h1 { color: blue; }

CSSOM:
  body (font-size: 16px)
   ├─ h1 (color: blue, font-size: 16px ← inherited)
   └─ p  (font-size: 16px ← inherited)
```
- CSS is **render-blocking** — the browser won't paint until CSSOM is complete
- Reason: Without CSS, the page would flash unstyled content (FOUC)

**3. Render Tree Construction**
Combines DOM and CSSOM. Only includes **visible** elements:
```
DOM node <h1> + CSSOM style {color: blue} → Render Tree node

Excluded from Render Tree:
  - <head>, <script>, <meta> (not visual)
  - Elements with display: none
  - Hidden elements
```

**4. Layout (Reflow)**
Calculates the exact position and size of every element in pixels:
```
Viewport: 1200px wide

<div style="width: 50%">        → 600px wide
  <p style="font-size: 16px">   → Calculate line breaks, height
```
- Layout is **expensive** — changing one element can trigger layout for its children and siblings
- Avoid triggering layout repeatedly (layout thrashing)

**5. Paint**
Fills in the actual pixels — colors, text, images, borders, shadows:
```
For each Render Tree node:
  → Draw background color
  → Draw border
  → Draw text
  → Draw shadows, etc.
```
- Paint order follows **stacking context** (z-index, position)
- Modern browsers split the page into **layers** for efficiency

**6. Composite**
Layers are combined (composited) in the correct order and sent to the GPU for display:
```
Layer 1: Background
Layer 2: Main content
Layer 3: Fixed header
Layer 4: Modal overlay
  → GPU composites layers → Screen pixels
```
- Compositing is the **cheapest** operation (GPU-accelerated)
- Animations using `transform` and `opacity` only trigger compositing (no layout/paint)

### Performance Implications

**What Triggers What:**
```
Change            → Triggers
─────────────────────────────
width, height     → Layout → Paint → Composite (most expensive)
color, background → Paint → Composite
transform, opacity→ Composite only (cheapest)
```

**Optimization Tips:**
- **Minimize render-blocking resources**: Use `async`/`defer` for scripts, inline critical CSS
- **Avoid layout thrashing**: Don't read layout properties (offsetHeight) between writes
- **Use `transform` for animations**: Avoids layout and paint; GPU-accelerated
- **Reduce DOM size**: Fewer nodes = faster layout
- **Use `will-change`**: Hint the browser to pre-promote elements to their own layer
- **Lazy load images/iframes**: Don't load off-screen resources during initial render

### The Critical Rendering Path

The **Critical Rendering Path (CRP)** is the minimum set of steps to render the first meaningful paint:

```
Optimized CRP:
  1. Minimize critical resources (HTML, CSS needed for above-the-fold)
  2. Minimize critical bytes (compress, minify)
  3. Minimize critical path length (reduce round trips)

Metrics:
  FCP (First Contentful Paint): When first text/image appears
  LCP (Largest Contentful Paint): When main content is visible
  CLS (Cumulative Layout Shift): Visual stability
  INP (Interaction to Next Paint): Responsiveness
```
