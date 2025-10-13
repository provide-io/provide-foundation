// Polyglot Dependency Injection Pattern - Go Example
//
// This example demonstrates the SAME dependency injection pattern as the
// Python version (01_polyglot_di_pattern.py). Compare the structure:
//
// Python:                    Go:
// class Database:            type Database struct {}
// def __init__(self, x):     func NewDatabase(x string) *Database
// container.register(...)    database := NewDatabase(...)
// container.resolve(...)     service := NewUserService(repo, notif, log)
//
// The mental model is IDENTICAL. This is the "golden cage" - you learn
// one pattern that works across all three languages.

package main

import "fmt"

// ==============================================================================
// Domain Models (Pure Business Logic - No Framework Dependencies)
// ==============================================================================

type User struct {
	ID    int
	Name  string
	Email string
}

// ==============================================================================
// Infrastructure Layer (Implements Technical Concerns)
// ==============================================================================

type Database struct {
	connectionString string
}

func NewDatabase(connectionString string) *Database {
	fmt.Printf("[Database] Connected to %s\n", connectionString)
	return &Database{connectionString: connectionString}
}

func (db *Database) Query(sql string) []map[string]interface{} {
	fmt.Printf("[Database] Executing: %s\n", sql)
	// Mock implementation
	return []map[string]interface{}{
		{"id": 1, "name": "Alice", "email": "alice@example.com"},
	}
}

type HTTPClient struct {
	baseURL string
	timeout int
}

func NewHTTPClient(baseURL string, timeout int) *HTTPClient {
	fmt.Printf("[HTTPClient] Configured for %s (timeout: %ds)\n", baseURL, timeout)
	return &HTTPClient{baseURL: baseURL, timeout: timeout}
}

func (c *HTTPClient) Post(path string, data map[string]interface{}) map[string]interface{} {
	url := c.baseURL + path
	fmt.Printf("[HTTPClient] POST %s with %v\n", url, data)
	// Mock implementation
	return map[string]interface{}{"status": "success", "message": "User created"}
}

type Logger struct {
	level string
}

func NewLogger(level string) *Logger {
	fmt.Printf("[Logger] Initialized with level %s\n", level)
	return &Logger{level: level}
}

func (l *Logger) Info(message string) {
	fmt.Printf("[INFO] %s\n", message)
}

func (l *Logger) Error(message string) {
	fmt.Printf("[ERROR] %s\n", message)
}

// ==============================================================================
// Application Layer (Business Logic Using Infrastructure)
// ==============================================================================

type UserRepository struct {
	db     *Database
	logger *Logger
}

// NewUserRepository creates a repository with explicit dependencies
// This is IDENTICAL to Python's @injectable class with __init__
func NewUserRepository(db *Database, logger *Logger) *UserRepository {
	logger.Info("UserRepository initialized")
	return &UserRepository{db: db, logger: logger}
}

func (r *UserRepository) FindByID(userID int) *User {
	r.logger.Info(fmt.Sprintf("Finding user %d", userID))
	rows := r.db.Query(fmt.Sprintf("SELECT * FROM users WHERE id = %d", userID))
	if len(rows) == 0 {
		return nil
	}
	row := rows[0]
	return &User{
		ID:    row["id"].(int),
		Name:  row["name"].(string),
		Email: row["email"].(string),
	}
}

type NotificationService struct {
	httpClient *HTTPClient
	logger     *Logger
}

func NewNotificationService(httpClient *HTTPClient, logger *Logger) *NotificationService {
	logger.Info("NotificationService initialized")
	return &NotificationService{httpClient: httpClient, logger: logger}
}

func (s *NotificationService) NotifyUserCreated(user *User) bool {
	s.logger.Info(fmt.Sprintf("Sending notification for user %s", user.Name))
	response := s.httpClient.Post("/notifications", map[string]interface{}{
		"user_id": user.ID,
		"event":   "user.created",
	})
	return response["status"] == "success"
}

type UserService struct {
	repository    *UserRepository
	notifications *NotificationService
	logger        *Logger
}

// NewUserService creates the main service with all dependencies
// This is IDENTICAL to Python's @injectable UserService.__init__
func NewUserService(
	repository *UserRepository,
	notifications *NotificationService,
	logger *Logger,
) *UserService {
	logger.Info("UserService initialized")
	return &UserService{
		repository:    repository,
		notifications: notifications,
		logger:        logger,
	}
}

func (s *UserService) GetUser(userID int) *User {
	s.logger.Info(fmt.Sprintf("Getting user %d", userID))
	user := s.repository.FindByID(userID)
	if user != nil {
		s.logger.Info(fmt.Sprintf("Found user: %s", user.Name))
		s.notifications.NotifyUserCreated(user)
	}
	return user
}

// ==============================================================================
// Composition Root (Application Entry Point)
// ==============================================================================

func main() {
	// This is IDENTICAL to Python's main() function structure
	// The only difference: Go doesn't have a DI container, so we wire manually
	// But the PATTERN is the same: create dependencies top-down, pass explicitly

	fmt.Println("======================================================================")
	fmt.Println("Go Dependency Injection Example")
	fmt.Println("======================================================================")

	// Step 1: Create infrastructure dependencies
	fmt.Println("\n[Composition Root] Creating infrastructure dependencies...")
	database := NewDatabase("postgresql://localhost/myapp")
	httpClient := NewHTTPClient("https://api.example.com", 30)
	logger := NewLogger("INFO")

	// Step 2: Create application services with dependencies
	fmt.Println("\n[Composition Root] Creating application services...")
	repository := NewUserRepository(database, logger)
	notifications := NewNotificationService(httpClient, logger)

	// Step 3: Create main service
	fmt.Println("\n[Composition Root] Creating UserService...")
	userService := NewUserService(repository, notifications, logger)

	// Step 4: Run the application
	fmt.Println("\n======================================================================")
	fmt.Println("Running Application")
	fmt.Println("======================================================================\n")

	user := userService.GetUser(1)
	if user != nil {
		fmt.Printf("\n✅ Successfully retrieved user: %s (%s)\n", user.Name, user.Email)
	} else {
		fmt.Println("\n❌ User not found")
	}
}
