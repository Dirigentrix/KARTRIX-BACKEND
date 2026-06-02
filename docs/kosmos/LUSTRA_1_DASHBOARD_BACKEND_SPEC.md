# Lustra 1.0 Dashboard & Backend Specs

## Purpose
Lustra is the operator-facing dashboard for DARTRIX. It shows system health, agent activity, command history, and realtime collaboration signals in a presentation-ready UI.

## Stack
- Frontend: React
- Backend: Flask
- Realtime transport: Socket.IO
- Data exchange: JSON contracts
- Visualization layer: responsive cards, timelines, and status indicators

## Frontend scope
### Main views
- Overview dashboard
- Agent registry
- Live message stream
- Task queue
- Executive cockpit summary
- Resonance and activity visualizations

### UI principles
- fast to scan
- high contrast
- show system state before detail
- highlight active, waiting, and blocked items
- keep the showcase readable from a distance

### Recommended components
- status tiles
- activity feed
- timeline panel
- command composer
- event graph
- error banner
- deployment health strip

## Backend scope
### Flask responsibilities
- serve the dashboard API
- validate incoming commands
- expose agent state
- handle persistence for the demo
- forward realtime events into Socket.IO channels

### Suggested API routes
- GET /api/health
- GET /api/agents
- GET /api/events
- POST /api/command
- POST /api/escalate
- GET /api/resonance

## Socket.IO events
- connect
- disconnect
- agent:status
- agent:event
- task:queued
- task:running
- task:complete
- system:alert
- ceo:escalation

## Data objects
### Agent card
- id
- name
- role
- state
- last_seen
- current_task

### Event item
- id
- level
- source
- title
- details
- created_at

### Resonance snapshot
- channel
- score
- phase
- trend
- note

## Demo behavior
- opening the dashboard should immediately show current state
- triggering a command should create a visible realtime event
- failed validation should surface in a clear warning panel
- successful execution should update both the message feed and agent tiles

## Hackathon polish checklist
- stable loading state
- readable empty state
- clear labels for non-technical judges
- single-source-of-truth backend data
- no hidden interactions required for the demo
