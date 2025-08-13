# Job Platform Flutter App

A comprehensive Flutter application built with Clean Architecture that integrates seamlessly with the Job Platform microservices backend.

## 🏗️ Architecture

This app follows **Clean Architecture** principles with the following layers:

- **Presentation Layer**: UI widgets, screens, and state management (Riverpod)
- **Domain Layer**: Business logic, entities, and use cases
- **Data Layer**: API clients, repositories, and local storage

### Project Structure

```
lib/
├── core/                           # Core app functionality
│   ├── config/                     # App configuration
│   ├── di/                         # Dependency injection
│   ├── network/                    # HTTP client and interceptors
│   ├── router/                     # Navigation and routing
│   ├── storage/                    # Local and secure storage
│   ├── theme/                      # App theming
│   └── utils/                      # Utility classes
├── features/                       # Feature modules
│   ├── auth/                       # Authentication
│   │   ├── data/                   # Data layer
│   │   ├── domain/                 # Domain layer
│   │   └── presentation/           # UI layer
│   ├── jobs/                       # Job management
│   ├── search/                     # Job search
│   ├── applications/               # Job applications
│   ├── profile/                    # User profile
│   ├── notifications/              # Notifications
│   └── home/                       # Home screen
└── shared/                         # Shared components
    ├── widgets/                    # Reusable widgets
    ├── models/                     # Shared models
    └── constants/                  # App constants
```

## 🚀 Getting Started

### Prerequisites

- Flutter SDK (3.10.0 or higher)
- Dart SDK (3.0.0 or higher)
- Android Studio / VS Code
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd job-platform-app
   ```

2. **Install dependencies**
   ```bash
   flutter pub get
   ```

3. **Generate code**
   ```bash
   flutter packages pub run build_runner build
   ```

4. **Run the app**
   ```bash
   flutter run
   ```

## 🔧 Configuration

### Environment Setup

The app automatically loads configuration from the backend config API. You can override default values by setting environment variables:

```bash
export USER_SERVICE_URL=http://localhost:8001
export JOB_SERVICE_URL=http://localhost:8002
export APPLICATION_SERVICE_URL=http://localhost:8003
export ANALYTICS_SERVICE_URL=http://localhost:8004
export NOTIFICATION_SERVICE_URL=http://localhost:8005
export SEARCH_SERVICE_URL=http://localhost:8006
```

### Feature Flags

The app supports dynamic feature flags loaded from the backend:

- `real_time_notifications`: Enable WebSocket notifications
- `advanced_search`: Enable advanced search filters
- `analytics`: Enable analytics tracking

## 📱 Features

### Authentication
- User registration and login
- JWT token management
- Secure token storage
- Automatic token refresh

### Job Management
- Browse job listings
- Job search and filtering
- Job details and application
- Company information

### User Profile
- Profile management
- Application history
- Saved jobs
- Preferences

### Real-time Features
- Push notifications
- WebSocket support
- Live updates

## 🛠️ Development

### Code Generation

This project uses several code generation tools:

- **Retrofit**: Generate API service classes
- **JSON Serializable**: Generate JSON serialization code
- **Riverpod Generator**: Generate provider code

To regenerate code after changes:

```bash
# Clean and rebuild
flutter packages pub run build_runner clean
flutter packages pub run build_runner build --delete-conflicting-outputs

# Watch for changes (development)
flutter packages pub run build_runner watch
```

### Adding New Microservices

1. **Create API service interface** in `lib/features/[feature]/data/api/`
2. **Add service URL** to `lib/core/config/app_config.dart`
3. **Generate API client** using build_runner
4. **Create repository** in `lib/features/[feature]/data/repositories/`
5. **Add to dependency injection** in `lib/core/di/providers.dart`

Example:
```dart
// 1. Create API interface
@RestApi()
abstract class NewServiceApi {
  factory NewServiceApi(Dio dio, {String baseUrl}) = _NewServiceApi;
  
  @GET('/api/endpoint')
  Future<List<DataModel>> getData();
}

