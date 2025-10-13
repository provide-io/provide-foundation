// Polyglot Dependency Injection Pattern - Rust Example
//
// This example demonstrates the SAME dependency injection pattern as the
// Python and Go versions. Compare the structure:
//
// Python:                    Rust:
// class Database:            struct Database {}
// def __init__(self, x):     impl Database { fn new(x: String) -> Self }
// container.register(...)    let database = Database::new(...)
// container.resolve(...)     let service = UserService::new(repo, notif, log)
//
// The mental model is IDENTICAL across all three languages.

use std::collections::HashMap;

// ==============================================================================
// Domain Models (Pure Business Logic - No Framework Dependencies)
// ==============================================================================

#[derive(Debug, Clone)]
struct User {
    id: i32,
    name: String,
    email: String,
}

// ==============================================================================
// Infrastructure Layer (Implements Technical Concerns)
// ==============================================================================

struct Database {
    connection_string: String,
}

impl Database {
    fn new(connection_string: String) -> Self {
        println!("[Database] Connected to {}", connection_string);
        Self { connection_string }
    }

    fn query(&self, sql: &str) -> Vec<HashMap<String, String>> {
        println!("[Database] Executing: {}", sql);
        // Mock implementation
        let mut row = HashMap::new();
        row.insert("id".to_string(), "1".to_string());
        row.insert("name".to_string(), "Alice".to_string());
        row.insert("email".to_string(), "alice@example.com".to_string());
        vec![row]
    }
}

struct HTTPClient {
    base_url: String,
    timeout: u32,
}

impl HTTPClient {
    fn new(base_url: String, timeout: u32) -> Self {
        println!("[HTTPClient] Configured for {} (timeout: {}s)", base_url, timeout);
        Self { base_url, timeout }
    }

    fn post(&self, path: &str, data: HashMap<String, String>) -> HashMap<String, String> {
        let url = format!("{}{}", self.base_url, path);
        println!("[HTTPClient] POST {} with {:?}", url, data);
        // Mock implementation
        let mut response = HashMap::new();
        response.insert("status".to_string(), "success".to_string());
        response.insert("message".to_string(), "User created".to_string());
        response
    }
}

struct Logger {
    level: String,
}

impl Logger {
    fn new(level: String) -> Self {
        println!("[Logger] Initialized with level {}", level);
        Self { level }
    }

    fn info(&self, message: &str) {
        println!("[INFO] {}", message);
    }

    fn error(&self, message: &str) {
        println!("[ERROR] {}", message);
    }
}

// ==============================================================================
// Application Layer (Business Logic Using Infrastructure)
// ==============================================================================

struct UserRepository<'a> {
    db: &'a Database,
    logger: &'a Logger,
}

// Constructor with explicit dependencies - IDENTICAL to Python and Go
impl<'a> UserRepository<'a> {
    fn new(db: &'a Database, logger: &'a Logger) -> Self {
        logger.info("UserRepository initialized");
        Self { db, logger }
    }

    fn find_by_id(&self, user_id: i32) -> Option<User> {
        self.logger.info(&format!("Finding user {}", user_id));
        let rows = self.db.query(&format!("SELECT * FROM users WHERE id = {}", user_id));
        if rows.is_empty() {
            return None;
        }
        let row = &rows[0];
        Some(User {
            id: row.get("id").unwrap().parse().unwrap(),
            name: row.get("name").unwrap().clone(),
            email: row.get("email").unwrap().clone(),
        })
    }
}

struct NotificationService<'a> {
    http_client: &'a HTTPClient,
    logger: &'a Logger,
}

impl<'a> NotificationService<'a> {
    fn new(http_client: &'a HTTPClient, logger: &'a Logger) -> Self {
        logger.info("NotificationService initialized");
        Self { http_client, logger }
    }

    fn notify_user_created(&self, user: &User) -> bool {
        self.logger.info(&format!("Sending notification for user {}", user.name));
        let mut data = HashMap::new();
        data.insert("user_id".to_string(), user.id.to_string());
        data.insert("event".to_string(), "user.created".to_string());
        let response = self.http_client.post("/notifications", data);
        response.get("status").map(|s| s == "success").unwrap_or(false)
    }
}

struct UserService<'a> {
    repository: &'a UserRepository<'a>,
    notifications: &'a NotificationService<'a>,
    logger: &'a Logger,
}

// Constructor with explicit dependencies - IDENTICAL to Python and Go
impl<'a> UserService<'a> {
    fn new(
        repository: &'a UserRepository<'a>,
        notifications: &'a NotificationService<'a>,
        logger: &'a Logger,
    ) -> Self {
        logger.info("UserService initialized");
        Self {
            repository,
            notifications,
            logger,
        }
    }

    fn get_user(&self, user_id: i32) -> Option<User> {
        self.logger.info(&format!("Getting user {}", user_id));
        if let Some(user) = self.repository.find_by_id(user_id) {
            self.logger.info(&format!("Found user: {}", user.name));
            self.notifications.notify_user_created(&user);
            Some(user)
        } else {
            None
        }
    }
}

// ==============================================================================
// Composition Root (Application Entry Point)
// ==============================================================================

fn main() {
    // This is IDENTICAL to Python's main() and Go's main() structure
    // The pattern: create dependencies top-down, pass explicitly

    println!("======================================================================");
    println!("Rust Dependency Injection Example");
    println!("======================================================================");

    // Step 1: Create infrastructure dependencies
    println!("\n[Composition Root] Creating infrastructure dependencies...");
    let database = Database::new("postgresql://localhost/myapp".to_string());
    let http_client = HTTPClient::new("https://api.example.com".to_string(), 30);
    let logger = Logger::new("INFO".to_string());

    // Step 2: Create application services with dependencies
    println!("\n[Composition Root] Creating application services...");
    let repository = UserRepository::new(&database, &logger);
    let notifications = NotificationService::new(&http_client, &logger);

    // Step 3: Create main service
    println!("\n[Composition Root] Creating UserService...");
    let user_service = UserService::new(&repository, &notifications, &logger);

    // Step 4: Run the application
    println!("\n======================================================================");
    println!("Running Application");
    println!("======================================================================\n");

    if let Some(user) = user_service.get_user(1) {
        println!("\n✅ Successfully retrieved user: {} ({})", user.name, user.email);
    } else {
        println!("\n❌ User not found");
    }
}
