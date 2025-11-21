# Clean Architecture


## Blogs and websites

- [A quick introduction to clean architecture](https://www.freecodecamp.org/news/a-quick-introduction-to-clean-architecture-990c014448d2/)
- [The SOLID Principles of Object-Oriented Programming Explained in Plain English](https://www.freecodecamp.org/news/solid-principles-explained-in-plain-english/)

- [SOLID Principles with Real Life Examples](https://www.geeksforgeeks.org/system-design/solid-principle-in-programming-understand-with-real-life-examples/)

- [What is Inversion of Control?](https://stackoverflow.com/questions/3058/what-is-inversion-of-control)
- [What is dependency injection?](https://stackoverflow.com/questions/130794/what-is-dependency-injection)



## Medium

- [The S.O.L.I.D Principles in Pictures](https://medium.com/backticks-tildes/the-s-o-l-i-d-principles-in-pictures-b34ce2f1e898)
- [The 7 Most Important Software Design Patterns](https://learningdaily.dev/the-7-most-important-software-design-patterns-d60e546afb0e)
- [Understanding Inversion of Control (IoC) Principle](https://medium.com/@amitkma/understanding-inversion-of-control-ioc-principle-163b1dc97454)



## Theory

### Key Concepts

- **What is web service?** - A software system designed to support interoperable machine-to-machine interaction over a network
- **What is MQ?** - Message Queue, a form of asynchronous service-to-service communication used in serverless and microservices architectures
- **What is SOAP web service?** - Simple Object Access Protocol, a messaging protocol for exchanging structured information in web services
- **What is REST web service?** - Representational State Transfer, an architectural style for designing networked applications using HTTP methods
- **What is WSDL?** - Web Services Description Language, an XML format for describing network services and their operations
- **What is Clean Architecture?** - A software design philosophy that separates concerns into layers, making code more maintainable and testable

### SOLID Principles

- **Single Responsibility Principle (SRP)** - A class should have only one reason to change, focusing on a single responsibility
- **Open-Closed Principle (OCP)** - Software entities should be open for extension but closed for modification
- **Liskov Substitution Principle (LSP)** - Objects of a superclass should be replaceable with objects of its subclasses without breaking functionality
- **Interface Segregation Principle (ISP)** - Clients should not be forced to depend on interfaces they don't use
- **Dependency Inversion Principle (DIP)** - High-level modules should not depend on low-level modules; both should depend on abstractions

### Common Design Patterns

- **Singleton** - Ensures a class has only one instance and provides global access to it
- **Factory Method** - Creates objects without specifying their exact classes
- **Strategy** - Defines a family of algorithms and makes them interchangeable
- **Observer** - Defines a one-to-many dependency between objects for automatic notifications
- **Builder** - Constructs complex objects step by step
- **Adapter** - Allows incompatible interfaces to work together
- **State** - Allows an object to alter its behavior when its internal state changes
