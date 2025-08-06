# Frontend Architecture

This directory contains the frontend applications for the Job Seeker Platform.

## Structure

```
frontend/
├── web-app/           # React/Next.js web application
├── flutter-app/       # Flutter mobile application
├── shared/            # Shared components, types, and utilities
└── README.md          # This file
```

## Technologies

### Web Application (React/Next.js)
- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS + Shadcn/ui
- **State Management**: Zustand
- **HTTP Client**: Axios
- **Authentication**: JWT with refresh tokens
- **Form Handling**: React Hook Form + Zod validation

### Mobile Application (Flutter)
- **Framework**: Flutter 3.x
- **Language**: Dart
- **State Management**: Riverpod
- **HTTP Client**: Dio
- **Authentication**: JWT with secure storage
- **UI Components**: Custom design system

## Shared Resources
- **API Types**: TypeScript interfaces shared between web and mobile
- **Constants**: API endpoints, configuration
- **Utilities**: Common helper functions

## Development Setup

### Web App
```bash
cd frontend/web-app
npm install
npm run dev
```

### Flutter App
```bash
cd frontend/flutter-app
flutter pub get
flutter run
```

## API Integration
Both applications connect to the Django backend services:
- User Service: Authentication and user management
- Job Service: Job listings and management
- Application Service: Job applications
- Search Service: Job search functionality
- Notification Service: Real-time notifications 