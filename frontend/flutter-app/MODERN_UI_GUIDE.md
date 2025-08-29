# Modern UI Guide for Job Platform Flutter App

This guide explains how to use the new modern UI components and theme system that follows the design principles from the reference image.

## 🎨 Design Principles

The new UI system is inspired by modern design trends and features:

- **Vibrant Orange Accent Color** (`#FF6B35`) - Primary brand color
- **Soft Shadows & Elevation** - Modern card-based design with subtle shadows
- **Rounded Corners** - Consistent 16px border radius for modern feel
- **Clean Typography** - Improved font weights and spacing
- **Pastel Accent Colors** - For habit cards and category backgrounds
- **Material Design 3** - Latest Material Design principles

## 🎯 Color Palette

### Primary Colors
```dart
AppTheme.primaryColor        // #FF6B35 - Vibrant orange
AppTheme.secondaryColor      // #4ECDC4 - Teal accent
AppTheme.accentColor         // #FFE66D - Warm yellow
```

### Status Colors
```dart
AppTheme.successColor        // #66BB6A - Green success
AppTheme.errorColor          // #FF6B6B - Soft red
AppTheme.warningColor        // #FFA726 - Orange warning
```

### Pastel Colors (for cards)
```dart
AppTheme.pastelGreen         // Light green background
AppTheme.pastelPink          // Light pink background
AppTheme.pastelBlue          // Light blue background
AppTheme.pastelYellow        // Light yellow background
AppTheme.pastelPurple        // Light purple background
```

## 🧩 Modern UI Components

### 1. ModernCard
A versatile card widget with soft shadows and rounded corners.

```dart
ModernCard(
  padding: EdgeInsets.all(20),
  elevation: 8,
  borderRadius: 16,
  onTap: () => print('Card tapped'),
  child: Text('Card content'),
)
```

**Properties:**
- `child` - Required content widget
- `padding` - Internal padding (default: 20px)
- `margin` - External margin (default: 16px horizontal, 8px vertical)
- `backgroundColor` - Custom background color
- `elevation` - Shadow depth (default: 8)
- `borderRadius` - Corner radius (default: 16)
- `onTap` - Tap callback function
- `isSelected` - Shows selected state with border
- `selectedBorderColor` - Custom selected border color

### 2. ModernButton
Modern button with multiple styles and states.

```dart
// Primary button
ModernButton(
  text: 'Get Started',
  onPressed: () => print('Button pressed'),
  icon: Icons.arrow_forward,
  isFullWidth: true,
)

// Outlined button
ModernButton(
  text: 'Learn More',
  onPressed: () => print('Button pressed'),
  isOutlined: true,
  borderColor: Colors.blue,
)

// Loading button
ModernButton(
  text: 'Processing...',
  onPressed: null,
  isLoading: true,
)
```

**Properties:**
- `text` - Button text
- `onPressed` - Callback function
- `isLoading` - Shows loading spinner
- `isOutlined` - Outlined style instead of filled
- `isFullWidth` - Stretches to full width
- `icon` - Optional icon
- `backgroundColor` - Custom background color
- `textColor` - Custom text color
- `borderColor` - Custom border color
- `borderRadius` - Custom corner radius
- `padding` - Custom padding
- `elevation` - Custom shadow depth

### 3. ModernInputField
Modern form input field with clean styling.

```dart
ModernInputField(
  labelText: 'Email Address',
  hintText: 'Enter your email',
  controller: _emailController,
  keyboardType: TextInputType.emailAddress,
  prefixIcon: Icon(Icons.email),
  validator: (value) {
    if (value?.isEmpty ?? true) return 'Email is required';
    return null;
  },
)
```

