---
name: mobile-architect
compatibility: Antigravity, Claude Code, GitHub Copilot
description: iOS/Android and Flutter/React Native dev. Use for mobile application development.
triggers:
  - "mobile app"
  - "iOS"
  - "Android"
  - "React Native"
  - "Flutter"
---

# Mobile Architect Skill

## Identity

You are a mobile architecture specialist focused on building cross-platform and native mobile applications.

## When to Use

- Designing mobile architecture
- Building React Native apps
- Developing Flutter applications
- Native iOS/Android development

## When NOT to Use

- Web-only projects with no native mobile target — use `frontend-architect` instead
- Mobile web (PWA) without native device API needs — use `frontend-architect` with responsive design patterns
- Backend services that power a mobile app — use `backend-architect` or `api-designer` for the server side
- When the existing mobile architecture is established and you only need to add a screen — follow the existing pattern directly

## React Native Architecture

### Project Structure

```
src/
├── components/       # Reusable components
│   ├── Button/
│   ├── Card/
│   └── Input/
├── screens/          # Screen components
│   ├── Home/
│   ├── Profile/
│   └── Settings/
├── navigation/       # Navigation config
│   ├── AppNavigator.tsx
│   └── types.ts
├── services/         # API services
│   ├── api.ts
│   └── auth.ts
├── store/            # State management
│   ├── index.ts
│   └── slices/
├── hooks/            # Custom hooks
├── utils/            # Utilities
└── types/            # TypeScript types
```

### Navigation Setup

```typescript
// navigation/AppNavigator.tsx
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

const Stack = createNativeStackNavigator<RootStackParamList>();

export const AppNavigator = () => {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Home">
        <Stack.Screen
          name="Home"
          component={HomeScreen}
          options={{ title: 'Home' }}
        />
        <Stack.Screen
          name="Profile"
          component={ProfileScreen}
          options={{ title: 'Profile' }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
};
```

## Flutter Architecture

### Project Structure

```
lib/
├── main.dart
├── app/
│   ├── app.dart
│   └── routes/
├── features/
│   ├── auth/
│   │   ├── data/
│   │   ├── domain/
│   │   └── presentation/
│   └── home/
├── core/
│   ├── theme/
│   ├── utils/
│   └── widgets/
└── shared/
    └── models/
```

### Clean Architecture Example

```dart
// domain/entities/user.dart
class User {
  final String id;
  final String name;
  final String email;

  User({required this.id, required this.name, required this.email});
}

// domain/repositories/user_repository.dart
abstract class UserRepository {
  Future<User> getUser(String id);
  Future<void> updateUser(User user);
}

// data/repositories/user_repository_impl.dart
class UserRepositoryImpl implements UserRepository {
  final UserRemoteDataSource remoteDataSource;

  UserRepositoryImpl({required this.remoteDataSource});

  @override
  Future<User> getUser(String id) async {
    return await remoteDataSource.getUser(id);
  }
}

// presentation/bloc/user_bloc.dart
class UserBloc extends Bloc<UserEvent, UserState> {
  final UserRepository repository;

  UserBloc({required this.repository}) : super(UserInitial()) {
    on<LoadUser>(_onLoadUser);
  }

  Future<void> _onLoadUser(LoadUser event, Emitter<UserState> emit) async {
    emit(UserLoading());
    try {
      final user = await repository.getUser(event.id);
      emit(UserLoaded(user));
    } catch (e) {
      emit(UserError(e.toString()));
    }
  }
}
```

## Performance Best Practices

### React Native

```typescript
// Use FlatList for long lists
<FlatList
  data={items}
  renderItem={renderItem}
  keyExtractor={(item) => item.id}
  initialNumToRender={10}
  maxToRenderPerBatch={10}
  windowSize={5}
  removeClippedSubviews={true}
/>

// Memoize components
const Item = memo(({ title }: ItemProps) => (
  <View style={styles.item}>
    <Text>{title}</Text>
  </View>
));

// Optimize images
<Image
  source={{ uri: imageUrl }}
  resizeMode="cover"
  style={styles.image}
/>
```

### Flutter

```dart
// Use ListView.builder for long lists
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) {
    return ItemWidget(item: items[index]);
  },
)

// Use const widgets
const Text('Hello')

// Optimize images with cached_network_image
CachedNetworkImage(
  imageUrl: url,
  placeholder: (context, url) => CircularProgressIndicator(),
  errorWidget: (context, url, error) => Icon(Icons.error),
)
```

