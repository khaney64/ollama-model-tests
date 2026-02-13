# Greenfield Task: TaskFlow - Task Management Application

## Prompt

You are a senior full-stack developer. Generate a complete, working task management application called "TaskFlow" with the following specifications.

### Backend: C# ASP.NET Core 8 Web API

Create a minimal Web API project with:

**Task Model:**
- `Id` (Guid, auto-generated)
- `Title` (string, required, max 200 chars)
- `Description` (string, optional, max 2000 chars)
- `Priority` (enum: Low, Medium, High)
- `Category` (string, optional, max 100 chars)
- `DueDate` (DateTime?, optional)
- `IsComplete` (bool, default false)
- `CreatedAt` (DateTime, auto-set)
- `UpdatedAt` (DateTime, auto-set on modify)

**Endpoints:**
- `GET /api/tasks` - List all tasks. Support query params: `?category=X&priority=High&isComplete=true`
- `GET /api/tasks/{id}` - Get single task
- `POST /api/tasks` - Create task (validate required fields, return 201 + Location header)
- `PUT /api/tasks/{id}` - Update task (return 200)
- `DELETE /api/tasks/{id}` - Delete task (return 204)
- `PATCH /api/tasks/{id}/toggle` - Toggle IsComplete (return 200)
- `GET /api/tasks/stats` - Return `{ total, completed, pending, byPriority: { low, medium, high } }`

**Requirements:**
- In-memory storage (thread-safe `ConcurrentDictionary`)
- Proper HTTP status codes (400 for validation, 404 for not found)
- CORS enabled for `http://localhost:3000`
- Seed 5 sample tasks on startup
- Use minimal API style (not controllers)
- Include `Program.cs` and any model/service files needed

### Frontend: React + TypeScript

Create a React app (assume `create-react-app` or Vite with TypeScript):

**Components:**
- `TaskList` - Displays task cards in a grid/list
- `TaskCard` - Shows title, priority badge (color-coded: red=High, yellow=Medium, green=Low), category tag, due date, completion checkbox
- `TaskForm` - Add/edit form with all fields, validation
- `StatsBar` - Shows total/completed/pending counts
- `FilterBar` - Filter by category (dropdown) and priority (buttons)

**Features:**
- Fetch tasks from API on mount
- Add, edit, delete tasks via API
- Toggle completion with checkbox
- Filter by category and priority (client-side after fetch)
- Color-coded priority badges
- Responsive layout
- Show loading and error states

**Deliver all files** with their relative paths clearly indicated. Include:
- `package.json` with dependencies
- `tsconfig.json`
- All component files
- CSS/styles (inline or CSS modules)
- API client/service file

## Evaluation Criteria

| Criteria | Weight | Description |
|----------|--------|-------------|
| Completeness | 25% | All endpoints and components present |
| Compilability | 20% | Code compiles/runs without modification |
| Correctness | 20% | Endpoints return correct data, UI functions work |
| Code Quality | 15% | Clean architecture, separation of concerns |
| TypeScript | 10% | Proper typing, no `any` abuse |
| Config | 10% | Build files, project structure, CORS, etc. |

**Score each criterion 1-10 and calculate weighted total.**
