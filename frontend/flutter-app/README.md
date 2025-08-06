# Job Seeker Flutter App

A modern, feature-rich mobile application for job seekers and employers built with Flutter.

## 🏗️ Architecture Overview

```
lib/
├── core/                    # Core functionality
│   ├── config/             # App configuration
│   ├── constants/          # App constants
│   ├── router/             # Navigation
│   ├── theme/              # App theming
│   ├── utils/              # Utility functions
│   └── widgets/            # Shared widgets
├── features/               # Feature modules
│   ├── auth/               # Authentication
│   ├── jobs/               # Job management
│   ├── applications/       # Job applications
│   ├── profile/            # User profile
│   ├── search/             # Job search
│   └── notifications/      # Notifications
├── shared/                 # Shared resources
│   ├── models/             # Data models
│   ├── services/           # API services
│   └── providers/          # State providers
└── main.dart              # App entry point
```

## 🚀 Features

### For Job Seekers
- **User Registration & Authentication**: Secure JWT-based authentication
- **Job Search**: Advanced search with filters (location, salary, skills)
- **Job Applications**: Apply to jobs with cover letters and resumes
- **Profile Management**: Complete profile with skills, experience, education
- **Application Tracking**: Track application status and responses
- **Job Recommendations**: AI-powered job recommendations
- **Notifications**: Real-time notifications for job updates

### For Employers
- **Job Posting**: Create and manage job listings
- **Application Management**: Review and manage applications
- **Candidate Search**: Search and filter candidates
- **Company Profile**: Manage company information
- **Analytics**: View job posting performance

## 🛠️ Tech Stack

- **Framework**: Flutter 3.x
- **Language**: Dart
- **State Management**: Riverpod
- **Navigation**: GoRouter
- **HTTP Client**: Dio
- **Local Storage**: Hive + SharedPreferences
- **Authentication**: JWT + Secure Storage
- **UI Components**: Custom design system
- **Theming**: Material 3 with dark/light modes

## 📱 Screens & Navigation

### Authentication Flow
- Splash Screen
- Onboarding
- Login
- Registration
- Forgot Password

### Main App Flow
- Home Dashboard
- Job Search
- Job Details
- Application Form
- Profile
- Applications
- Notifications
- Settings

## 🔧 Setup Instructions

### Prerequisites
- Flutter SDK 3.10.0 or higher
- Dart SDK 3.0.0 or higher
- Android Studio / VS Code
- Android SDK / Xcode (for mobile development)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/3wes22/job-seeker.git
   cd job-seeker/frontend/flutter-app
   ```

2. **Install dependencies**
   ```bash
   flutter pub get
   ```

3. **Run the app**
   ```bash
   flutter run
   ```

### Environment Configuration

Create a `.env` file in the root directory:
```env
API_BASE_URL=http://localhost:8001
ENVIRONMENT=development
```

## 🏗️ Project Structure Details

### Core Module (`lib/core/`)
- **config/**: App configuration, environment settings
- **constants/**: App-wide constants, API endpoints
- **router/**: Navigation configuration with GoRouter
- **theme/**: Material 3 theming with light/dark modes
- **utils/**: Utility functions, helpers, extensions
- **widgets/**: Reusable UI components

### Features Module (`lib/features/`)
Each feature follows a clean architecture pattern:
```
feature/
├── data/
│   ├── datasources/
│   ├── models/
│   └── repositories/
├── domain/
│   ├── entities/
│   ├── repositories/
│   └── usecases/
├── presentation/
│   ├── pages/
│   ├── widgets/
│   └── providers/
└── feature.dart
```

### Shared Module (`lib/shared/`)
- **models/**: Shared data models
- **services/**: API service classes
- **providers/**: Global state providers

## 🎨 Design System

### Colors
- **Primary**: Blue (#2563EB)
- **Secondary**: Green (#10B981)
- **Accent**: Orange (#F59E0B)
- **Error**: Red (#EF4444)
- **Success**: Green (#22C55E)

### Typography
- **Font Family**: Inter
- **Weights**: Regular, Medium, SemiBold, Bold
- **Sizes**: 10px to 32px

### Components
- Custom buttons, cards, inputs
- Consistent spacing and elevation
- Responsive design patterns

## 🔐 Security Features

- JWT token management
- Secure local storage
- Biometric authentication
- Network security
- Input validation

## 📊 State Management

Using Riverpod for:
- **Authentication state**
- **User profile data**
- **Job listings**
- **Application status**
- **Theme preferences**
- **Network connectivity**

## 🧪 Testing

- **Unit Tests**: Business logic and utilities
- **Widget Tests**: UI components
- **Integration Tests**: Feature workflows
- **Golden Tests**: Visual regression testing

## 📦 Build & Deployment

### Android
```bash
flutter build apk --release
flutter build appbundle --release
```

### iOS
```bash
flutter build ios --release
```

## 🔄 API Integration

The app connects to the Django backend services:
- **User Service**: Authentication and user management
- **Job Service**: Job listings and management
- **Application Service**: Job applications
- **Search Service**: Job search functionality
- **Notification Service**: Real-time notifications

## 📈 Performance

- **Lazy loading** for images and data
- **Caching** strategies for API responses
- **Optimized** widget rebuilds
- **Memory management** best practices

## 🐛 Debugging

- **Logging**: Structured logging with different levels
- **Error tracking**: Comprehensive error handling
- **Performance monitoring**: App performance metrics
- **Network debugging**: API request/response logging

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Review the code examples 