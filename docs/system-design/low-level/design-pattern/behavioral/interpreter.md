# Interpreter Design Pattern

## Blogs and websites

## Medium

## Youtube

- [40. Interpreter Design Pattern | LLD System Design | Design pattern explanation in Java](https://www.youtube.com/watch?v=fFlPm0pzQYI)

## Theory

### Interpreter Pattern

**Theory:** Defines a grammatical representation for a language and an interpreter to interpret sentences in the language.

**Why it's used:**
- To implement domain-specific languages (DSL)
- When grammar is simple and efficiency is not critical
- To interpret and evaluate expressions
- For scripting and configuration languages

**Diagram:**
```text
AbstractExpression
  ↓
┌─────────┼─────────┐
Terminal  NonTerminal
Expression Expression
```
*Terminal expressions hold values while non-terminal ones combine sub-expressions into sentences.*

**Real-Life Examples:**
- **SQL Parsers:** SQL query interpretation
- **Regular Expressions:** Regex pattern matching
- **Configuration Files:** Spring SpEL, JSP Expression Language
- **Mathematical Expressions:** Calculator apps parsing "2 + 3 * 4"
- **Rule Engines:** Business rule evaluation
- **Query Languages:** GraphQL, MongoDB query language
- **Scripting Languages:** Embedded scripting (Lua, JavaScript engines)

**Advantages:**
- Easy to change and extend grammar
- Grammar is explicit in code structure
- Easy to implement simple grammars
- Adding new expressions is straightforward

**Disadvantages:**
- Complex grammars become hard to maintain
- Performance issues (use parser generators for complex grammars)
- Can result in large number of classes
- Not suitable for complex languages

**When to Use:**
- Grammar is simple and well-defined
- Efficiency is not a critical concern
- You need to interpret domain-specific languages
- You're building expression evaluators or rule engines

---

### Pitfalls and Best Practices

**Pitfall:** Performance issues; maintenance nightmare for complex grammars
**Best Practice:** Use parser generators (ANTLR) for complex grammars; cache parsed results

---

### Testing Interpreter Pattern

- Test grammar rules individually
- Test expression parsing and evaluation
- Verify complex expressions
- Test error handling for invalid syntax

---

### Java Example

*Expressions compose into trees; interpret() evaluates the whole sentence.*

```java
interface Expression { int interpret(); }            // Abstract expression
class Number implements Expression {                 // Terminal expression
    private final int value;
    Number(int value) { this.value = value; }
    public int interpret() { return value; }
}
class Add implements Expression {                    // Non-terminal: combines operands
    private final Expression left, right;
    Add(Expression left, Expression right) { this.left = left; this.right = right; }
    public int interpret() { return left.interpret() + right.interpret(); }
}
```

---

### Second Java Example: Access-Control Rule Engine

*Business rules like "role == ADMIN OR (role == EDITOR AND owner == true)" become expression trees.*

```java
import java.util.Map;

interface Rule {                                       // Abstract expression
    boolean interpret(Map<String, String> ctx);
}

class Equals implements Rule {                         // Terminal: leaf comparison
    private final String key, expected;
    Equals(String key, String expected) {
        this.key = key; this.expected = expected;
    }
    public boolean interpret(Map<String, String> ctx) {
        return expected.equals(ctx.get(key));
    }
}

class And implements Rule {                            // Non-terminal: combines rules
    private final Rule left, right;
    And(Rule left, Rule right) { this.left = left; this.right = right; }
    public boolean interpret(Map<String, String> ctx) {
        return left.interpret(ctx) && right.interpret(ctx);
    }
}

class Or implements Rule {                             // Non-terminal: alternatives
    private final Rule left, right;
    Or(Rule left, Rule right) { this.left = left; this.right = right; }
    public boolean interpret(Map<String, String> ctx) {
        return left.interpret(ctx) || right.interpret(ctx);
    }
}

class Not implements Rule {                            // Non-terminal: negation
    private final Rule inner;
    Not(Rule inner) { this.inner = inner; }
    public boolean interpret(Map<String, String> ctx) {
        return !inner.interpret(ctx);
    }
}

class AccessDemo {                                     // Client: builds sentence once
    public static void main(String[] args) {
        // Rule: ADMIN, or EDITOR who owns the document.
        Rule canEdit = new Or(
            new Equals("role", "ADMIN"),
            new And(new Equals("role", "EDITOR"), new Equals("owner", "true"))
        );
        Map<String, String> ctx = Map.of("role", "EDITOR", "owner", "true");
        System.out.println(canEdit.interpret(ctx));    // true
        Map<String, String> guest = Map.of("role", "VIEWER", "owner", "false");
        System.out.println(canEdit.interpret(guest));  // false
    }
}
```

**Why this domain works:**
- Non-technical teams edit rules; code stays unchanged because grammar maps to classes.
- New operators (`Not`, `GreaterThan`) are new classes, not parser rewrites.
- Same tree can be interpreted, pretty-printed, or converted to SQL by swapping interpreters.

---

### Interpreter vs Visitor

| Aspect | Interpreter | Visitor |
|---|---|---|
| Purpose | Evaluate sentences of a small language or rule grammar | Add new operations over a stable object structure |
| Structure | Expression tree built from grammar (terminal + non-terminal) | Element hierarchy plus separate visitor carrying the operation |
| Adding behaviour | Add a new grammar rule as a new expression class | Add a new operation as a new visitor without touching elements |
| Typical use | Math evaluators, access-control rules, regex, SpEL, SQL filters | AST analysis, export (XML/JSON), tax/discount over cart items |
| Scaling limit | Class explosion and slow recursion for large grammars | Painful when element types change often (all visitors break) |

**Rule of thumb:** use Interpreter when the language is small and evaluation is the goal; use
Visitor when the object structure is stable and you keep adding operations over it.

---

### Interview Questions and Answers

**Q1: When is Interpreter the right choice versus a parser generator like ANTLR?**
**A:** Interpreter fits tiny, stable grammars (filters, permissions, calculator) where each rule
maps cleanly to a class. Once you need precedence, loops, or real syntax errors, switch to
ANTLR or a parser combinator — hand-rolled interpreters recurse poorly and are hard to debug.

**Q2: How do you avoid a class explosion as the grammar grows?**
**A:** Keep the grammar minimal, reuse generic nodes (`BinaryOp` with an operator enum instead of
`Add`/`Subtract`/`Multiply` classes), share flyweight terminals, and cache parsed trees so you
parse once and interpret many times.

**Q3: How would you handle invalid input like "role == " with a missing value?**
**A:** Fail at parse time, not interpret time: validate tokens while building the tree and throw
a `ParseException` with position and expected token. At interpretation, treat missing context
keys as explicit `false` or throw `MissingVariableException` depending on fail-open policy.

**Q4: When should you avoid the Interpreter pattern?**
**A:** Avoid it for complex languages, performance-critical parsing (regex engines, compilers),
or grammars that change weekly. Maintenance cost and recursion overhead quickly outweigh the
elegance — a script engine (GraalVM, Lua), rule engine (Drools), or proper parser wins.

**Key takeaway:** Interpreter turns grammar into composable expression objects — perfect for
small DSLs and rule engines, overkill for full languages.
