# Responsive Drawer Menu Implementation Guide

## Overview
Your portfolio now includes a responsive drawer navigation system that:
- Shows horizontal navigation on desktop (screens > 768px)
- Shows a hamburger menu icon on mobile (screens ≤ 768px)
- Slides in from the right on mobile devices
- Uses vanilla JavaScript (no frameworks needed)

## What Was Added

### 1. HTML Structure (in `index.html`)
```html
<nav>
    <!-- Hamburger Menu Button -->
    <button class="menu-toggle" aria-label="Toggle navigation menu">
        <span class="hamburger"></span>
        <span class="hamburger"></span>
        <span class="hamburger"></span>
    </button>

    <!-- Navigation Menu -->
    <ul class="nav-menu">
        <li><a href="index.html">Home</a></li>
        <!-- ... other links ... -->
    </ul>

    <!-- Overlay -->
    <div class="nav-overlay"></div>
</nav>
```

### 2. CSS Styling (in `css/styles.css`)
- Hamburger button with animated icon
- Drawer menu that slides from right
- Semi-transparent overlay
- Responsive breakpoint at 768px

### 3. JavaScript (in `js/drawer-menu.js`)
- Toggle menu open/close
- Close on overlay click
- Close on link click
- Close on ESC key
- Auto-close when resizing to desktop

## How to Add to Other Lab Pages

To add the drawer menu to your other portfolio pages (lab02.html, lab03.html, etc.):

### Step 1: Update the Navigation HTML

Replace the existing `<nav>` section with:

```html
<nav>
    <!-- Hamburger Menu Button (visible on mobile) -->
    <button class="menu-toggle" aria-label="Toggle navigation menu">
        <span class="hamburger"></span>
        <span class="hamburger"></span>
        <span class="hamburger"></span>
    </button>

    <!-- Navigation Menu -->
    <ul class="nav-menu">
        <li><a href="index.html">Home</a></li>
        <li><a href="lab02.html">AI Evaluation</a></li>
        <li><a href="lab03.html">Tufte Critique</a></li>
        <li><a href="lab04.html">Tableau Viz</a></li>
        <li><a href="lab05.html">Lab 5</a></li>
        <li><a href="lab06.html">Hometown Map</a></li>
    </ul>

    <!-- Overlay for drawer (visible when menu is open on mobile) -->
    <div class="nav-overlay"></div>
</nav>
```

### Step 2: Add JavaScript Reference

Add this line before the closing `</body>` tag:

```html
    <script src="js/drawer-menu.js"></script>
</body>
```

### Step 3: Ensure CSS is Linked

Make sure your page links to the stylesheet:

```html
<link rel="stylesheet" href="css/styles.css">
```

## Features

### Desktop View (> 768px)
- Horizontal navigation bar
- Hamburger button is hidden
- Links display inline

### Mobile View (≤ 768px)
- Hamburger icon (☰) appears on left
- Clicking opens drawer from right
- Semi-transparent overlay covers content
- Menu slides in smoothly
- Clicking overlay or link closes drawer
- ESC key closes drawer

### Accessibility
- ARIA label on button for screen readers
- Keyboard navigation support (ESC to close)
- Focus management
- Proper semantic HTML

## Customization

### Change Drawer Width
In `css/styles.css`, find:
```css
.nav-menu {
    width: 280px;  /* Change this value */
}
```

### Change Animation Speed
Find `transition` properties and adjust timing:
```css
transition: right 0.3s ease;  /* Change 0.3s to your preference */
```

### Change Breakpoint
In the media query, change `768px` to your preferred breakpoint:
```css
@media (max-width: 768px) {
    /* Mobile styles */
}
```

### Change Colors
The drawer uses your existing color scheme:
- Background: `#277391` (your nav blue)
- Hover: `rgba(255, 255, 255, 0.1)`
- Overlay: `rgba(0, 0, 0, 0.5)`

## Testing

To test the responsive drawer:

1. **Desktop View**: Open in browser at full width - should see horizontal nav
2. **Mobile View**: Resize browser to < 768px width - should see hamburger icon
3. **Click Hamburger**: Drawer should slide in from right
4. **Click Overlay**: Drawer should close
5. **Click Link**: Drawer should close and navigate
6. **Press ESC**: Drawer should close
7. **Resize Window**: Drawer should auto-close if resizing to desktop view

## Browser Support
- Chrome/Edge: ✅ Full support
- Firefox: ✅ Full support
- Safari: ✅ Full support
- Mobile browsers: ✅ Full support

## Notes
- No external libraries required (vanilla JavaScript)
- Fully responsive
- Smooth animations
- Accessible
- Works on all modern browsers