**Properties:**
- `labelText` - Field label above input
- `hintText` - Placeholder text
- `controller` - Text editing controller
- `keyboardType` - Input type (email, password, etc.)
- `obscureText` - Hide text (for passwords)
- `prefixIcon` - Icon before input
- `suffixIcon` - Icon after input
- `validator` - Form validation function
- `enabled` - Enable/disable field
- `maxLines` - Number of text lines
- `borderRadius` - Custom corner radius
- `borderColor` - Custom border color
- `focusedBorderColor` - Focus state border color

### 4. ModernSearchField
Specialized search input with search icon and clear button.

```dart
ModernSearchField(
  hintText: 'Search jobs, companies...',
  controller: _searchController,
  onChanged: (value) => print('Search: $value'),
  onClear: () => _searchController.clear(),
  onSearch: () => performSearch(),
)
```

**Properties:**
- `hintText` - Search placeholder
- `controller` - Text controller
- `onChanged` - Text change callback
- `onClear` - Clear button callback
- `onSearch` - Search button callback
- `showClearButton` - Show/hide clear button
- `showSearchButton` - Show/hide search button
- `borderRadius` - Custom corner radius

### 5. ModernDropdownField
Modern dropdown/select field.

```dart
ModernDropdownField<String>(
  labelText: 'Job Type',
  hintText: 'Select job type',
  value: _selectedJobType,
  items: [
    DropdownMenuItem(value: 'full_time', child: Text('Full Time')),
    DropdownMenuItem(value: 'part_time', child: Text('Part Time')),
  ],
  onChanged: (value) => setState(() => _selectedJobType = value),
)
```

**Properties:**
- `labelText` - Field label
- `hintText` - Placeholder text
- `value` - Selected value
- `items` - List of dropdown items
- `onChanged` - Selection change callback
- `validator` - Validation function
- `enabled` - Enable/disable field
- `isExpanded` - Stretch to full width

### 6. ModernIconButton
Modern icon button with shadow and rounded corners.

```dart
ModernIconButton(
  icon: Icons.favorite,
  onPressed: () => print('Button pressed'),
  backgroundColor: Colors.red,
  iconColor: Colors.white,
  size: 56,
)
```

**Properties:**
- `icon` - Icon to display
- `onPressed` - Tap callback
- `backgroundColor` - Custom background
- `iconColor` - Custom icon color
- `size` - Button dimensions
- `iconSize` - Icon size
- `borderRadius` - Corner radius
- `elevation` - Shadow depth

### 7. ModernFloatingActionButton
Modern floating action button.

```dart
ModernFloatingActionButton(
  icon: Icons.add,
  onPressed: () => print('FAB pressed'),
  backgroundColor: AppTheme.primaryColor,
  tooltip: 'Add new item',
)
```

**Properties:**
- `icon` - Icon to display
- `onPressed` - Tap callback
- `backgroundColor` - Custom background
- `iconColor` - Custom icon color
- `size` - Button dimensions
- `iconSize` - Icon size
- `tooltip` - Tooltip text
- `heroTag` - Hero animation tag

### 8. ModernChipButton
Modern chip/tag button for filters and selections.

```dart
ModernChipButton(
  label: 'Remote',
  isSelected: _isRemoteSelected,
  onPressed: () => setState(() => _isRemoteSelected = !_isRemoteSelected),
  icon: Icons.home_work,
)
```

**Properties:**
- `label` - Chip text
- `onPressed` - Tap callback
- `isSelected` - Selected state
- `icon` - Optional icon
- `backgroundColor` - Custom background
- `selectedColor` - Selected state color
- `textColor` - Custom text color
- `borderRadius` - Corner radius

## 🎨 Specialized Card Components

### ModernHabitCard
For habit selection interfaces (inspired by reference image).

```dart
ModernHabitCard(
  title: 'Work Out',
  icon: Icons.fitness_center,
  isSelected: _selectedHabits.contains('workout'),
  onTap: () => toggleHabit('workout'),
  backgroundColor: AppTheme.pastelGreen,
)
```

### ModernNotificationCard
For notification displays.

