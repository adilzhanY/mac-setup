# Node.js Best Practices (Yoni Goldberg and contributors)

Legal source: https://github.com/goldbergyoni/nodebestpractices (MIT/CC licensed public repository). Read the README sections 1 (architecture), 2 (error handling), 3 (code style), 5 (production, titles and the TL;DRs present), 6 (security, titles), 7 (performance, titles). The second third of the README (detailed TL;DRs for 5.7 onward, sections 6 to 8 bodies) was cut off by the fetch.

## Key lessons used in languages/typescript/

- Structure by business component, three layers, the web layer (`req`/`res`) never reaches domain code; config validated at startup; TypeScript used thoughtfully. (node-runtime.md 2 and 3)
- Errors: async/await, extend `Error`, operational vs programmer errors, central handler, exit gracefully on unknown errors and let the platform restart, mature logger to stdout, catch `unhandledRejection`, validate arguments with a library, `return await` for full stack traces, subscribe to emitter and stream `error` events. (errors-and-async.md, node-runtime.md 4 and 7)
- Production: lock dependencies, use the platform's process supervisor, `NODE_ENV=production`, LTS Node, log to stdout, `npm ci`, request IDs in every log line. (node-runtime.md)
- Security: lint security rules, limit payload size and concurrency, no eval, avoid module loading by variable, careful child processes, hide error details, non-root, `node:` protocol for builtins, prevent unsafe redirects and evil regex. (node-runtime.md 8, modules-imports-exports.md 6)
- Code style: no effects at module load time; explicit module entry points. (modules-imports-exports.md 4 and 12)
