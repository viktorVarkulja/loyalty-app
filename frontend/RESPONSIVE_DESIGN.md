# Responsive Design Guide

This application follows a **mobile-first** approach with responsive breakpoints.

## Breakpoints

- **Mobile**: < 640px (default, base styles)
- **Tablet**: 640px - 1024px
- **Desktop**: > 1024px

## Design Principles

### 1. Mobile-First Approach
All base styles are designed for mobile devices first, then enhanced for larger screens using media queries.

### 2. Touch-Friendly
- Minimum tap target size: 44x44 pixels
- Adequate spacing between interactive elements
- No hover-dependent functionality

### 3. Progressive Enhancement
- Core functionality works on all devices
- Enhanced features for capable devices
- Graceful degradation for older browsers

## Responsive Features

### Layout
- **Mobile**: Single column, full-width cards
- **Tablet**: 2-column grids where appropriate
- **Desktop**: 3-4 column grids, max-width containers

### Navigation
- **Mobile/Tablet**: Bottom navigation bar (fixed)
- **Desktop**: Bottom navigation centered with max-width
- Navigation adapts to safe-area-insets for notched devices

### Typography
- **Mobile**: Base font sizes (14-16px body, 24-28px headings)
- **Tablet**: Slightly larger (16-18px body, 28-32px headings)
- **Desktop**: Full size (16-18px body, 32-36px headings)

### Images & Icons
- Optimized for retina displays
- SVG icons scale perfectly on all devices
- Lazy loading for better performance

### Cards & Components
- Flexible padding and spacing
- Adaptive grid layouts
- Responsive modal sizes

## Testing Responsive Design

### Viewports to Test
1. **Mobile**: 375x667 (iPhone SE), 390x844 (iPhone 12/13/14)
2. **Tablet**: 768x1024 (iPad), 810x1080 (iPad Pro)
3. **Desktop**: 1366x768, 1920x1080

### Orientation
- Portrait (primary for mobile/tablet)
- Landscape (optimized for all devices)

### Features to Verify
- [ ] Navigation is accessible on all screen sizes
- [ ] Text is readable without zooming
- [ ] Forms are easy to fill on mobile
- [ ] Tap targets are large enough
- [ ] Images scale appropriately
- [ ] No horizontal scrolling
- [ ] Content adapts to viewport
- [ ] PWA works on all devices

## Browser Support

- Chrome/Edge (last 2 versions)
- Firefox (last 2 versions)
- Safari (last 2 versions)
- iOS Safari (iOS 13+)
- Chrome Android (last 2 versions)

## PWA Specific

### Install Prompt
- Appears on supported browsers
- Dismissible
- Respects user preference

### Offline Capability
- Service worker caches assets
- Network-first for API calls
- Cache-first for static assets

### Safe Areas
The app respects device safe areas:
- Top notch (iPhone X+)
- Bottom home indicator
- Rounded corners

```css
padding: env(safe-area-inset-top) env(safe-area-inset-right)
         env(safe-area-inset-bottom) env(safe-area-inset-left);
```

## Performance Considerations

1. **Images**: Use appropriate sizes, lazy load
2. **Fonts**: System font stack for instant rendering
3. **CSS**: Mobile-first reduces overrides
4. **JS**: Code splitting and lazy loading
5. **Caching**: Service worker for offline

## Accessibility

- Semantic HTML
- ARIA labels where needed
- Keyboard navigation support
- Screen reader friendly
- High contrast for readability
- Touch and pointer device support

## Known Limitations

1. **Desktop Navigation**: Bottom navigation on desktop could be replaced with a sidebar in future versions
2. **Very Small Screens**: Optimized for 320px+ width
3. **Print Styles**: Basic print styles included

## Future Enhancements

- Dark mode support
- Desktop sidebar navigation
- Landscape optimizations for tablets
- Foldable device support
- Advanced PWA features (badges, shortcuts)
