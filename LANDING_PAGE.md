# Landing Page - AI Applications Portfolio

This is the main landing page for the Chatbots repository, showcasing all applications with an animated, modern interface.

## Features

### Visual Design
- **Animated Hero Section**: Gradient text with fade-in animations
- **Floating Particles**: Dynamic background particle system
- **3D Card Effects**: Mouse-tracking hover effects on app cards
- **Smooth Scrolling**: Seamless navigation between sections
- **Responsive Layout**: Optimized for all screen sizes

### Sections
1. **Hero**: Eye-catching introduction with call-to-action buttons
2. **Applications**: Showcase of available apps with detailed information
3. **About**: Platform mission and values
4. **Contact**: Links to GitHub and other resources

### Applications Showcased

#### Scientific Chatbot
- 8 scientific domains (Chemistry, Physics, Biology, etc.)
- Powered by Claude AI
- Interactive category selection
- Real-time Q&A

#### Pain Management Platform
- 8-week structured curriculum
- AI-powered chatbot with RAG
- Pain tracking and analytics
- Community support features

#### Coming Soon
- Placeholder for future applications
- Innovation focus

## Technical Implementation

### HTML (index.html)
- Semantic HTML5 structure
- Accessibility-friendly
- SEO optimized
- Fast loading

### CSS (styles.css)
- Modern CSS with custom properties
- Gradient backgrounds and animations
- Flexbox and Grid layouts
- Mobile-first responsive design
- Smooth transitions and transforms

### JavaScript (script.js)
- Particle animation system
- Intersection Observer for scroll animations
- Mouse-tracking card effects
- Smooth scroll navigation
- Parallax effects
- Dynamic number animations
- Easter egg (Konami code)

## Animations

### On Load
- Fade-in page transition
- Header slide-down
- Hero text typing effect

### On Scroll
- Fade-up content animations
- Parallax hero section
- Animated statistics counting
- Feature tag stagger animations

### On Hover
- 3D card transforms
- Button scale effects
- Icon glow pulses
- Link underline animations

## Usage

Simply open `index.html` in a web browser, or serve via any HTTP server:

```bash
# Python
python -m http.server 8000

# Node.js
npx serve

# PHP
php -S localhost:8000
```

Then navigate to `http://localhost:8000`

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Mobile)

## Performance

- Lightweight: ~33KB total (HTML + CSS + JS)
- No external dependencies except Google Fonts
- Optimized animations using CSS transforms
- Minimal JavaScript for enhanced interactivity

## Customization

### Adding New Apps
Edit `index.html` and add a new app card in the `.apps-grid` section:

```html
<div class="app-card" data-aos="fade-up" data-aos-delay="600">
    <!-- App card content -->
</div>
```

### Changing Colors
Edit CSS custom properties in `styles.css`:

```css
:root {
    --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --accent-purple: #667eea;
    /* Add more colors */
}
```

### Adding Animations
Add new animations in `script.js` or `styles.css` using the existing patterns.

## Future Enhancements

- [ ] Dark/Light mode toggle
- [ ] Language selection
- [ ] Search functionality
- [ ] App filtering by category
- [ ] Live app status indicators
- [ ] User testimonials section
- [ ] Blog/News section
- [ ] Analytics integration

## Credits

- Built with vanilla HTML, CSS, and JavaScript
- Icons: Emoji (built-in)
- Font: Inter (Google Fonts)
- Inspired by modern web design trends
