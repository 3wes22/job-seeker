#!/bin/bash

# Job Platform Flutter App Setup Script
# This script helps set up the development environment

set -e

echo "🚀 Setting up Job Platform Flutter App..."

# Check if Flutter is installed
if ! command -v flutter &> /dev/null; then
    echo "❌ Flutter is not installed. Please install Flutter first:"
    echo "   https://flutter.dev/docs/get-started/install"
    exit 1
fi

# Check Flutter version
FLUTTER_VERSION=$(flutter --version | grep -o "Flutter [0-9]\+\.[0-9]\+\.[0-9]\+" | cut -d' ' -f2)
REQUIRED_VERSION="3.10.0"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$FLUTTER_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Flutter version $FLUTTER_VERSION is too old. Required: $REQUIRED_VERSION or higher"
    exit 1
fi

echo "✅ Flutter version $FLUTTER_VERSION detected"

# Get dependencies
echo "📦 Getting Flutter dependencies..."
flutter pub get

# Create necessary directories
echo "📁 Creating project structure..."
mkdir -p lib/features/auth/{data/{api,repositories},domain/{entities,repositories,usecases},presentation/{screens,widgets,providers}}
mkdir -p lib/features/jobs/{data/{api,repositories},domain/{entities,repositories,usecases},presentation/{screens,widgets,providers}}
mkdir -p lib/features/search/{data/{api,repositories},domain/{entities,repositories,usecases},presentation/{screens,widgets,providers}}
mkdir -p lib/features/applications/{data/{api,repositories},domain/{entities,repositories,usecases},presentation/{screens,widgets,providers}}
mkdir -p lib/features/profile/{data/{api,repositories},domain/{entities,repositories,usecases},presentation/{screens,widgets,providers}}
mkdir -p lib/features/notifications/{data/{api,repositories},domain/{entities,repositories,usecases},presentation/{screens,widgets,providers}}
mkdir -p lib/features/home/{data/{api,repositories},domain/{entities,repositories,usecases},presentation/{screens,widgets,providers}}
mkdir -p lib/features/splash/{data/{api,repositories},domain/{entities,repositories,usecases},presentation/{screens,widgets,providers}}
mkdir -p lib/shared/{widgets,models,constants}
mkdir -p assets/{images,icons,config,fonts}
mkdir -p test/{unit,integration,widget}
mkdir -p integration_test

# Create placeholder files to maintain structure
echo "📝 Creating placeholder files..."
touch lib/features/auth/data/api/.gitkeep
touch lib/features/auth/data/repositories/.gitkeep
touch lib/features/auth/domain/entities/.gitkeep
touch lib/features/auth/domain/repositories/.gitkeep
touch lib/features/auth/domain/usecases/.gitkeep
touch lib/features/auth/presentation/screens/.gitkeep
touch lib/features/auth/presentation/widgets/.gitkeep
touch lib/features/auth/presentation/providers/.gitkeep

touch lib/features/jobs/data/api/.gitkeep
touch lib/features/jobs/data/repositories/.gitkeep
touch lib/features/jobs/domain/entities/.gitkeep
touch lib/features/jobs/domain/repositories/.gitkeep
touch lib/features/jobs/domain/usecases/.gitkeep
touch lib/features/jobs/presentation/screens/.gitkeep
touch lib/features/jobs/presentation/widgets/.gitkeep
touch lib/features/jobs/presentation/providers/.gitkeep

touch lib/features/search/data/api/.gitkeep
touch lib/features/search/data/repositories/.gitkeep
touch lib/features/search/domain/entities/.gitkeep
touch lib/features/search/domain/repositories/.gitkeep
touch lib/features/search/domain/usecases/.gitkeep
touch lib/features/search/presentation/screens/.gitkeep
touch lib/features/search/presentation/widgets/.gitkeep
touch lib/features/search/presentation/providers/.gitkeep

touch lib/features/applications/data/api/.gitkeep
touch lib/features/applications/data/repositories/.gitkeep
touch lib/features/applications/domain/entities/.gitkeep
touch lib/features/applications/domain/repositories/.gitkeep
touch lib/features/applications/domain/usecases/.gitkeep
touch lib/features/applications/presentation/screens/.gitkeep
touch lib/features/applications/presentation/widgets/.gitkeep
touch lib/features/applications/presentation/providers/.gitkeep

touch lib/features/profile/data/api/.gitkeep
touch lib/features/profile/data/repositories/.gitkeep
touch lib/features/profile/domain/entities/.gitkeep
touch lib/features/profile/domain/repositories/.gitkeep
touch lib/features/profile/domain/usecases/.gitkeep
touch lib/features/profile/presentation/screens/.gitkeep
touch lib/features/profile/presentation/widgets/.gitkeep
touch lib/features/profile/presentation/providers/.gitkeep

touch lib/features/notifications/data/api/.gitkeep
touch lib/features/notifications/data/repositories/.gitkeep
touch lib/features/notifications/domain/entities/.gitkeep
touch lib/features/notifications/domain/repositories/.gitkeep
touch lib/features/notifications/domain/usecases/.gitkeep
touch lib/features/notifications/presentation/screens/.gitkeep
touch lib/features/notifications/presentation/widgets/.gitkeep
touch lib/features/notifications/presentation/providers/.gitkeep

touch lib/features/home/data/api/.gitkeep
touch lib/features/home/data/repositories/.gitkeep
touch lib/features/home/domain/entities/.gitkeep
touch lib/features/home/domain/repositories/.gitkeep
touch lib/features/home/domain/usecases/.gitkeep
touch lib/features/home/presentation/screens/.gitkeep
touch lib/features/home/presentation/widgets/.gitkeep
touch lib/features/home/presentation/providers/.gitkeep

touch lib/features/splash/data/api/.gitkeep
touch lib/features/splash/data/repositories/.gitkeep
touch lib/features/splash/domain/entities/.gitkeep
touch lib/features/splash/domain/repositories/.gitkeep
touch lib/features/splash/domain/usecases/.gitkeep
touch lib/features/splash/presentation/screens/.gitkeep
touch lib/features/splash/presentation/widgets/.gitkeep
touch lib/features/splash/presentation/providers/.gitkeep

touch lib/shared/widgets/.gitkeep
touch lib/shared/models/.gitkeep
touch lib/shared/constants/.gitkeep

touch assets/images/.gitkeep
touch assets/icons/.gitkeep
touch assets/config/.gitkeep
touch assets/fonts/.gitkeep

touch test/unit/.gitkeep
touch test/integration/.gitkeep
touch test/widget/.gitkeep

# Generate code
echo "🔨 Generating code..."
flutter packages pub run build_runner build --delete-conflicting-outputs

# Run tests to ensure everything is working
echo "🧪 Running tests..."
flutter test

echo "✅ Setup completed successfully!"
echo ""
echo "🎯 Next steps:"
echo "1. Review the project structure in lib/"
echo "2. Check the README.md for development guidelines"
echo "3. Start implementing your features"
echo "4. Run 'flutter run' to start the app"
echo ""
echo "📚 Useful commands:"
echo "  flutter run                    # Run the app"
echo "  flutter test                   # Run tests"
echo "  flutter packages pub run build_runner build --delete-conflicting-outputs  # Generate code"
echo "  flutter packages pub run build_runner watch  # Watch for changes"
echo ""
echo "🚀 Happy coding!" 