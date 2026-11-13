# Quick Theme System Reference

## 🎨 Available Themes

### Blue Themes
- **Blue Light** (Default) - Professional, bright
- **Blue Dark** - Professional, dark

### Green Themes  
- **Green Light** - Fresh, natural
- **Green Dark** - Fresh, dark

### Pink Themes
- **Pink Light** - Modern, trendy
- **Pink Dark** - Modern, dark

## 🚀 Quick Start for Users

1. **Login** to the application
2. **Click Settings** in the menu
3. **Select Theme** from "Theme Preferences" section
4. **Done!** Theme saves automatically

## 👨‍💻 For Developers

### Using Theme in Components

```javascript
import { useTheme } from '../context/ThemeContext'

function MyComponent() {
  const { currentTheme, changeTheme, themes } = useTheme()
  
  return (
    <div>
      <p>Current: {currentTheme}</p>
      <button onClick={() => changeTheme('pink-dark')}>
        Switch to Pink Dark
      </button>
    </div>
  )
}
```

### Using CSS Variables

```css
/* Use variables instead of hardcoded colors */
.my-component {
  background-color: var(--color-background);
  color: var(--color-text);
  border: 1px solid var(--color-border);
}

.my-button {
  background-color: var(--color-primary);
  color: white;
}

.my-button:hover {
  background-color: var(--color-button-hover);
}
```

### Available CSS Variables

```
Color Variables (use in CSS):
--color-primary              Primary brand color
--color-primary-light        Lighter primary
--color-primary-lighter      Even lighter primary
--color-primary-lightest     Very light primary

--color-secondary            Secondary color
--color-secondary-light      Lighter secondary
--color-secondary-lighter    Even lighter secondary

--color-accent              Accent color
--color-background          Main background
--color-background-secondary    Secondary background
--color-background-tertiary     Tertiary background

--color-text                Main text color
--color-text-secondary      Secondary text
--color-text-tertiary       Tertiary text

--color-border              Border color
--color-border-light        Light border

--color-success             Success green
--color-warning             Warning orange
--color-danger              Danger red
--color-info                Info blue

--color-card-bg             Card background
--color-card-border         Card border
--color-input-bg            Input background
--color-input-border        Input border
--color-button-hover        Button hover state
```

## 📊 Theme Values by Type

### Blue Light
```
Primary: #1e40af
Secondary: #0c4a6e  
Accent: #1e40af
Background: #ffffff
Text: #111827
```

### Blue Dark
```
Primary: #3b82f6
Secondary: #38bdf8
Accent: #3b82f6
Background: #0f172a
Text: #f1f5f9
```

### Green Light
```
Primary: #059669
Secondary: #047857
Accent: #10b981
Background: #ffffff
Text: #111827
```

### Green Dark
```
Primary: #10b981
Secondary: #14b8a6
Accent: #10b981
Background: #0f172a
Text: #f1f5f9
```

### Pink Light
```
Primary: #db2777
Secondary: #be185d
Accent: #ec4899
Background: #ffffff
Text: #111827
```

### Pink Dark
```
Primary: #ec4899
Secondary: #f43f5e
Accent: #ec4899
Background: #0f172a
Text: #f1f5f9
```

## 🔧 Adding a New Theme

### Step 1: Add to themes.js
```javascript
// frontend/src/styles/themes.js
export const THEMES = {
  'purple-light': {
    name: 'Purple Light',
    mode: 'light',
    colors: {
      primary: '#7c3aed',
      // ... add all 40+ color variables
    }
  }
}
```

### Step 2: Update app.py
```python
# app.py
allowed_themes = [
  'blue-light', 'blue-dark',
  'green-light', 'green-dark',
  'pink-light', 'pink-dark',
  'purple-light'  # Add new theme
]
```

### Step 3: Update theme groups (optional)
```javascript
// frontend/src/styles/themes.js
export const THEME_GROUPS = {
  blue: ['blue-light', 'blue-dark'],
  green: ['green-light', 'green-dark'],
  pink: ['pink-light', 'pink-dark'],
  purple: ['purple-light', 'purple-dark']  // Add if both modes
}
```

## 🐛 Troubleshooting

### Theme not saving?
- Check browser console for errors
- Verify user is logged in
- Check network tab for API calls

### Colors not updating?
- Hard refresh (Ctrl+F5)
- Clear localStorage
- Check if component uses CSS variables

### Component doesn't have theme colors?
- Update CSS to use `var(--color-*)`
- Add fallback values: `var(--color-text, #333)`
- Check if CSS file is imported

## 📝 Common CSS Patterns

### Text Color
```css
.text-default {
  color: var(--color-text);
}

.text-secondary {
  color: var(--color-text-secondary);
}
```

### Backgrounds
```css
.bg-main {
  background-color: var(--color-background);
}

.bg-card {
  background-color: var(--color-card-bg);
}
```

### Buttons
```css
.btn {
  background-color: var(--color-primary);
  color: white;
}

.btn:hover {
  background-color: var(--color-button-hover);
}
```

### Inputs
```css
input, select {
  background-color: var(--color-input-bg);
  color: var(--color-text);
  border: 1px solid var(--color-input-border);
}
```

### Cards
```css
.card {
  background-color: var(--color-card-bg);
  border: 1px solid var(--color-card-border);
  color: var(--color-text);
}
```

## 🎯 Best Practices

1. **Always use CSS variables** for colors
2. **Provide fallbacks** in var() function
3. **Use semantic names** (--color-danger, not --color-red)
4. **Test in light & dark** modes
5. **Check contrast ratios** for accessibility
6. **Group related colors** for consistency

## 📞 Support

For issues or questions about the theme system:
- Check THEME_SYSTEM_GUIDE.md for detailed docs
- Check IMPLEMENTATION_COMPLETE.md for technical details
- Review component CSS files for examples

---

**Version:** 1.0  
**Last Updated:** 2024  
**Status:** Production Ready ✓
