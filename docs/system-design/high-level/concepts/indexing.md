# Indexing

## Theory

### Database Indexes Basics

A database index is a data structure that improves the speed of data retrieval operations on a table at the cost of additional storage and slower writes. Think of it like the index at the back of a book — instead of reading every page to find a topic, you look up the index to jump directly to the right page.

**Why Indexes Matter:**
Without an index, the database must perform a **full table scan** — reading every single row to find matching records. For a table with millions of rows, this can take seconds or minutes. With the right index, the same query runs in milliseconds.

```
Without Index (Full Table Scan):
  SELECT * FROM users WHERE email = 'john@example.com';
  → Scans all 10 million rows → ~5 seconds

With Index on email column:
  → B-Tree lookup → ~5 milliseconds (1000x faster)
```

**How Indexes Work (B-Tree — the most common):**
```
                    [M]
                   /   \
              [D, H]   [R, X]
             / | \     / | \
           [A-C][E-G][I-L] [N-Q][S-W][Y-Z]
                              ↓
                         Leaf nodes point
                         to actual table rows
```
The database traverses the tree from root to leaf, narrowing the search at each level. A B-Tree with millions of records typically has only 3-4 levels, meaning any lookup takes at most 3-4 disk reads.

**Index Types Explained:**
- **B-Tree Index**: Default. Supports equality (`=`) and range queries (`>`, `<`, `BETWEEN`). Works for most use cases.
- **Hash Index**: Only supports equality lookups. Faster than B-Tree for exact matches but cannot do range queries.
- **Full-Text Index**: Tokenizes text and builds an inverted index. Used for search (e.g., `MATCH AGAINST` in MySQL).
- **Geospatial Index (R-Tree)**: Indexes 2D/3D spatial data. Used for "find restaurants near me" queries.
- **Bitmap Index**: Stores bitmaps for each distinct value. Efficient for columns with few distinct values (e.g., gender, status).
- **Composite Index**: Index on multiple columns `(col_a, col_b)`. Order matters — follows the **leftmost prefix rule**.

**The Trade-off:**
```
  Reads:  Index makes them FASTER (O(log n) vs O(n))
  Writes: Index makes them SLOWER (must update index on INSERT/UPDATE/DELETE)
  Space:  Index uses ADDITIONAL storage (can be 10-30% of table size)
```

**When to Index:**
- Columns used in `WHERE` clauses frequently
- Columns used in `JOIN` conditions (foreign keys)
- Columns used in `ORDER BY` or `GROUP BY`
- High-cardinality columns (many distinct values)

**When NOT to Index:**
- Small tables (full scan is fast enough)
- Columns rarely used in queries
- Low-cardinality columns (unless using bitmap index)
- Write-heavy tables where read performance isn't critical

**Common Index Mistakes:**
- Over-indexing: Every column indexed → slow writes, wasted space
- Unused indexes: Indexes that no query ever uses
- Wrong composite order: `INDEX(a, b)` helps `WHERE a = ?` but not `WHERE b = ?`
- Not monitoring: Use `EXPLAIN` to verify indexes are actually being used

---

## Quick Reference

Data structure to speed up query performance.

**Types:**
- **B-Tree**: Balanced tree, default for most databases
- **Hash**: Fast equality lookups
- **Full-Text**: Text search
- **Geospatial**: Location-based queries
- **Bitmap**: Low-cardinality columns

**Trade-offs:**
- Faster reads
- Slower writes
- Additional storage

**Best Practices:**
- Index frequently queried columns
- Index foreign keys
- Use composite indexes for multiple columns
- Avoid over-indexing
- Monitor index usage
