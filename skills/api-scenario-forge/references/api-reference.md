# API references

Use these links as the source of truth for command names, arguments, JSON
schemas, supported behaviors, and verification tools. Read the relevant
section immediately before using that part of the workflow instead of relying
on copied command details in this skill.

## When discovering or controlling a browser MSW session

Read the [Browser CLI reference](https://msw-dev-tool-docs.vercel.app/docs/browser-cli)
when selecting a CDP target, inspecting browser session state, changing HTTP
or WebSocket scenarios, adding temporary handlers, or resetting a browser
session.

## When discovering or controlling a Node MSW session

Read the [Node CLI reference](https://msw-dev-tool-docs.vercel.app/docs/node-cli)
when listing Node sessions, selecting a PID, changing Node HTTP or WebSocket
scenarios, adding temporary handlers, or resetting a Node session.

## When choosing HTTP behaviors or response presets

Read [HTTP Mocking Scenarios](https://msw-dev-tool-docs.vercel.app/docs/http)
for loading, failure, alternative-data, passthrough, temporary-handler, and
dynamic-response workflows.

Read the [Handler Table reference](https://msw-dev-tool-docs.vercel.app/docs/handler-table)
when choosing behavior names, supported HTTP status presets, custom response
fields, enable/disable semantics, or reset behavior.

## When controlling WebSocket scenarios

Read [WebSocket Mocking Scenarios](https://msw-dev-tool-docs.vercel.app/docs/websocket)
when configuring endpoints, listeners, message branches, schedules, close
responses, or temporary WebSocket handlers.

## When verifying the application in a browser

Read the [Chrome DevTools MCP documentation](https://developer.chrome.com/docs/devtools/agents)
when navigating, inspecting DOM and console state, observing network activity,
interacting with the application, or collecting screenshots as verification
evidence.

If a command or payload in this skill conflicts with a linked reference, follow
the linked documentation and report the discrepancy.
