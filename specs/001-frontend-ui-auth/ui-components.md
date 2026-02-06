# UI Components Specification: Frontend UI with Authentication

**Feature**: 001-frontend-ui-auth
**Created**: 2026-01-09
**Status**: Draft

## Reusable Components

### AuthForm Component

**Props & behavior**:
- `title`: String - The form title (e.g., "Login" or "Sign Up")
- `fields`: Array of objects defining form fields with properties: {name, label, type, required}
- `submitButtonText`: String - Text for the submit button
- `onSubmit`: Function - Callback when form is submitted
- `isLoading`: Boolean - Whether the form is in a loading state
- `errorMessage`: String - Error message to display if any

**Visual role**: Provides a consistent form layout for authentication pages with proper styling, validation, and loading states.

---

### TaskCard Component

**Props & behavior**:
- `task`: Object - Task object with properties: {id, title, description, completed, dueDate, createdAt}
- `onToggleComplete`: Function - Callback when completion status is toggled
- `onEdit`: Function - Callback when edit button is clicked
- `onDelete`: Function - Callback when delete button is clicked
- `onSelect`: Function - Callback when card is selected/clicked

**Visual role**: Displays a single task with title, description, due date, and status indicator. Includes action buttons for editing, deleting, and toggling completion status.

---

### TaskForm Component

**Props & behavior**:
- `task`: Object - Task object to pre-populate form (optional for new tasks)
- `onSubmit`: Function - Callback when form is submitted
- `onCancel`: Function - Callback when cancel button is clicked
- `isLoading`: Boolean - Whether the form is in a loading state
- `errors`: Object - Field-specific error messages

**Visual role**: Provides a consistent form layout for creating and editing tasks with proper validation and error handling.

---

### Navigation Component

**Props & behavior**:
- `currentUser`: Object - Current user object with properties: {id, email, name}
- `activePage`: String - Identifier for the currently active page
- `onLogout`: Function - Callback when logout is triggered

**Visual role**: Provides consistent navigation across all application pages with user profile and logout functionality. Adapts layout for desktop (sidebar) and mobile (top navigation).

---

### LoadingSpinner Component

**Props & behavior**:
- `size`: String - Size of spinner ("sm", "md", "lg") - default "md"
- `className`: String - Additional CSS classes to apply

**Visual role**: Provides a consistent loading indicator that can be used throughout the application during API calls or other asynchronous operations.

---

### ToastNotification Component

**Props & behavior**:
- `message`: String - The notification message
- `type`: String - Type of notification ("success", "error", "warning", "info") - default "info"
- `duration`: Number - Duration in milliseconds before auto-dismissing - default 5000
- `onDismiss`: Function - Callback when notification is dismissed

**Visual role**: Displays temporary notifications to provide feedback to users about actions they've taken or system events.

---

### EmptyState Component

**Props & behavior**:
- `title`: String - Title for the empty state
- `description`: String - Description explaining the empty state
- `icon`: String - Icon name or JSX element to display
- `actionText`: String - Text for the primary action button (optional)
- `onActionClick`: Function - Callback when action button is clicked (optional)

**Visual role**: Provides a consistent way to display empty states when there is no data to show, such as when a user has no tasks yet.

---

### ProtectedRoute Component

**Props & behavior**:
- `children`: ReactNode - The content to render if user is authenticated
- `fallbackUrl`: String - URL to redirect to if user is not authenticated - default "/login"

**Visual role**: Wrapper component that checks authentication status and redirects unauthenticated users to the login page.

---

### ApiClient Component

**Props & behavior**:
- `baseUrl`: String - Base URL for API requests
- `authToken`: String - JWT token for authentication

**Visual role**: Centralized API client that automatically attaches Authorization header to requests and handles 401 responses by redirecting to login.