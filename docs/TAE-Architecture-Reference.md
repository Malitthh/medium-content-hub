# Test Automation Engineering — Architect Reference

> **Author:** Senior Test Engineer · ISTQB CTAL-TAE v2.0 Certified

> **Purpose:** Living reference for test automation architecture, patterns, and standards.
> Read this to onboard a project, design a TAF from scratch, answer interview questions, or refresh your knowledge as an architect.

> **Last updated:** 2026

---

## Table of Contents

1. [The Mental Model — What Test Automation Really Is](#1-the-mental-model)
2. [The Three-Layer TAF Architecture](#2-the-three-layer-taf-architecture)
3. [The Generic Test Automation Architecture (gTAA)](#3-the-generic-test-automation-architecture-gtaa)
4. [Design Patterns](#4-design-patterns)
   - 4.1 [Page / Screen Object Model (POM)](#41-page--screen-object-model-pom)
   - 4.2 [Flow Model Pattern](#42-flow-model-pattern)
   - 4.3 [Facade Pattern](#43-facade-pattern)
   - 4.4 [Singleton Pattern](#44-singleton-pattern)
   - 4.5 [How the Four Patterns Work Together](#45-how-the-four-patterns-work-together)
5. [Object-Oriented Programming Principles](#5-object-oriented-programming-principles)
6. [SOLID Principles](#6-solid-principles)
7. [Clean Code Standards](#7-clean-code-standards)
8. [Wait Strategies](#8-wait-strategies)
   - 8.1 [Hardcoded Wait — Avoid](#81-hardcoded-wait--avoid)
   - 8.2 [Dynamic Polling — Explicit Wait](#82-dynamic-polling--explicit-wait)
   - 8.3 [Fluent Wait — Advanced Polling](#83-fluent-wait--advanced-polling)
   - 8.4 [Event Subscription — Most Reliable](#84-event-subscription--most-reliable)
   - 8.5 [Selenium Naming vs Modern Framework Naming](#85-selenium-naming-vs-modern-framework-naming)
   - 8.6 [The Golden Rule on Waits](#86-the-golden-rule-on-waits)
9. [Testability — What You Need from the SUT](#9-testability--what-you-need-from-the-sut)
10. [Test Environments](#10-test-environments)
11. [CI/CD Pipeline Integration](#11-cicd-pipeline-integration)
12. [Configuration Management for Testware](#12-configuration-management-for-testware)
13. [Test Data Strategy](#13-test-data-strategy)
14. [Logging and Reporting](#14-logging-and-reporting)
15. [Risk Management in Test Automation](#15-risk-management-in-test-automation)
16. [Continuous Improvement](#16-continuous-improvement)
17. [Test Scripting Approaches — Maturity Ladder](#17-test-scripting-approaches--maturity-ladder)
18. [API and Contract Testing](#18-api-and-contract-testing)
19. [Static Analysis](#19-static-analysis)
20. [Practical Project Structure — Java / Appium](#20-practical-project-structure--java--appium)
21. [Practical Project Structure — TypeScript / Playwright](#21-practical-project-structure--typescript--playwright)
22. [Interview Reference — Questions and Answers](#22-interview-reference--questions-and-answers)
23. [The Architect Prompt — Reusable Project Bootstrap](#23-the-architect-prompt--reusable-project-bootstrap)
24. [Glossary](#24-glossary)

---

## 1. The Mental Model

> **Simple version:** The SUT is the thing being tested. The TAF is the thing doing the testing. They are completely separate. Your TAF talks to the SUT through defined interfaces. Everything else follows from this.

### What is the System Under Test (SUT)?

The SUT is the application under test. It has no knowledge of your test framework. It just receives actions and produces observable results. Your TAF is the client. The SUT is the server.

Examples:
- A web app being tested by Playwright → the web app is the SUT
- A mobile app being tested by Appium → the mobile app is the SUT
- A REST API being tested → the API is the SUT

### What is the Test Automation Framework (TAF)?

The TAF is the code you write to drive and assert on the SUT. It is a software project in its own right. It has architecture, design patterns, naming conventions, version control, and a CI/CD pipeline.

The TAF communicates with the SUT through three channels:

| Channel | What it does | Tools |
|---|---|---|
| UI | Drives the visual interface — clicks, inputs, navigation | Playwright, Appium, Selenium |
| API | Sends HTTP requests directly to backend endpoints | RestAssured, Playwright request, OkHttp |
| Database | Reads/writes data directly for setup and teardown only | JDBC, Hibernate, Sequelize |

> **Rule:** Assert through the UI or API. Use the database only for setup and teardown. Never assert on database state as a substitute for a proper API assertion — it creates tight coupling to implementation.

---

## 2. The Three-Layer TAF Architecture

This is the foundational architecture. Every project follows this regardless of language, tool, or platform.

```
┌─────────────────────────────────────────┐
│          LAYER 1 — Test Scripts         │  ← what tests DO
│   spec files · suites · annotations     │
└──────────────────┬──────────────────────┘
                   │ calls only
┌──────────────────▼──────────────────────┐
│        LAYER 2 — Business Logic         │  ← what the APP does
│  Screen/Page Objects · Flow Models      │
└──────────────────┬──────────────────────┘
                   │ calls only
┌──────────────────▼──────────────────────┐
│         LAYER 3 — Core Libraries        │  ← how automation WORKS
│ DriverFactory · Logger · WaitHelper     │
└──────────────────┬──────────────────────┘
                   │ interfaces with
┌──────────────────▼──────────────────────┐
│        System Under Test (SUT)          │
│     Web App · Mobile App · API          │
└─────────────────────────────────────────┘
```

### Layer Rules — Non-Negotiable

| Layer | Contains | Must NOT contain |
|---|---|---|
| Test Scripts | Test methods, assertions, test data references | Locators, driver calls, raw Appium/Playwright API |
| Business Logic | Screen objects, flow models, SUT-specific helpers | Driver setup, reporter config, SUT-independent utilities |
| Core Libraries | Driver factory, logger, wait helpers, reporters | Anything SUT-specific or test-specific |

### Why Three Layers?

**Without layers**, a change to one button in the UI requires hunting through 50 test files.
**With layers**, that same change touches one locator in one screen object class. Done.

The layers enforce the Single Responsibility Principle at the architectural level, not just the class level.

---

## 3. The Generic Test Automation Architecture (gTAA)

The gTAA is the formal ISTQB name for the system that connects your TAF to the outside world. Think of it as the wiring diagram above your three layers.

```
      Project Management
             ↕
    ┌────────────────────┐
    │  Test Automation   │    ← Configuration Management (CI/CD, environments, testware)
    │    Framework       │    ← Test Management (Jira, Azure DevOps)
    │                    │
    │  Test Generation   │  optional — model-based or AI-generated tests
    │  Test Definition   │  your spec files and test data
    │  Test Execution    │  your runner (TestNG, JUnit, Playwright runner)
    │  Test Adaptation   │  the layer that talks to the SUT
    └────────┬───────────┘
             ↓
      System Under Test
```

### The Four gTAA Capabilities Explained Simply

| Capability | Plain English | In Your Project |
|---|---|---|
| Test Generation | Automated creation of test cases from a model | AI tools, model-based testing — optional |
| Test Definition | Where your tests and test data are defined | `tests/` folder, `testData.json` |
| Test Execution | Running the tests and producing logs | TestNG runner, Maven Surefire |
| Test Adaptation | The adapter between TAF and SUT | Appium driver, Playwright browser, RestAssured |

---

## 4. Design Patterns

### 4.1 Page / Screen Object Model (POM)

**The analogy:** A TV remote. The remote hides all the electronics inside. You press "Volume Up" — you do not wire the circuit yourself. The remote is the page object. The button is the locator. The action is the method.

**The rule:** One class per screen. Locators are private. Methods are public. Test scripts never contain raw selectors.

**Without POM — the problem:**
```java
// Test file A
driver.findElement(By.id("login-btn")).click();

// Test file B
driver.findElement(By.id("login-btn")).click();

// Test file C
driver.findElement(By.id("login-btn")).click();

// Dev renames the button ID → you update 3 files
// In a real project this could be 50 files
```

**With POM — the solution:**
```java
// LoginScreen.java — Business Logic layer
public class LoginScreen extends BaseScreen {

    // Locators are PRIVATE — test scripts cannot touch them directly
    @AndroidFindBy(accessibility = "login-button")
    @iOSXCUITFindBy(accessibility = "login-button")
    private MobileElement loginButton;

    @AndroidFindBy(accessibility = "username-field")
    @iOSXCUITFindBy(accessibility = "username-field")
    private MobileElement usernameField;

    @AndroidFindBy(accessibility = "password-field")
    @iOSXCUITFindBy(accessibility = "password-field")
    private MobileElement passwordField;

    public LoginScreen(AppiumDriver driver) {
        super(driver);
        PageFactory.initElements(new AppiumFieldDecorator(driver), this);
    }

    // Public methods expose BEHAVIOUR, not elements
    public void login(String username, String password) {
        waitForElement(usernameField).sendKeys(username);
        passwordField.sendKeys(password);
        loginButton.click();
    }

    public String getErrorMessage() {
        return waitForElement(By.accessibility("error-message")).getText();
    }
}

// LoginTest.java — Test Scripts layer (clean — no locators anywhere)
@Test
public void loginWithValidCredentials() {
    loginScreen.login(testData.validUser, testData.validPass);
    Assert.assertTrue(homeScreen.isLoaded(), "Home screen should be visible after login");
}
```

**Dev renames the button ID → you update one line in `LoginScreen.java`. All 50 tests are fixed automatically.**

### 4.2 Flow Model Pattern

**The analogy:** A travel agent. You call and say "book me a week in Tokyo." The agent handles flights, hotel, JR Pass, and itinerary. You do not call each service yourself. The travel agent is the flow model. The individual services are your screen objects.

**The problem it solves:** Multi-step user journeys duplicated across many tests.

**Without Flow Model — duplication:**
```java
// Test A — happy checkout
cartScreen.addItem("laptop");
cartScreen.proceedToCheckout();
checkoutScreen.fillAddress(address);
checkoutScreen.selectShipping("standard");
paymentScreen.enterCard(card);
paymentScreen.confirmOrder();

// Test B — verify order summary (same 6 lines again before the actual assertion)
cartScreen.addItem("laptop");
checkoutScreen.fillAddress(address);
// ... repeated
```

**With Flow Model — one reusable journey:**
```java
// CheckoutFlow.java — Business Logic layer
public class CheckoutFlow {
    private final CartScreen cartScreen;
    private final CheckoutScreen checkoutScreen;
    private final PaymentScreen paymentScreen;

    public CheckoutFlow(AppiumDriver driver) {
        this.cartScreen     = new CartScreen(driver);
        this.checkoutScreen = new CheckoutScreen(driver);
        this.paymentScreen  = new PaymentScreen(driver);
    }

    public void completeCheckout(String item, Address address, Card card) {
        cartScreen.addItem(item);
        cartScreen.proceedToCheckout();
        checkoutScreen.fillAddress(address);
        checkoutScreen.selectShipping("standard");
        paymentScreen.enterCard(card);
        paymentScreen.confirmOrder();
    }
}

// Test A — one line of setup
checkoutFlow.completeCheckout("laptop", testData.address, testData.card);
Assert.assertTrue(confirmationScreen.isVisible());

// Test B — same one line
checkoutFlow.completeCheckout("laptop", testData.address, testData.card);
Assert.assertEquals(summaryScreen.getTotal(), "AUD 1,299.00");
```

**New step added to checkout → fix it in `CheckoutFlow` once. All tests updated.**

> **Flow Model sits above POM.** Screen Objects are the individual steps. Flow Models are the choreographed journeys. You call a Flow from your test script. The Flow calls Screen Objects. Screen Objects call the driver.

### 4.3 Facade Pattern

**The analogy:** A hospital receptionist. Behind the desk are radiology, pharmacy, billing, and pathology. You do not navigate each department. You tell the receptionist what you need. They handle the routing.

**What it hides in your TAF:** All the complexity of setting up an Appium driver — server connection, capability loading, platform branching, session management.

**Without Facade — every test class is a mess:**
```java
// Duplicated in every test class that needs a driver
DesiredCapabilities caps = new DesiredCapabilities();
caps.setCapability("platformName", "Android");
caps.setCapability("appium:deviceName", "Pixel 7");
caps.setCapability("appium:app", System.getenv("APP_PATH"));
caps.setCapability("appium:automationName", "UiAutomator2");
AppiumDriver driver = new AndroidDriver(
    new URL("http://" + System.getenv("APPIUM_HOST") + ":4723"),
    caps
);
```

**With Facade — clean:**
```java
AppiumDriver driver = DriverFactory.getDriver("android");
// All that complexity lives inside DriverFactory. Tests know nothing about it.
```

**Key benefit:** You change the Appium server address, upgrade the device, or add a new platform — you change it in `DriverFactory` only. Zero test files break.

### 4.4 Singleton Pattern

**The analogy:** One master key for an office building. No matter who asks for it — the cleaner, the manager, the security guard — they all get the same physical key. There is only ever one.

**What it prevents:** Multiple driver sessions competing for the same device port.

**Without Singleton — chaos:**
```java
// Test A creates a driver
AppiumDriver driverA = new AndroidDriver(url, caps); // session 1

// Test B also creates a driver
AppiumDriver driverB = new AndroidDriver(url, caps); // session 2

// Two sessions on one device → port conflict → flaky failures
```

**With Singleton — one session:**
```java
public class DriverFactory {

    // The "one key" — private, static, class-level
    private static AppiumDriver instance = null;

    public static AppiumDriver getDriver(String platform) {
        if (instance == null) {
            // This block runs ONCE across the entire test run
            instance = createDriver(platform);
        }
        return instance; // Everyone gets the same instance
    }

    public static void quitDriver() {
        if (instance != null) {
            instance.quit();
            instance = null; // Allow a fresh session next suite
        }
    }

    private static AppiumDriver createDriver(String platform) {
        // All the messy setup lives here — hidden from callers
        DesiredCapabilities caps = CapabilityManager.load(platform);
        try {
            String host = ConfigManager.get("appium.host");
            return platform.equals("ios")
                ? new IOSDriver(new URL(host), caps)
                : new AndroidDriver(new URL(host), caps);
        } catch (MalformedURLException e) {
            throw new RuntimeException("Invalid Appium host: " + e.getMessage());
        }
    }
}
```

> **Singleton and Facade live in the same class** (`DriverFactory`) because they solve different problems. Singleton = only one driver. Facade = hides how it is built. Together they give you a clean, stable driver for your entire test suite.

### 4.5 How the Four Patterns Work Together

```
Test Script
    │
    │ calls one method
    ▼
Flow Model  ──────────── Facade Pattern: hides journey complexity
    │
    │ calls individual screens
    ▼
Screen Object ────────── POM: encapsulates locators, hides element detail
    │
    │ calls driver
    ▼
DriverFactory ─────────── Facade: hides Appium setup
              ─────────── Singleton: one driver instance
    │
    ▼
Appium → SUT
```

Every layer hides something from the layer above. This is the principle of encapsulation applied at architectural scale.

---

## 5. Object-Oriented Programming Principles

The four pillars and how they appear in a TAF:

| Pillar | What it means | TAF example |
|---|---|---|
| Encapsulation | Bundle data and behaviour together. Hide internals. | Locators are `private` in screen objects. Tests cannot access raw selectors. |
| Abstraction | Expose only what the caller needs. Hide the rest. | `loginScreen.login(user, pass)` — the caller does not know about the individual field interactions. |
| Inheritance | Share behaviour through a parent class. | `LoginScreen extends BaseScreen` — gets `waitForElement`, `takeScreenshot` etc. for free. |
| Polymorphism | Different classes, same interface. | `AndroidLoginScreen` and `IOSLoginScreen` both extend `LoginScreen` but implement gestures differently. |

---

## 6. SOLID Principles

Memorise these with one TAF example each. This is the most common interview topic.

| Letter | Principle | One-line definition | TAF example |
|---|---|---|---|
| S | Single Responsibility | One class, one job | `LoginScreen` handles login only. It does not also handle navigation or form validation. |
| O | Open / Closed | Open for extension, closed for modification | Add iOS support by extending `BaseScreen`, not by rewriting it with `if (platform == "ios")` blocks. |
| L | Liskov Substitution | A subclass can replace its parent without breaking anything | `MobileLoginScreen` works anywhere `BaseScreen` is expected. |
| I | Interface Segregation | Do not force a class to implement methods it does not use | Mobile screens should not implement `getNetworkTab()` — that belongs in a separate web-only interface. |
| D | Dependency Inversion | Depend on abstractions, not concretions | Tests depend on `IDriverFactory` interface, not `AndroidDriver` directly. Swap to a remote grid → zero test changes. |

**The SOLID violation that causes the most maintenance pain in practice:**

Violating Single Responsibility — screen objects that contain 200 lines covering three different screens, or test classes that do setup, execution, and reporting all in one method. When one thing changes, everything breaks.

---

## 7. Clean Code Standards

Source: Robert C. Martin — *Clean Code: A Handbook of Agile Software Craftsmanship* (2008)

### Naming

```java
// Bad — meaningless names
MobileElement e1;
public void m1(String s, String s2) { ... }

// Good — names that explain intent
MobileElement loginButton;
public void login(String username, String password) { ... }
```

**Naming conventions for a TAF project:**

| Artifact | Convention | Example |
|---|---|---|
| Test class | `[Feature]Test` | `BusinessInfoTest` |
| Screen object | `[Screen]Screen` | `LoginScreen` |
| Flow class | `[Journey]Flow` | `MerchantOnboardingFlow` |
| Helper/utility | `[Name]Helper` or `[Name]Manager` | `WaitHelper`, `CapabilityManager` |
| Test data key | `camelCase` matching field name | `businessName`, `abnNumber` |

### No Hardcoding

```java
// Bad — hardcoded everywhere
driver.findElement(By.id("submit")).click();
Thread.sleep(3000);
String url = "http://localhost:4723";

// Good — externalised
loginScreen.tapSubmit();
waitHelper.waitForVisible(element, 10);
String url = ConfigManager.get("appium.server.url");
```

**What to externalise:**

| What | Where it lives |
|---|---|
| URLs and endpoints | `config.properties` or environment variable |
| Device capabilities | `android.capabilities.json`, `ios.capabilities.json` |
| Test data | `testData.json` or CSV fixtures |
| Feature toggles | `featureFlags.properties` |
| Timeouts | `config.properties` — never inline |

### Method Length and Complexity

- A method should do one thing and fit on one screen
- If you need to scroll to understand a method, it is too long — break it up
- Maximum 3–4 parameters on a method. More than that → use a parameter object or builder pattern

### Logging — Six Levels

```java
logger.fatal("Driver session could not be created — aborting suite");
logger.error("Login failed: expected home screen, got error modal");
logger.warn("Element not immediately visible — retrying with FluentWait");
logger.info("Test: login_valid_user | Status: STARTED");
logger.debug("Tapping element: By.accessibilityId('login-button') at (230, 445)");
logger.trace("Raw Appium response: {status: 0, sessionId: 'abc123', value: null}");
```

**When to use which level:**

| Level | Use when | Enabled in CI |
|---|---|---|
| FATAL | Suite must abort — driver creation failure, environment unreachable | Always |
| ERROR | Test case fails — assertion failure, unexpected exception | Always |
| WARN | Unexpected but recoverable — retry triggered, element stale | Always |
| INFO | Normal execution milestones — test started, navigated to screen | Always |
| DEBUG | Diagnostic detail — element coordinates, wait duration | On failure only |
| TRACE | Raw API calls, full response bodies | Dev investigation only |

### Version Control Branching

```
main           ← stable, release-tagged, always green
  └── feature/TC-123-login-automation    ← new test cases
  └── fix/TC-456-flaky-checkout-wait     ← fixing unstable tests
  └── release/v2.1                       ← testware aligned to SUT v2.1
```

**Align testware version tags to SUT release tags.** This makes it possible to answer "which tests ran against which version of the app" — essential for defect triage.

---

## 8. Wait Strategies

This is one of the highest-frequency interview topics. Know all four, rank them, give the code.

### 8.1 Hardcoded Wait — Avoid

**The analogy:** Setting a timer for 30 minutes to pick up your pizza. It might be ready in 10. It might take 40. You are guessing.

**The problem:** Makes every test slower. Fails on slow environments. Passes on fast ones. Non-deterministic by design.

```java
// Java — never do this
Thread.sleep(3000);

// JavaScript — never do this
await page.waitForTimeout(3000);
```

**The one legitimate use:** Adding a 500ms pause to debug a visual issue during local development. Never commit `Thread.sleep` to source control.

### 8.2 Dynamic Polling — Explicit Wait

**The analogy:** Calling the pizza shop every 2 minutes to ask "is it ready?" Better than a timer — you stop as soon as it is ready — but you are still doing the work.

```java
// Selenium / Appium Java — WebDriverWait
WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
MobileElement element = (MobileElement) wait.until(
    ExpectedConditions.visibilityOfElementLocated(By.accessibilityId("login-button"))
);

// Playwright TypeScript equivalent
await page.waitForSelector('[data-testid="login-button"]');
await expect(page.locator('[data-testid="login-button"]')).toBeVisible();
```

**When to use:** Any time you need to wait for a specific element or condition. This is your default wait strategy.

### 8.3 Fluent Wait — Advanced Polling

**The analogy:** Calling the pizza shop every 2 minutes, but this time you also tell them "if you pick up and hear silence, just ignore it and keep my order live." Same polling idea but with custom frequency and exception handling.

Fluent Wait is Explicit Wait with two extra controls:
1. You set the polling interval (how often it checks)
2. You specify which exceptions to silently ignore during retries

```java
// Java — FluentWait (preferred over WebDriverWait for complex conditions)
Wait<AppiumDriver> wait = new FluentWait<>(driver)
    .withTimeout(Duration.ofSeconds(15))
    .pollingEvery(Duration.ofMillis(300))           // check every 300ms
    .ignoring(NoSuchElementException.class)         // element not yet in DOM — that is OK
    .ignoring(StaleElementReferenceException.class) // element refreshed — retry
    .withMessage("Login button did not appear within 15 seconds");

MobileElement loginButton = wait.until(
    d -> (MobileElement) d.findElement(By.accessibilityId("login-button"))
);
```

**Fluent Wait in your `WaitHelper` class — the clean way:**
```java
public class WaitHelper {

    private final AppiumDriver driver;
    private static final int DEFAULT_TIMEOUT = 10;
    private static final int DEFAULT_POLLING_MS = 300;

    public WaitHelper(AppiumDriver driver) {
        this.driver = driver;
    }

    public MobileElement waitForVisible(By locator) {
        return waitForVisible(locator, DEFAULT_TIMEOUT);
    }

    public MobileElement waitForVisible(By locator, int timeoutSeconds) {
        return new FluentWait<>(driver)
            .withTimeout(Duration.ofSeconds(timeoutSeconds))
            .pollingEvery(Duration.ofMillis(DEFAULT_POLLING_MS))
            .ignoring(NoSuchElementException.class)
            .ignoring(StaleElementReferenceException.class)
            .until(d -> {
                MobileElement el = (MobileElement) d.findElement(locator);
                return el.isDisplayed() ? el : null;
            });
    }

    public boolean waitForInvisible(By locator, int timeoutSeconds) {
        return new FluentWait<>(driver)
            .withTimeout(Duration.ofSeconds(timeoutSeconds))
            .pollingEvery(Duration.ofMillis(DEFAULT_POLLING_MS))
            .ignoring(NoSuchElementException.class)
            .until(ExpectedConditions.invisibilityOfElementLocated(locator));
    }

    public String waitForText(By locator, String expectedText, int timeoutSeconds) {
        MobileElement el = new FluentWait<>(driver)
            .withTimeout(Duration.ofSeconds(timeoutSeconds))
            .pollingEvery(Duration.ofMillis(DEFAULT_POLLING_MS))
            .ignoring(NoSuchElementException.class)
            .until(ExpectedConditions.textToBePresentInElementLocated(locator, expectedText));
        return el != null ? driver.findElement(locator).getText() : null;
    }
}
```

### 8.4 Event Subscription — Most Reliable

**The analogy:** The pizza shop texts you the second it comes out of the oven. You do nothing until that message arrives. No checking. No guessing. The shop (the SUT) tells you (the TAF) when something happens.

**Why it is the most reliable:** There is no window during which the condition is true but the TAF has not noticed yet. With polling, there is always a gap of up to one full poll interval. With event subscription, the gap is zero.

**The requirement:** The SUT must support and fire the right events. This is a conversation with the dev team.

**Appium event listener — subscribing to driver events:**
```java
// AppiumEventListener.java — Core Libraries layer
public class AppiumEventListener implements WebDriverEventListener {

    private static final Logger logger = LogManager.getLogger(AppiumEventListener.class);

    @Override
    public void beforeClickOn(WebElement element, WebDriver driver) {
        logger.debug("About to click: {}", element.toString());
    }

    @Override
    public void afterClickOn(WebElement element, WebDriver driver) {
        logger.info("Clicked: {}", element.toString());
    }

    @Override
    public void onException(Throwable throwable, WebDriver driver) {
        logger.error("Exception during driver action: {}", throwable.getMessage());
        // Capture screenshot automatically on any driver exception
        AllureHelper.attachScreenshot(driver, "exception_screenshot");
    }
}

// Wire it up in DriverFactory
EventFiringWebDriver eventDriver = new EventFiringWebDriver(rawDriver);
eventDriver.register(new AppiumEventListener());
```

**Playwright event subscription (TypeScript) — the most natural implementation:**
```typescript
// Subscribe to network responses — resolves the INSTANT the API responds
await Promise.all([
    page.waitForResponse(
        res => res.url().includes('/api/merchant/onboard') && res.status() === 200
    ),
    page.click('#submit-onboarding')
]);
// Zero polling — wakes up the exact millisecond the response arrives

// Subscribe to custom DOM events fired by the SUT
await Promise.all([
    page.evaluate(() =>
        new Promise(resolve =>
            document.addEventListener('stripe-connect-complete', resolve, { once: true })
        )
    ),
    page.click('#connect-stripe')
]);
```

**What to ask developers to build into the SUT:**
- `accessibility` / `content-desc` attributes on all interactive elements
- Meaningful `data-testid` attributes on key elements
- Custom DOM events at significant business moments (form submitted, payment complete)
- Test environment variables that disable animations and rate limiting

### 8.5 Selenium Naming vs Modern Framework Naming

This table exists because old-school interviewers use the Selenium terms. Know the mapping.

| Selenium term | CTAL-TAE category | What it really does | Modern equivalent |
|---|---|---|---|
| Implicit Wait | Hardcoded (global) | Sets a global timeout on every `findElement` call silently | Nothing — Playwright has no implicit wait. This is intentional. |
| Explicit Wait | Dynamic Polling | `WebDriverWait` — polls until condition is true or timeout | `page.waitForSelector()`, `expect(locator).toBeVisible()` |
| Fluent Wait | Advanced Polling | Like explicit wait but custom poll interval + ignore exceptions | Playwright `expect()` assertions have this built in automatically |

**The dangerous combination — never mix implicit and explicit in Selenium:**

When both are active, Selenium applies them sequentially. A 10-second implicit wait plus a 10-second explicit wait means the driver can wait up to 20 seconds before failing. This makes timeouts completely unpredictable and can double your suite execution time.

```java
// BAD — never do this in Selenium/Appium
driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(10)); // global
WebDriverWait explicitWait = new WebDriverWait(driver, Duration.ofSeconds(10)); // per-element
// Combined = up to 20 seconds unpredictably
```

**The Playwright truth:** Playwright's `expect()` assertions use `MutationObserver` under the hood — the DOM's native change notification system. This is closer to event subscription than polling. It reacts to the DOM changing rather than checking on a timer. This is why Playwright waits are more reliable than Selenium waits at the same timeout value.

### 8.6 The Golden Rule on Waits

```
If you wrote Thread.sleep() — fix it.
If you wrote an implicit wait — remove it.
If you wrote an explicit wait — good, but consider FluentWait for complex conditions.
If the SUT fires events you can subscribe to — use them.
```

---

## 9. Testability — What You Need from the SUT

Testability is a non-functional requirement of the application. It should be designed in from the start, not bolted on after. The TAE's job is to identify what is needed and communicate it to the dev team.

### Three Testability Dimensions

| Dimension | Definition | In Practice |
|---|---|---|
| Observability | The SUT provides interfaces to read its state | API responses, DOM structure, logs, accessibility labels |
| Controllability | The SUT provides interfaces to trigger actions | UI elements with stable IDs, API endpoints, test environment flags |
| Architecture Transparency | Clear documentation of components and interfaces | API docs, component diagrams, swagger/OpenAPI specs |

### Locator Strategy Priority

Use locators in this order. The further down the list, the more fragile.

```
1. Accessibility ID / content-desc  ← most stable, works cross-platform
2. data-testid attribute            ← stable, dev-added, explicit purpose
3. Resource ID (Android)            ← stable if devs keep IDs meaningful
4. XCUITest element type (iOS)      ← acceptable for standard UI components
5. Class name                       ← fragile — too generic
6. XPath                            ← last resort — brittle, slow
```

**What to request from developers:**

```xml
<!-- Android — add content-desc to all interactive elements -->
<Button
    android:id="@+id/loginButton"
    android:contentDescription="login-button"   ← this is your accessibility ID
    android:text="Log In" />

<!-- iOS — accessibilityIdentifier in code -->
loginButton.accessibilityIdentifier = "login-button"
```

**For web (Playwright):**
```html
<!-- Ask devs to add data-testid to all key elements -->
<button data-testid="login-button">Log In</button>
<input data-testid="username-field" type="text" />
```

---

## 10. Test Environments

Every project has multiple environments. Know what runs where.

| Environment | Purpose | Test types | Notes |
|---|---|---|---|
| Local dev | Initial development and debugging | Component, GUI, API, white-box | Developer's machine — fast iteration |
| Build / CI | Verify the build is not broken | Component tests, component integration, static analysis | No deployment — runs against built artefact |
| Integration | Full system testing against a real deployment | System integration, acceptance, black-box only | First environment with monitoring |
| Preproduction | Performance and non-functional quality | Performance, load, stress, UAT | Closest to production — monitored |
| Production | Live system monitoring | Canary, A/B testing, smoke checks | Real users — minimal intrusion |

**Practical rule:** Only run smoke tests in production. Never run destructive or load tests in production.

---

## 11. CI/CD Pipeline Integration

### Where Each Test Level Runs

```
Commit pushed
     │
     ▼
┌────────────────────────────────┐
│         BUILD PHASE            │
│  • Static analysis (SonarQube) │
│  • Unit / component tests      │
│  • Component integration tests │
│  • TAF configuration tests     │
└────────────────┬───────────────┘
                 │ only if build phase passes
                 ▼
┌────────────────────────────────┐
│         DEPLOY PHASE           │
│  • Deploy to integration env   │
│  • System tests (smoke first)  │
│  • System integration tests    │
└────────────────┬───────────────┘
                 │
                 ▼
┌────────────────────────────────┐
│       SCHEDULED / NIGHTLY      │
│  • Full regression suite       │
│  • Performance tests           │
│  • Cross-device matrix         │
└────────────────────────────────┘
```

### Two Ways to Integrate System Tests into the Pipeline

**Option 1 — Tests as part of the deployment (quality gate):**
- Tests run inside the deployment step
- A failed test fails the deployment and can trigger a rollback
- If tests must be re-run, a full redeployment is required
- Use when you need a hard quality gate with automated rollback

**Option 2 — Tests as a separate pipeline triggered by deployment:**
- Tests run in a separate pipeline triggered after successful deployment
- Tests do not block the deployment
- Rollback requires manual action
- Use when you run many different test suites or need flexibility

### GitHub Actions — Appium Example Structure

```yaml
# .github/workflows/appium-tests.yml
name: Appium Mobile Tests

on:
  push:
    branches: [main, feature/**]
  schedule:
    - cron: '0 20 * * *'  # Nightly at 8pm UTC

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Java
        uses: actions/setup-java@v4
        with:
          java-version: '17'

      - name: Static analysis
        run: mvn verify -P static-analysis

      - name: Run smoke suite
        run: mvn test -Dsuite=smoke -Dplatform=android

      - name: Upload Allure results
        uses: actions/upload-artifact@v4
        with:
          name: allure-results
          path: target/allure-results

  nightly-regression:
    runs-on: ubuntu-latest
    if: github.event_name == 'schedule'
    steps:
      - name: Run full regression
        run: mvn test -Dsuite=regression -Dplatform=android
```

---

## 12. Configuration Management for Testware

Configuration management ensures the right test code runs against the right version of the application, in the right environment.

### Three Things to Version-Control

| What | Where it lives | Example |
|---|---|---|
| Test environment config | `src/test/resources/config/` | URLs, credentials per environment |
| Test data | `src/test/resources/fixtures/` | Test users, form data, card numbers |
| Test suites | `src/test/resources/suites/` | Which tests run against which release |

### Feature Toggle Pattern

Use a feature toggle to enable or disable specific test groups per release without changing test code.

```properties
# featureFlags.properties
feature.stripe.connect=true
feature.abn.validation=true
feature.multi.location=false   # Not released in v2.1 — tests skipped
```

```java
// BaseTest.java — skip tests for unreleased features automatically
@BeforeMethod
public void checkFeatureFlag(Method method) {
    FeatureFlag annotation = method.getAnnotation(FeatureFlag.class);
    if (annotation != null) {
        boolean enabled = ConfigManager.getBoolean("feature." + annotation.value());
        if (!enabled) {
            throw new SkipException("Feature '" + annotation.value() + "' is not enabled in this environment");
        }
    }
}

// Usage in test
@Test
@FeatureFlag("multi.location")
public void testMultiLocationSetup() {
    // Skipped automatically in environments where the feature is off
}
```

### Aligning Testware to SUT Versions

```bash
# Tag your testware to match the SUT release
git tag -a testware-v2.1 -m "Aligned to Autara SUT v2.1"
git push origin testware-v2.1
```

When a defect is reported against a specific release, you can check out the exact testware tag that tested it. This is essential for defect triage.

---

## 13. Test Data Strategy

### The Three Rules

1. Never hardcode test data in test files
2. Create test data fresh per test when possible — never rely on leftover state
3. Clean up after yourself — leave the environment in the same state you found it

### Data Sources in Priority Order

| Source | When to use | Example |
|---|---|---|
| API call in `@BeforeMethod` | Creating users, accounts, records needed by the test | `POST /api/merchants` to create a test merchant |
| JSON fixture file | Static data that does not change between runs | Valid/invalid ABN formats, card numbers |
| Database seed script | Large datasets for performance tests | 10,000 product records for load testing |
| Environment variable | Credentials, secrets | `ADMIN_USER`, `ADMIN_PASS` — never in source control |

### Test Data File Structure

```json
// src/test/resources/fixtures/testData.json
{
  "validMerchant": {
    "businessName": "Sunrise Cafe Pty Ltd",
    "abn": "51824753556",
    "email": "test.merchant@autara-test.com",
    "phone": "+61400000001"
  },
  "invalidAbn": {
    "tooShort": "5182475",
    "wrongChecksum": "51824753557",
    "empty": "",
    "nonNumeric": "5182475ABC"
  },
  "stripeTestCard": {
    "number": "4242424242424242",
    "expiry": "12/26",
    "cvv": "123"
  }
}
```

### Setup and Teardown Pattern

```java
public class BusinessInfoTest extends BaseTest {

    @BeforeMethod
    public void setupMerchant() {
        // Create test merchant via API — fast, not via UI
        testMerchant = apiClient.createMerchant(testData.validMerchant);
        logger.info("Created test merchant: {}", testMerchant.getId());
    }

    @AfterMethod
    public void cleanupMerchant() {
        // Clean up regardless of test outcome
        if (testMerchant != null) {
            apiClient.deleteMerchant(testMerchant.getId());
            logger.info("Deleted test merchant: {}", testMerchant.getId());
        }
    }

    @Test
    public void submitValidBusinessInfo() {
        // Test focuses only on what only UI can verify
        businessInfoScreen.fillForm(testMerchant);
        businessInfoScreen.submit();
        Assert.assertTrue(verificationScreen.isLoaded());
    }
}
```

---

## 14. Logging and Reporting

### What to Log — TAS Logging Checklist

Every automated test run should produce logs that answer these questions without needing to re-run:

- Which test was running and when did it start and end?
- What was the final status — passed, failed, or TAS failure?
- What was the SUT's state at the moment of failure?
- What was the correlation ID for the failing API call?
- Were there any unexpected conditions during the run?

```java
// AppiumLogger.java — Core Libraries layer
public class AppiumLogger {

    private final Logger logger;
    private final String testName;

    public AppiumLogger(String testName) {
        this.testName = testName;
        this.logger = LogManager.getLogger(testName);
    }

    public void testStarted() {
        logger.info("TEST STARTED: {}", testName);
    }

    public void testPassed() {
        logger.info("✓ TEST PASSED: {}", testName);
    }

    public void testFailed(Throwable cause) {
        logger.error("✗ TEST FAILED: {} | Reason: {}", testName, cause.getMessage());
    }

    public void step(String description) {
        logger.info("  STEP: {}", description);
    }

    public void apiCall(String method, String url, int status, String correlationId) {
        logger.debug("  API: {} {} → {} | Trace: {}", method, url, status, correlationId);
    }
}
```

### Correlation ID — Advanced Debugging

When your TAF makes an API call and that call fails, log the correlation ID from the response header. Developers can then search server logs by that ID to see exactly what happened on the backend.

```java
Response response = apiClient.post("/api/merchant/onboard", payload);
String correlationId = response.getHeader("X-Trace-Id");
logger.debug("Onboarding call: status={}, traceId={}", response.getStatusCode(), correlationId);

if (response.getStatusCode() != 200) {
    logger.error("Onboarding failed. Server trace: {}", correlationId);
    // Developer searches server logs with this ID
}
```

### Allure Report Integration

```java
// AllureHelper.java — Core Libraries layer
public class AllureHelper {

    public static void attachScreenshot(AppiumDriver driver, String name) {
        byte[] screenshot = ((TakesScreenshot) driver).getScreenshotAs(OutputType.BYTES);
        Allure.addAttachment(name, "image/png", new ByteArrayInputStream(screenshot), ".png");
    }

    public static void attachLog(String name, String content) {
        Allure.addAttachment(name, "text/plain", content);
    }

    @Step("{description}")
    public static void step(String description) {
        // Appears as a named step in the Allure report
    }
}
```

### Test Progress Report — Required Content

A report published after every test run must contain:
1. Test results — pass / fail / skip / blocked per test and per suite
2. SUT version and build number
3. Test environment configuration used
4. Which tests failed and the failure reason
5. Correlation IDs for any API failures
6. Trend comparison to the previous run (pass rate delta)
7. Screenshot or video attached to every failed test

---

## 15. Risk Management in Test Automation

### Deployment Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Firewall blocks TAF → Appium server | Tests cannot start | Pre-run connectivity check. Alert and abort early rather than failing silently. |
| Device battery dies mid-run | Partial suite execution | Monitor device health in `@BeforeClass`. Alert if battery < 20%. |
| Auto-update on device changes UI | All tests using that element break | Pin OS version in capabilities. Separate environment for upgrade testing. |
| Wrong TAF version deployed | Tests test the wrong features | Align testware tags to SUT release tags. CI/CD picks up the matching branch. |
| Hardcoded timeouts too short on slow CI | Flaky failures | All timeouts from `config.properties` — easily tunable per environment. |
| Appium version incompatibility | Tests fail with cryptic driver errors | Pin Appium client and server versions. Test upgrades in a branch first. |

### Flaky Tests — The Most Expensive Risk

A flaky test is one that passes sometimes and fails sometimes without any change to the SUT. It destroys trust in the test suite.

**Common causes and fixes:**

| Cause | Fix |
|---|---|
| `Thread.sleep` with too short a value | Replace with FluentWait |
| Shared test data between tests | Create fresh data per test in `@BeforeMethod` |
| Test order dependency | Make every test independent — no shared state |
| Race condition in the SUT | Subscribe to the completion event rather than guessing timing |
| XPath locator breaks on minor UI update | Switch to accessibility ID |
| Animation not complete when test acts | Ask dev to add accessibility ID, or disable animations in test env |

**The flaky test protocol:**
1. Move the test out of the active suite immediately — it is poisoning the pipeline
2. Tag it `@Flaky` and log a defect
3. Investigate in isolation with `DEBUG` logging enabled
4. Fix root cause — never just increase the timeout as a permanent solution
5. Re-enable only after three consecutive clean runs

---

## 16. Continuous Improvement

### When to Improve Your TAF

After the suite is running stably, improve in this order:

1. **Scripting approach** — still using linear scripting? Migrate to structured (POM) then data-driven
2. **Test execution speed** — suite taking too long? Parallelise. Remove duplicate tests. Split into batches.
3. **Verification methods** — reimplementing the same assertions? Create shared `AssertionHelper` methods
4. **Library updates** — regularly review Appium client, TestNG, Allure versions. Pilot first, adopt with a plan.
5. **Setup / teardown** — repeated code before every test? Move to `@Before` methods using API calls
6. **Documentation** — every public method should have a Javadoc comment

### Test Histogram

A visual history of test results across many runs. Shows which tests are fragile (flip between pass/fail), which are stable, and which are permanently broken.

**How to read it:**

| Pattern | Meaning | Action |
|---|---|---|
| Consistently green | Stable, reliable | No action needed |
| Frequently flips | Flaky — race condition or data dependency | Investigate and fix |
| Consistently red | Broken — SUT defect or outdated test | Log defect or update test |
| Recently went red | Regression introduced by last SUT change | Raise with dev team |

Use Allure's built-in trend view, or your CI/CD platform's test results history for this.

### AI-Assisted Improvements

Modern tools like Healenium can detect when a locator has changed and suggest or auto-apply the new selector. This is called self-healing automation. Mention it in architect discussions as the forward direction of the field — but do not rely on it as a substitute for well-maintained accessibility IDs.

---

## 17. Test Scripting Approaches — Maturity Ladder

These are in order from least to most mature. Most professional projects should be at Structured Scripting or above.

| Approach | How it works | When to use | Pros | Cons |
|---|---|---|---|---|
| Capture / Playback | Record user actions, replay them | Proof of concept only | Zero coding needed | Breaks on any UI change. Cannot scale. |
| Linear Scripting | Write scripts with no reusable libraries | Very small scope | Easy to start | Impossible to maintain at scale |
| Structured Scripting | Reusable libraries and screen objects (POM) | All professional projects | Maintainable, scalable | Requires programming knowledge |
| Data-Driven Testing | Same script, multiple data inputs from CSV/JSON | High-volume form testing | Easily extend coverage | Requires good test data management |
| Keyword-Driven Testing | Tests are tables of keywords that TAEs implement | Non-technical stakeholder involvement | Business analysts can author tests | Complex to implement. High maintenance overhead at scale. |
| BDD | Given / When / Then in feature files | Business / Dev / QA collaboration | Shared language across roles | Often misused as just a syntax style without actual collaboration |
| TDD | Write failing test first, implement to pass | Developer component testing | Forces testability into design | Requires discipline. Slower initial development. |

---

## 18. API and Contract Testing

### Why API Tests Are More Valuable Than UI Tests for Backend Logic

- 10–50x faster than UI tests
- No flakiness from animations, screen transitions, or device orientation
- Test business logic without the UI layer in the way
- Catch backend defects before they surface in the UI

### Contract Testing — The Most Important Concept for Microservices

**The problem:** Service A and Service B are developed by different teams. Service A calls Service B's API. Both teams deploy independently. Service B changes its response format without telling Service A. Production breaks.

**Contract testing solves this.** A contract is an agreed record of the interactions between two services. Both sides verify they honour it independently — before deployment.

| Approach | Who defines the contract | When to use |
|---|---|---|
| Consumer-driven | Consumer defines what it expects from the provider | When you control the consumer and want to protect against provider changes |
| Provider-driven | Provider defines what it offers | When you are building an API and want to document your contract for consumers |

**Tools:** Pact (Java, TypeScript, and more)

### Schema Validation

Schema validation checks that an API response matches a defined structure — correct field names, correct types, required fields present, value ranges enforced.

It replaces dozens of individual field assertions with a single validation call.

```java
// Without schema validation — verbose
Assert.assertNotNull(response.jsonPath().getString("merchant.id"));
Assert.assertEquals(response.jsonPath().getString("merchant.status"), "PENDING");
Assert.assertNotNull(response.jsonPath().getString("merchant.createdAt"));
// ... 20 more lines for a complex response

// With schema validation — concise
given()
    .when().get("/api/merchant/" + merchantId)
    .then()
    .statusCode(200)
    .body(matchesJsonSchemaInClasspath("schemas/merchant-response-schema.json"));
```

---

## 19. Static Analysis

Static analysis scans your code without executing it. It finds bugs, security violations, and style issues before a single test runs.

**Apply to both the SUT and the TAF code.** Test automation code has the same security risks — a plaintext password in a test script is just as dangerous as one in production code.

### What Static Analysis Catches in TAF Code

| Issue | Example | Tool |
|---|---|---|
| Hardcoded credentials | `String pass = "Admin123"` in a test file | SonarQube, SpotBugs |
| Unreachable assertions | `Assert.assertTrue(false)` that always fails | PMD |
| Thread.sleep usage | Automated flagging of `Thread.sleep` in committed code | Checkstyle |
| Unused imports / variables | Dead code that confuses maintainers | IntelliJ inspections, SonarQube |
| Missing null checks | Potential NPEs in wait helper chains | SpotBugs |

### Severity Levels

| Level | Action |
|---|---|
| Critical | Block the build. Fix before merge. |
| High | Fix in the same sprint. |
| Medium | Log as tech debt. Fix in next sprint. |
| Low | Fix when touching the file. |

---

## 20. Practical Project Structure — Java / Appium

```
autara-appium/
│
├── pom.xml                              ← Maven dependencies and build config
│
├── src/
│   ├── main/java/                       ← LAYER 3: Core Libraries
│   │   └── com.autara.automation/
│   │       ├── core/
│   │       │   ├── DriverFactory.java   ← Singleton + Facade
│   │       │   ├── CapabilityManager.java
│   │       │   ├── ConfigManager.java
│   │       │   └── AppiumEventListener.java
│   │       ├── helpers/
│   │       │   ├── WaitHelper.java      ← FluentWait utility
│   │       │   ├── AllureHelper.java
│   │       │   ├── ApiClient.java
│   │       │   └── TestDataLoader.java
│   │       └── logging/
│   │           └── AppiumLogger.java
│   │
│   └── test/java/                       ← LAYERS 1 & 2
│       └── com.autara.automation/
│           ├── base/
│           │   ├── BaseTest.java        ← @BeforeSuite, @AfterSuite, listeners
│           │   └── BaseScreen.java      ← common screen methods
│           │
│           ├── screens/                 ← LAYER 2: Screen Objects (POM)
│           │   ├── LoginScreen.java
│           │   ├── HomeScreen.java
│           │   ├── BusinessInfoScreen.java
│           │   ├── VerificationScreen.java
│           │   ├── AvailabilityScreen.java
│           │   └── StripeConnectScreen.java
│           │
│           ├── flows/                   ← LAYER 2: Flow Models
│           │   ├── AuthFlow.java
│           │   └── MerchantOnboardingFlow.java
│           │
│           └── tests/                   ← LAYER 1: Test Scripts
│               ├── auth/
│               │   └── LoginTest.java
│               ├── onboarding/
│               │   ├── BusinessInfoTest.java
│               │   ├── VerificationTest.java
│               │   ├── AvailabilityTest.java
│               │   └── StripeConnectTest.java
│               └── e2e/
│                   └── FullOnboardingTest.java
│
└── src/test/resources/
    ├── capabilities/
    │   ├── android.capabilities.json
    │   └── ios.capabilities.json
    ├── fixtures/
    │   └── testData.json
    ├── config/
    │   ├── config.dev.properties
    │   └── config.staging.properties
    ├── schemas/
    │   └── merchant-response-schema.json
    ├── featureFlags.properties
    └── suites/
        ├── smoke.xml
        ├── regression.xml
        └── onboarding.xml
```

### Key Files — Complete Implementations

**BaseScreen.java:**
```java
public abstract class BaseScreen {

    protected final AppiumDriver driver;
    protected final WaitHelper waitHelper;
    protected final AppiumLogger logger;

    public BaseScreen(AppiumDriver driver) {
        this.driver     = driver;
        this.waitHelper = new WaitHelper(driver);
        this.logger     = new AppiumLogger(this.getClass().getSimpleName());
        PageFactory.initElements(new AppiumFieldDecorator(driver), this);
    }

    protected MobileElement waitForVisible(By locator) {
        return waitHelper.waitForVisible(locator);
    }

    protected MobileElement waitForVisible(By locator, int timeoutSeconds) {
        return waitHelper.waitForVisible(locator, timeoutSeconds);
    }

    protected void scrollDown() {
        Dimension size = driver.manage().window().getSize();
        int startY = (int) (size.height * 0.8);
        int endY   = (int) (size.height * 0.2);
        int centerX = size.width / 2;
        new TouchAction<>(driver)
            .press(PointOption.point(centerX, startY))
            .waitAction(WaitOptions.waitOptions(Duration.ofMillis(800)))
            .moveTo(PointOption.point(centerX, endY))
            .release()
            .perform();
    }

    protected void takeScreenshot(String name) {
        AllureHelper.attachScreenshot(driver, name);
    }
}
```

**android.capabilities.json:**
```json
{
  "platformName": "Android",
  "appium:deviceName": "Pixel_7_API_33",
  "appium:platformVersion": "13.0",
  "appium:app": "${APP_PATH}",
  "appium:automationName": "UiAutomator2",
  "appium:newCommandTimeout": 60,
  "appium:noReset": false,
  "appium:fullReset": false,
  "appium:autoGrantPermissions": true
}
```

**smoke.xml:**
```xml
<!DOCTYPE suite SYSTEM "https://testng.org/testng-1.0.dtd">
<suite name="Autara Smoke Suite" parallel="none" verbose="1">
    <listeners>
        <listener class-name="com.autara.automation.listeners.TestListener"/>
        <listener class-name="io.qameta.allure.testng.AllureTestNg"/>
    </listeners>
    <test name="Core Smoke Tests">
        <groups>
            <run><include name="smoke"/></run>
        </groups>
        <classes>
            <class name="com.autara.automation.tests.auth.LoginTest"/>
            <class name="com.autara.automation.tests.onboarding.BusinessInfoTest"/>
        </classes>
    </test>
</suite>
```

---

## 21. Practical Project Structure — TypeScript / Playwright

```
autara-playwright/
│
├── playwright.config.ts                 ← environments, retries, reporters
│
├── tests/                               ← LAYER 1: Test Scripts
│   ├── auth/
│   │   └── login.spec.ts
│   ├── onboarding/
│   │   ├── business-info.spec.ts
│   │   └── stripe-connect.spec.ts
│   └── e2e/
│       └── full-onboarding.spec.ts
│
├── pages/                               ← LAYER 2: Page Objects (POM)
│   ├── BasePage.ts
│   ├── LoginPage.ts
│   ├── BusinessInfoPage.ts
│   └── StripeConnectPage.ts
│
├── flows/                               ← LAYER 2: Flow Models
│   ├── AuthFlow.ts
│   └── MerchantOnboardingFlow.ts
│
├── helpers/                             ← LAYER 3: Core Libraries
│   ├── ApiClient.ts
│   ├── Logger.ts
│   └── TestDataLoader.ts
│
└── fixtures/
    ├── testData.json
    ├── env.dev.json
    └── env.staging.json
```

---

## 22. Interview Reference — Questions and Answers

### Architecture Questions

**"Walk me through how you would architect a mobile automation project from scratch."**

> "I follow the three-layer TAF model. Test Scripts sit at the top — these are my TestNG spec classes and they only call Flow Models or Screen Objects. They contain no locators and no driver calls. The Business Logic layer contains Screen Objects using the Page Object Model and Flow Models for multi-step user journeys. The Core Libraries layer is SUT-independent — DriverFactory, WaitHelper, Logger, CapabilityManager — and is reusable across multiple projects.
>
> For design patterns I use Singleton in DriverFactory to ensure one driver session across the suite, and Facade to hide the platform-specific capability setup from all callers. Screen Objects apply POM with accessibility IDs as the preferred locator strategy. I apply SOLID throughout — each class has one responsibility, core libraries are extended not modified.
>
> For CI/CD I put component tests and static analysis in the build phase and system tests in the deploy phase, with a nightly full regression on a schedule."

---

**"What is the Page Object Model and why do you use it?"**

> "POM is a design pattern where each screen in the application has a corresponding class. Locators are private fields inside that class. Test scripts never contain raw selectors — they only call methods that describe what a user does, like `loginScreen.login(user, pass)`.
>
> The benefit is maintainability. When the UI changes, I update one class, not fifty test files. It also applies the Single Responsibility Principle — the screen class owns all knowledge of that screen's structure. I extend this with the Flow Model pattern for multi-step journeys so those steps are reusable and named clearly across tests."

---

**"Explain SOLID in test automation."**

> "S — each screen object has one responsibility. LoginScreen handles login only, not navigation or validation of other screens.
> O — I extend BaseScreen to add platform support rather than modifying it with if-else platform checks.
> L — any screen object can substitute its parent BaseScreen without breaking behaviour.
> I — mobile screens don't implement web-only methods. Interfaces are focused.
> D — tests depend on an IDriverFactory interface, not AndroidDriver directly. Swapping to a remote Appium grid requires zero test changes."

---

**"What is the difference between Implicit, Explicit, and Fluent wait?"**

> "These are Selenium's three wait mechanisms. Implicit wait is a global timeout applied silently to every findElement call — it is essentially hardcoded and you should never mix it with explicit waits because the timeouts compound unpredictably.
>
> Explicit wait — WebDriverWait — is targeted. You wait for a specific condition with its own timeout. Much better.
>
> Fluent wait is explicit wait with two extra controls: you set the polling interval and you specify which exceptions to ignore during retries. This is what I use by default in a WaitHelper class because it handles StaleElementReferenceException gracefully and lets me tune the poll frequency per use case.
>
> In Playwright the distinction largely disappears. Every expect() assertion has Fluent Wait behaviour built in and uses MutationObserver under the hood — so it is closer to event subscription than polling. That is why Playwright waits are more reliable than Selenium waits."

---

**"What is event subscription and how does it differ from polling?"**

> "With polling, the TAF repeatedly asks the SUT 'are you ready yet?' on a timer. There is always a gap between when the SUT becomes ready and when the next poll runs.
>
> With event subscription, the TAF goes idle and the SUT notifies it the instant something happens. Zero gap. Zero wasted checks.
>
> In Playwright this works via page.waitForResponse() subscribing to network events, or page.waitForEvent() for browser events. For custom application events, developers can fire document.dispatchEvent with a custom event type and the test subscribes to it.
>
> The limitation is that the SUT must support and fire meaningful events. That is a conversation you need to have with the dev team during project setup — it is part of the testability requirements."

---

**"How do you handle test data?"**

> "I never hardcode test data in test files — that is a clean code violation. Test data lives in JSON fixtures loaded by a TestDataLoader class. For environment-specific data I use config properties files, one per environment. Secrets like passwords live in environment variables, never in source code.
>
> For test setup I prefer creating data via API in a @BeforeMethod rather than through the UI — it is ten times faster and removes a whole layer of test dependency. Cleanup happens in @AfterMethod using the same API. This keeps tests independent and the environment clean."

---

**"What is contract testing?"**

> "Contract testing verifies that two services can communicate and the data format between them matches an agreed contract. Unlike schema validation which only checks structure, contract testing captures the full interaction and lets both the consumer and the provider independently verify they honour it.
>
> I would use it in a microservices architecture to catch integration defects before system integration testing — finding them earlier in the SDLC where they are cheaper to fix. The main tools are Pact. There are two approaches: consumer-driven where the consumer defines expectations, and provider-driven where the provider publishes its contract."

---

### Scenario Questions

**"A test is failing intermittently in CI but always passes locally. What do you do?"**

> "First I isolate it — run it standalone in CI with DEBUG logging enabled. I check whether it has a timing dependency on shared test data, a race condition exposed by CI's slower startup, or a Thread.sleep that is too short for the CI environment. I also check whether it depends on the order of previous tests.
>
> If it is timing, I replace the hardcoded wait with FluentWait and increase the timeout in the CI config properties. If it is data, I make the test create its own fresh data in @BeforeMethod via API. If it is test order dependency, I refactor to eliminate shared state. I never just increase the timeout as the final fix — I find the root cause.
>
> In the meantime the test is tagged @Flaky and removed from the blocking suite so it does not poison the pipeline."

---

**"The developers renamed all the button accessibility IDs in the latest release. How bad is the impact?"**

> "If the project has proper POM, the impact is contained. Every accessibility ID lives in a screen object class, not in test files. I update the ID in one class per screen. All the tests using that screen are fixed automatically.
>
> If the project does not have POM and locators are scattered through test files, this is a much larger change — which is exactly why POM is non-negotiable from day one.
>
> Going forward, I would work with the dev team to establish a naming convention for accessibility IDs and treat them as a public API. Changes to them should be flagged as breaking changes requiring a testware update."

---

## 23. The Architect Prompt — Reusable Project Bootstrap

Paste this at the start of any new AI-assisted session to establish context without re-explaining everything.

```
## Context

I am a Senior SDET, ISTQB CTAL-TAE v2.0 certified, working on [PROJECT NAME].
I apply the following without needing explanations:
- 3-layer TAF: Test Scripts → Business Logic (Screen Objects + Flow Models) → Core Libraries
- gTAA capabilities: Test Generation, Definition, Execution, Adaptation
- Patterns: POM, Flow Model, Facade, Singleton
- OOP: Encapsulation, Abstraction, Inheritance, Polymorphism
- SOLID: S/O/L/I/D with TAF examples
- Clean Code: no hardcoding, meaningful names, 6-level logging, short methods
- Wait strategy: dynamic polling preferred, no hardcoded waits, event subscription where SUT supports it
- CI/CD: component tests in build phase, system tests in deploy phase, nightly regression
- Config management: feature toggles, env-specific caps, version-aligned testware tags

## Project details

Language:     [TypeScript]
Framework:    [Playwright]
Test runner:  [Playwright runner]
Build tool:   [npm]
Reporting:    [Allure]
CI/CD:        [GitHub Actions/ Azure DevOps]
SUT:          [Brief description of what the app does]

## Standards to enforce in all code

- DriverFactory must be Singleton + Facade
- No locators in test classes
- No hardcoded wait — use dynamic polling
- No hardcoded strings — config from properties, data from JSON fixtures
- Use hooks, e.g., @beforeEach, @AfterAll etc

## Task

[Your specific request here]
```

---

## 24. Glossary

| Term | Definition |
|---|---|
| TAF | Test Automation Framework — the complete system that runs your tests |
| SUT | System Under Test — the application being tested |
| gTAA | Generic Test Automation Architecture — the formal ISTQB model describing TAF capabilities |
| TAE | Test Automation Engineer |
| POM | Page Object Model — design pattern encapsulating screen locators in classes |
| Flow Model | Design pattern for reusable multi-step user journeys |
| Facade | Design pattern that hides complex subsystems behind a simple interface |
| Singleton | Design pattern ensuring only one instance of a class exists |
| SOLID | Five OOP design principles: Single Responsibility, Open/Closed, Liskov, Interface Segregation, Dependency Inversion |
| Implicit Wait | Selenium: global timeout on every findElement. Avoid mixing with explicit wait. |
| Explicit Wait | Selenium/Appium: targeted wait for a specific condition. Correct default approach. |
| Fluent Wait | Advanced explicit wait with custom polling interval and exception ignoring. Preferred. |
| Event Subscription | TAF goes idle; SUT fires a notification. Most reliable. Requires SUT support. |
| MutationObserver | Browser API for watching DOM changes. Used internally by Playwright for reliable waiting. |
| Contract Testing | Verifying that two services honour an agreed interaction contract. Tools: Pact. |
| Schema Validation | Verifying API response structure matches a defined schema. Replaces many individual assertions. |
| Test Histogram | Visual history of test results across runs. Used to identify fragile tests. |
| Self-healing | AI-based mechanism that detects changed locators and updates them automatically. |
| Correlation ID | Unique identifier linking a TAF log entry to a corresponding server log entry. |
| Testability | Non-functional requirement describing how easy the SUT is to test — observability, controllability, architecture transparency. |
| TAS | Test Automation Solution — the complete implementation including TAF, testware, and configuration |
| Testware | All artefacts produced by test activities — scripts, data, configs, reports |
| Feature Toggle | Configuration flag that enables or disables a test group per release or environment |
| In-sprint Automation | Agile practice of completing test automation for a story within the same sprint it is developed |
| BDD | Behaviour-Driven Development — Given/When/Then format. Tools: Cucumber, JBehave. |
| TDD | Test-Driven Development — write the failing test first, then implement to make it pass |
| DDT | Data-Driven Testing — same test logic executed with multiple input data sets |
| KDT | Keyword-Driven Testing — tests defined as tables of keywords that TAEs implement |
| Static Analysis | Code scanning without execution to find bugs, security issues, and style violations. Tools: SonarQube, SpotBugs, Checkstyle. |
| Canary Release | Production deployment strategy where new version is rolled out to a small % of users first |
| Blue/Green Deployment | Production strategy maintaining two identical environments — one live, one for new release |

---

*This document is a living reference. Update it when you encounter new patterns, new tools, or better explanations. The best architecture docs are the ones their authors actually read.*