// 2. Add to config
static String _newServiceUrl = 'http://localhost:8007';

// 3. Generate code
flutter packages pub run build_runner build

// 4. Create repository
class NewServiceRepository {
  final NewServiceApi _api;
  
  NewServiceRepository(this._api);
  
  Future<List<DataModel>> getData() => _api.getData();
}

// 5. Add to providers
@riverpod
NewServiceRepository newServiceRepository(NewServiceRepositoryRef ref) {
  final api = NewServiceApi(ref.watch(dioClientProvider).getDioForService('new'));
  return NewServiceRepository(api);
}
```

### State Management

The app uses **Riverpod** for state management. Key concepts:

- **Providers**: Define dependencies and state
- **Notifiers**: Manage state changes
- **ConsumerWidget**: Access providers in UI

Example:
```dart
class JobsNotifier extends StateNotifier<AsyncValue<List<Job>>> {
  final JobsRepository _repository;
  
  JobsNotifier(this._repository) : super(const AsyncValue.loading());
  
  Future<void> fetchJobs() async {
    state = const AsyncValue.loading();
    try {
      final jobs = await _repository.getJobs();
      state = AsyncValue.data(jobs);
    } catch (error, stackTrace) {
      state = AsyncValue.error(error, stackTrace);
    }
  }
}

@riverpod
class Jobs extends _$Jobs {
  @override
  Future<List<Job>> build() async {
    return ref.watch(jobsRepositoryProvider).getJobs();
  }
  
  Future<void> refresh() async {
    ref.invalidateSelf();
  }
}
```

### Testing

The project includes comprehensive testing setup:

```bash
# Unit tests
flutter test

# Integration tests
flutter test integration_test/

# Coverage report
flutter test --coverage
genhtml coverage/lcov.info -o coverage/html
```

## 📦 Dependencies

### Core Dependencies
- **flutter_riverpod**: State management
- **dio**: HTTP client
- **retrofit**: API client generation
- **json_annotation**: JSON serialization
- **go_router**: Navigation
- **flutter_secure_storage**: Secure storage
- **shared_preferences**: Local storage

### Development Dependencies
- **build_runner**: Code generation
- **retrofit_generator**: Retrofit code generation
- **json_serializable**: JSON code generation
- **riverpod_generator**: Riverpod code generation
- **mockito**: Testing mocks

## 🔐 Security

- JWT tokens stored in secure storage
- HTTPS enforced in production
- Input validation and sanitization
- Secure API communication

## 📊 Performance

- Lazy loading of data
- Efficient state management
- Optimized image loading
- Minimal network requests

## 🚀 Deployment

### Android
```bash
flutter build apk --release
flutter build appbundle --release
```

### iOS
```bash
flutter build ios --release
```

### Web
```bash
flutter build web --release
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:

- Create an issue in the repository
- Check the documentation
- Review the code examples

## 🔄 Updates

To update dependencies:

```bash
flutter pub upgrade
flutter packages pub run build_runner build --delete-conflicting-outputs
```

## 📝 TODO

- [ ] Implement actual API integration
- [ ] Add comprehensive error handling
- [ ] Implement offline support
- [ ] Add analytics tracking
- [ ] Implement push notifications
- [ ] Add comprehensive testing
- [ ] Performance optimization
- [ ] Accessibility improvements
- [ ] Internationalization
- [ ] Dark mode support

## 🎯 Roadmap

### Phase 1: Core Features ✅
- [x] Project structure setup
- [x] Authentication system
- [x] Basic navigation
- [x] Theme system

### Phase 2: Job Management 🚧
- [ ] Job listing
- [ ] Job search
- [ ] Job details
- [ ] Application system

### Phase 3: Advanced Features 📋
- [ ] Real-time notifications
- [ ] Advanced search
- [ ] Analytics dashboard
- [ ] Offline support

### Phase 4: Polish & Optimization 🎨
- [ ] Performance optimization
- [ ] UI/UX improvements
- [ ] Comprehensive testing
- [ ] Documentation 