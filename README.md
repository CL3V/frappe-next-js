# Frappe Next JS

A Frappe App to setup and manage Next.js frontends on your custom Frappe App.

## Installation

In your bench directory:

```bash
bench get-app frappe-next-js
bench install-app frappe_next_js
```

This will install the `Frappe Next JS` frappe app on your bench and enable custom bench CLI commands that will ease the process of attaching a Next.js frontend to your Frappe Application.

## Setting Up Next.js Frontend

To set up a new Next.js frontend, you can run the following command in your bench directory:

```bash
bench add-nextjs --app <app-name> --name frontend --typescript --tailwindcss

# or just run it and answer the prompts
bench add-nextjs
```

### Options

| Option                             | Description                    | Default     |
| ---------------------------------- | ------------------------------ | ----------- |
| `--app`                            | Name of the Frappe app         | (prompted)  |
| `--name`                           | Name of the frontend directory | `frontend`  |
| `--typescript / --no-typescript`   | Use TypeScript                 | (prompted)  |
| `--tailwindcss / --no-tailwindcss` | Use TailwindCSS                | (prompted)  |
| `--site`                           | Site name for API proxying     | `localhost` |

### What Gets Created

The command will:

1. **Scaffold a Next.js 15 project** with App Router
2. **Set up createResource pattern** (like frappe-ui) for Frappe backend integration
3. **Set up API proxying** for development (requests to `/api/*` proxy to Frappe)
4. **Include shadcn/ui components** (Button, Card, Input, Toast)
5. **Optionally configure TypeScript** for type safety
6. **Optionally set up TailwindCSS** for styling
7. **Create an app root `package.json`** with `postinstall`, `dev`, and `build` scripts
8. **Update `hooks.py`** with routing rules for the SPA
9. **Add npm scripts** to the bench root `package.json`

### Project Structure

After running the command, your app will have:

```
your_app/
├── package.json              # App root - delegates to frontend/
├── your_app/
│   ├── hooks.py              # Updated with routing rules
│   ├── api.py                # Guest-accessible API methods
│   └── www/
│       └── frontend/
│           └── index.html
└── frontend/
    ├── package.json
    ├── next.config.js
    ├── tailwind.config.js
    ├── tsconfig.json
    └── src/
        ├── app/
        │   ├── layout.tsx
        │   ├── page.tsx
        │   ├── globals.css
        │   └── login/
        │       └── page.tsx
        ├── lib/
        │   ├── frappe.tsx     # createResource, useFrappe, useListResource, useDocResource
        │   └── utils.ts
        ├── components/
        │   └── ui/            # shadcn/ui components
        └── hooks/
            └── use-toast.ts
```

## Development

Once the setup is complete, start the dev server from the app root:

```bash
cd apps/your_app && npm run dev
```

Or from the bench directory:

```bash
npm run dev:frontend
```

This will start the Next.js development server at `http://localhost:3000`.

### API Calls

Use the `useResource` hook (similar to frappe-ui's `createResource`):

```tsx
import { useResource, useFrappe } from "@/lib/frappe";

export default function MyComponent() {
  const { user, isLoggedIn } = useFrappe();

  const todos = useResource({
    method: "frappe.client.get_list",
    params: { doctype: "ToDo", fields: ["name", "description"] },
    auto: true,
  });

  if (todos.loading) return <p>Loading...</p>;

  return (
    <ul>
      {todos.data?.map((todo) => (
        <li key={todo.name}>{todo.description}</li>
      ))}
    </ul>
  );
}
```

## Building for Production

Build and export assets to Frappe's `www` directory:

```bash
cd apps/your_app && npm run build
```

Or from the bench directory:

```bash
bench build --app your_app
```

## Features

- **Next.js 15** with App Router and Turbopack
- **createResource pattern** (like frappe-ui) for API calls
- **shadcn/ui** component library included
- **TypeScript** support (optional)
- **TailwindCSS** support (optional)
- **Hot Module Replacement** during development
- **API Proxy** configuration for Frappe backend
- **Automatic routing** setup in Frappe hooks
- **Login page** with Frappe authentication

## License

MIT
# frappe-next-js