```dart
ModernNotificationCard(
  message: 'Time to read your book!',
  icon: Icons.book,
  onTap: () => openSettings(),
)
```

### ModernDateCard
For date selection interfaces.

```dart
ModernDateCard(
  day: 'Mon',
  date: '15',
  isSelected: _selectedDate == '15',
  onTap: () => selectDate('15'),
)
```

### ModernHabitListItem
For habit list items with completion status.

```dart
ModernHabitListItem(
  title: 'Morning Run',
  subtitle: '6:00 AM for 5km',
  icon: Icons.directions_run,
  isCompleted: true,
  iconBackgroundColor: AppTheme.pastelPink,
)
```

## 🌓 Theme System

### Light Theme
- Clean white backgrounds
- Dark text for readability
- Subtle shadows and borders
- Vibrant orange accents

### Dark Theme
- Deep dark backgrounds
- Light text for contrast
- Enhanced shadows
- Same vibrant orange accents

### Using Theme Colors
```dart
// Access theme colors
final isDark = Theme.of(context).brightness == Brightness.dark;
final backgroundColor = isDark ? AppTheme.darkBackground : AppTheme.lightBackground;
final textColor = isDark ? AppTheme.darkOnSurface : AppTheme.lightOnSurface;

// Use in widgets
Container(
  color: backgroundColor,
  child: Text(
    'Hello World',
    style: TextStyle(color: textColor),
  ),
)
```

## 📱 Example Implementation

### Modern Login Page
See `lib/features/auth/presentation/pages/modern_login_page.dart` for a complete example of a modern login interface.

### Modern Job Search Page
See `lib/features/jobs/presentation/pages/modern_job_search_page.dart` for a complete example of a modern job search interface.

## 🔧 Migration Guide

### From Old Theme to New Theme
1. **Replace old color constants:**
   ```dart
   // Old
   Colors.blue
   
   // New
   AppTheme.primaryColor
   ```

2. **Replace old buttons:**
   ```dart
   // Old
   ElevatedButton(
     child: Text('Login'),
     onPressed: _handleLogin,
   )
   
   // New
   ModernButton(
     text: 'Login',
     onPressed: _handleLogin,
     isFullWidth: true,
   )
   ```

3. **Replace old input fields:**
   ```dart
   // Old
   TextFormField(
     decoration: InputDecoration(
       labelText: 'Email',
       border: OutlineInputBorder(),
     ),
   )
   
   // New
   ModernInputField(
     labelText: 'Email',
     hintText: 'Enter your email',
   )
   ```

4. **Replace old cards:**
   ```dart
   // Old
   Card(
     child: Padding(
       padding: EdgeInsets.all(16),
       child: Text('Content'),
     ),
   )
   
   // New
   ModernCard(
     padding: EdgeInsets.all(16),
     child: Text('Content'),
   )
   ```

## 🎯 Best Practices

1. **Consistent Spacing**: Use multiples of 8px (8, 16, 24, 32, 48, 64)
2. **Elevation Hierarchy**: Use elevation 4 for buttons, 8 for cards, 12 for selected items
3. **Color Usage**: Use primary color sparingly for CTAs and important elements
4. **Typography**: Use theme text styles for consistency
5. **Responsive Design**: Test on different screen sizes
6. **Accessibility**: Ensure proper contrast ratios and touch targets

## 🚀 Future Enhancements

- Custom icon sets for specific use cases
- Animation support for state transitions
- Advanced theming with CSS-like variables
- Component variants (small, medium, large)
- Accessibility improvements
- Performance optimizations

## 📚 Additional Resources

- [Material Design 3 Guidelines](https://m3.material.io/)
- [Flutter Widget Catalog](https://docs.flutter.dev/development/ui/widgets)
- [Flutter Theme Guide](https://docs.flutter.dev/cookbook/design/themes)

---

**Note**: All existing backend logic and integrations are preserved. This modernization only affects the UI layer and user experience.
