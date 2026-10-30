# Use The Index, Luke (Markus Winand)

- Legal URL: https://use-the-index-luke.com/ (the author's free web edition of "SQL Performance Explained")
- Read for kwx-developer data topic, 2026-10-30.

## What I read

- Concatenated keys: https://use-the-index-luke.com/sql/where-clause/the-equals-operator/concatenated-keys
- Greater, less and between (access vs filter predicates): https://use-the-index-luke.com/sql/where-clause/searching-for-ranges/greater-less-between-tuning-sql-access-filter-predicates
- Obfuscated conditions overview: https://use-the-index-luke.com/sql/where-clause/obfuscation
- No offset: https://use-the-index-luke.com/no-offset
- Fetching the next page (seek method): https://use-the-index-luke.com/sql/partial-results/fetch-next-page

Skipped: the B-tree anatomy chapters (models know them), vendor specific execution plan chapters.

## Key lessons

- A composite index serves only queries on its leftmost columns. Choose column order so one index serves as many queries as possible; one good composite index beats several single column ones (less space, cheaper writes).
- Equality columns first, range columns last. After a range condition, later index columns are only filter predicates, checked row by row while scanning leaf nodes; they do not narrow the scanned range. Read EXPLAIN for "Index Cond" vs "Filter".
- Obfuscated conditions defeat indexes: functions on columns (dates), mixed types (numeric strings), concatenated columns, "smart logic" (`col = :x OR :x IS NULL`), math on columns. Rewrite the predicate or index the expression.
- OFFSET reads and discards skipped rows and gives unstable pages when rows are inserted. Keyset (seek) pagination filters on the last seen sort key with a unique tie breaker: `WHERE (sale_date, sale_id) < (?, ?) ORDER BY sale_date DESC, sale_id DESC FETCH FIRST 10 ROWS ONLY`, with an index on `(sale_date, sale_id)`.
- Row value comparisons are index friendly in PostgreSQL (since 8.4) and Db2; MySQL evaluates them but cannot use them as an index range; Oracle and SQL Server need the expanded form.
- Paging requires a deterministic sort order. Cost of keyset paging: no jump to page N, and the client must carry the full cursor.

Used in: `data/indexes-and-queries.md` sections 1, 4, 6.
