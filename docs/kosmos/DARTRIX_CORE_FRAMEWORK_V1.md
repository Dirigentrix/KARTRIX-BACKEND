# DARTRIX Core Framework v1.0

## Purpose
DARTRIX Core Framework v1.0 is the Python orchestration layer for the KARTRIX-BACKEND ecosystem. It coordinates agents, validates messages, routes contracts, and keeps the system demoable under hackathon conditions.

## Design goals
- predictable orchestration
- clear message contracts
- low-friction demo startup
- testable agent lifecycle
- easy integration with dashboard and realtime events

## Core primitives

### 1. Orchestrator
The Orchestrator owns system startup, shutdown, routing, and escalation. It is responsible for:
- loading the agent registry
- booting the message bus
- dispatching tasks to agents
- collecting responses
- escalating unresolved items to CEO Cockpit

### 2. MessageBus
The MessageBus is the internal transport layer. It moves:
- commands
- observations
- status updates
- validation results
- alerts

Recommended message shape:
~~~json
{
  "type": "task|status|alert|response",
  "source": "agent-name",
  "target": "agent-name|broadcast|ceo",
  "payload": {},
  "timestamp": "ISO-8601"
}
~~~

### 3. Agent
Each agent follows the same lifecycle:
- initialize
- validate input
- execute
- return result
- report status

### 4. Contract
A contract is the normalized payload exchanged between components. It should contain:
- mission
- plan
- tasks
- filters
- sequence

### 5. Registry
The Registry stores agent metadata, capabilities, and activation state. It should answer:
- which agents exist
- which agents are active
- which agent handles each category

## Runtime flow
1. Load configuration
2. Register agents
3. Open the bus
4. Validate the contract
5. Dispatch tasks
6. Collect outputs
7. Render dashboard status
8. Escalate if the flow stalls

## Suggested Python module layout
- dartrix_core.py
- message_bus.py
- contracts.py
- registry.py
- agents/
- tests/

## Demo priorities
- a clean startup path
- visible state transitions
- one happy-path task
- one validation failure
- one escalation to CEO Cockpit

## Hackathon acceptance criteria
- the framework starts without manual repair
- the message bus can route at least one end-to-end task
- the contract validator returns readable feedback
- the system is easy to explain in under two minutes