## Platform-Specific Code

### React Native

```typescript
import { Platform, StyleSheet } from "react-native";

const styles = StyleSheet.create({
  container: {
    ...Platform.select({
      ios: {
        shadowColor: "#000",
        shadowOffset: { width: 0, height: 2 },
      },
      android: {
        elevation: 4,
      },
    }),
  },
});
```

### Flutter

```dart
import 'dart:io' show Platform;

Widget build(BuildContext context) {
  return Container(
    decoration: Platform.isIOS
      ? BoxDecoration(
          boxShadow: [BoxShadow(color: Colors.black, blurRadius: 4)]
        )
      : null,
  );
}
```

## Tips

- Use platform-specific designs when appropriate
- Optimize for battery and performance
- Test on real devices
- Handle offline scenarios
- Follow platform guidelines

## Anti-Patterns

- Never load a full-resolution image into memory without downsampling because on low-RAM devices the OS kills the process silently and users see a blank screen with no error message.
- Never perform network calls on the main thread because any latency spike freezes the UI, triggering ANR dialogs on Android and watchdog kills on iOS.
- Never store sensitive data in SharedPreferences or NSUserDefaults because these are readable by backup tools and rooted/jailbroken devices without any special permission.
- Never assume background tasks will complete because iOS and Android battery optimisers terminate background work without notification, leaving the app in a partial state.
- Never implement deep link handling without testing cold-start because the navigation stack is not initialised on cold start and the deep link target screen crashes with a null reference.
- Never cache API responses without an expiry strategy because stale data accumulates and users see outdated content after server-side changes with no indication that the data is old.

## Failure Modes

| Failure | Cause | Recovery |
|---|---|---|
| App crashes on low-memory device due to large bitmap loaded into memory | Full-resolution image loaded directly into an `ImageView` or `Image` widget without downsampling or cache eviction | Use `resizeMode="cover"` with explicit dimensions (RN) or `cached_network_image` with `memCacheSize` limit (Flutter); verify with Android Profiler / Instruments that peak memory stays below device limit |
| Deep link fails on cold start because navigation stack not initialized | Deep link URL arrives before the navigation container is mounted, so the route is dropped silently | Handle deep links in the `NavigationContainer` `linking` config (RN) or `GoRouter` `redirect` (Flutter); add a cold-start test that opens the app via deep link and confirms the correct screen is shown |
| Background task killed by OS battery optimizer, silently dropping work | Long-running background task not registered as a foreground service (Android) or Background App Refresh disabled (iOS) | Use `react-native-background-fetch` or WorkManager (Android) / BGTaskScheduler (iOS) for deferrable work; confirm task completion in device logs under battery saver mode |
| Offline sync conflict not resolved, corrupting local data store | Two writes to the same record (one offline, one from server) applied with last-write-wins and no conflict resolution strategy | Implement vector-clock or timestamp-based conflict resolution; add an integration test that writes offline, syncs, and asserts the correct merged state |
| Push notification delivery fails on iOS because APNs cert expired | APNs production certificate has a 1-year expiry and was not renewed; notifications silently drop | Rotate the APNs certificate or switch to APNs token-based authentication (no expiry); add a calendar reminder or automated alert 30 days before cert expiry |

## Self-Verification Checklist

- [ ] Build exits 0 on the target platform: `npx react-native run-ios --configuration Release` or `flutter build apk` exits 0
- [ ] App launches without crash on the lowest supported OS version (verified on emulator or physical device — not just latest OS)
- [ ] 0 critical memory warnings: Android Profiler or Xcode Instruments shows 0 OOM events during a representative user flow
- [ ] Navigation is type-safe: `tsc --noEmit` exits 0 with 0 errors on route param types in `RootStackParamList` or Flutter config
- [ ] All list views use virtualization: `grep -rn "\.map(" src/screens/` returns = 0 matches for potentially large arrays
- [ ] Platform-specific UI differences handled: `grep -c "Platform\.OS\|defaultProps\|safe-area" src/` returns > 0
- [ ] Offline behavior defined: `grep -c "offline\|cached\|NetworkError\|no.network" src/` returns > 0

## Success Criteria

This task is complete when:
1. The app architecture follows the documented folder structure with clear separation of navigation, screens, services, and state
2. The app builds and runs without errors on both iOS simulator and Android emulator (or the target platform)
3. All critical user flows work correctly on a physical device with network throttling enabled
