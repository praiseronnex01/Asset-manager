# Color Theme System - Documentation

## Overview
The Asset Management application now includes a comprehensive color theme system with multiple themes and dark mode support.

## Available Themes

### Blue Themes (Default)
- **Blue Light**: Professional blue theme with light background
- **Blue Dark**: Professional blue theme with dark background

### Green Themes
- **Green Light**: Nature-inspired green theme with light background
- **Green Dark**: Nature-inspired green theme with dark background

### Pink Themes
- **Pink Light**: Modern pink theme with light background
- **Pink Dark**: Modern pink theme with dark background

## Architecture

### Frontend Components

#### 1. ThemeContext (src/context/ThemeContext.jsx)
Provides global theme management through React Context API.

**Features:**
- Manages current theme state
- Persists theme preference to localStorage
- Syncs with backend database
- Provides `useTheme()` hook for components

**Usage:**
```javascript
import { useTheme } from '../context/ThemeContext'

function MyComponent() {
  const { currentTheme, changeTheme, themes } = useTheme()
  
  // Change theme
  changeTheme('green-dark')
}
```

#### 2. Theme Configuration (src/styles/themes.js)
Defines all theme color palettes.

**Structure:**
```javascript
export const THEMES = {
  'blue-light': {
    name: 'Blue Light',
    mode: 'light',
    colors: {
      primary: '#1e40af',
      background: '#ffffff',
      // ... all color variables
    }
  },
  // ... other themes
}
```

**Color Variables Available:**
- Primary colors: `primary`, `primary-light`, `primary-lighter`, `primary-lightest`
- Secondary colors: `secondary`, `secondary-light`, `secondary-lighter`
- Accent color
- Background colors: `background`, `background-secondary`, `background-tertiary`
- Text colors: `text`, `text-secondary`, `text-tertiary`
- Utility colors: `border`, `border-light`, `success`, `warning`, `danger`, `info`
- Component colors: `card-bg`, `card-border`, `input-bg`, `input-border`, `button-hover`

#### 3. SettingsPage (src/pages/SettingsPage.jsx)
Updated to display theme selector with visual previews.

**Features:**
- Theme cards grouped by color family
- Visual color previews
- Active theme indicator
- Instant theme switching

#### 4. CSS Variables (src/index.css)
Root CSS variables that get updated based on selected theme.

```css
:root {
  --color-primary: #1e40af;
  --color-background: #ffffff;
  /* ... all variables */
}
```

### Backend Integration

#### API Endpoints

**1. Check Authentication (GET /api/check-auth)**
```
GET /api/check-auth
Response: { authenticated: boolean, user_id?: number }
```

**2. Get User Theme (GET /api/user-theme)**
```
GET /api/user-theme
Requires: Authentication
Response: { theme: string }
```

**3. Set User Theme (POST /api/user-theme)**
```
POST /api/user-theme
Content-Type: application/json
Body: { theme: string }
Requires: Authentication
Response: { success: boolean, theme: string }
```

**Allowed Themes:**
- blue-light
- blue-dark
- green-light
- green-dark
- pink-light
- pink-dark

#### Database
User theme preference is stored in the `users` table:
```sql
ALTER TABLE users ADD COLUMN theme TEXT DEFAULT 'blue-light';
```

## Usage

### For End Users

1. Navigate to Settings page
2. Scroll to "Theme Preferences" section
3. Select desired theme from available options
4. Theme is applied immediately and saved to database

### For Developers

#### Applying Themes to Components
Use CSS variables instead of hardcoded colors:

```css
/* Before (hardcoded) */
.card {
  background-color: #ffffff;
  color: #333;
  border: 1px solid #ddd;
}

/* After (theme-aware) */
.card {
  background-color: var(--color-card-bg, #ffffff);
  color: var(--color-text, #333);
  border: 1px solid var(--color-card-border, #ddd);
}
```

#### Creating Custom Themes
To add a new theme, add it to `src/styles/themes.js`:

```javascript
export const THEMES = {
  'your-theme-name': {
    name: 'Display Name',
    mode: 'light' | 'dark',
    colors: {
      primary: '#...',
      background: '#...',
      // ... all required color variables
    }
  }
}
```

Then update allowed themes in `app.py`:
```python
allowed_themes = [
  'blue-light', 'blue-dark',
  'green-light', 'green-dark',
  'pink-light', 'pink-dark',
  'your-theme-name'  # Add here
]
```

## Technical Details

### Theme Initialization Flow
1. App mounts with ThemeProvider wrapper
2. ThemeContext checks localStorage for saved theme
3. If authenticated, fetches latest theme from backend
4. CSS variables applied to document root
5. All components render with current theme colors

### Performance Considerations
- CSS variables update instantly on theme change
- localStorage provides quick theme loading on app startup
- No rerendering of entire component tree needed
- Smooth transitions enabled with `transition: background-color 0.3s ease`

### Browser Support
- Modern browsers with CSS custom properties support (Chrome, Firefox, Safari, Edge)
- Fallback values provided for all CSS variables using `var(color, fallback)`

## Styling Best Practices

1. **Always use CSS variables** for colors instead of hardcoded values
2. **Provide fallback values** in var() for older browsers
3. **Test in both light and dark modes** when creating new components
4. **Use semantic color names** (e.g., --color-danger, not --color-red)
5. **Group related colors** (primary, secondary, accent) for consistency

## File Changes Summary

### New Files
- `frontend/src/context/ThemeContext.jsx`
- `frontend/src/styles/themes.js`

### Modified Files
- `frontend/src/App.jsx` - Added ThemeProvider wrapper
- `frontend/src/pages/SettingsPage.jsx` - Expanded with theme selector UI
- `frontend/src/pages/SettingsPage.css` - Added theme card styles
- `frontend/src/index.css` - Added CSS variables
- `frontend/src/App.css` - Updated to use CSS variables
- `app.py` - Added theme API endpoints

## Future Enhancements

1. System preference detection (prefers-color-scheme media query)
2. Time-based theme switching (light during day, dark at night)
3. Custom theme builder UI
4. Import/export theme configurations
5. Per-component theme overrides
6. Accessibility contrast verification

## Troubleshooting

### Theme not persisting after refresh
- Clear browser cache and localStorage
- Check database update query success
- Verify user is authenticated

### Colors not updating
- Hard refresh browser (Ctrl+F5)
- Check if component is using CSS variables
- Verify theme name is in allowed themes list

### Theme not loading on startup
- Check browser console for errors
- Verify localStorage access is enabled
- Check backend connectivity

## Support
For issues or feature requests, contact the development team.
