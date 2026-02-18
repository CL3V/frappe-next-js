"""
Next.js Boilerplate Templates for Frappe Next JS
With createResource pattern (like frappe-ui) and shadcn/ui
"""

# package.json template for Next.js project (TypeScript)
NEXTJS_PACKAGE_JSON = """{
  "name": "{{ spa_name }}",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev --turbopack -p 3000",
    "build": "next build",
    "build:frappe": "next build && npm run export-assets",
    "export-assets": "rm -rf ../{{ app_package }}/www/{{ spa_name }} && mkdir -p ../{{ app_package }}/www/{{ spa_name }} && cp -r out/* ../{{ app_package }}/www/{{ spa_name }}/",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "^15.1.0",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.1.0",
    "tailwind-merge": "^2.2.0",
    "lucide-react": "^0.468.0",
    "@radix-ui/react-slot": "^1.1.0",
    "@radix-ui/react-dialog": "^1.1.0",
    "@radix-ui/react-dropdown-menu": "^2.1.0",
    "@radix-ui/react-toast": "^1.2.0",
    "@radix-ui/react-label": "^2.1.0",
    "@radix-ui/react-select": "^2.1.0",
    "socket.io-client": "^4.8.0"
  },
  "devDependencies": {
    "@types/node": "^22.0.0",
    "@types/react": "^19.0.0",
    "@types/react-dom": "^19.0.0",
    "typescript": "^5.7.0",
    "eslint": "^9.0.0",
    "eslint-config-next": "^15.1.0",
    "tailwindcss": "^3.4.0",
    "postcss": "^8.4.0",
    "autoprefixer": "^10.4.0",
    "tailwindcss-animate": "^1.0.7"
  }
}
"""

# package.json template for Next.js project (JavaScript only)
NEXTJS_PACKAGE_JSON_JS = """{
  "name": "{{ spa_name }}",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev --turbopack -p 3000",
    "build": "next build",
    "build:frappe": "next build && npm run export-assets",
    "export-assets": "rm -rf ../{{ app_package }}/www/{{ spa_name }} && mkdir -p ../{{ app_package }}/www/{{ spa_name }} && cp -r out/* ../{{ app_package }}/www/{{ spa_name }}/",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "^15.1.0",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.1.0",
    "tailwind-merge": "^2.2.0",
    "lucide-react": "^0.468.0",
    "@radix-ui/react-slot": "^1.1.0",
    "@radix-ui/react-dialog": "^1.1.0",
    "@radix-ui/react-dropdown-menu": "^2.1.0",
    "@radix-ui/react-toast": "^1.2.0",
    "@radix-ui/react-label": "^2.1.0",
    "@radix-ui/react-select": "^2.1.0",
    "socket.io-client": "^4.8.0"
  },
  "devDependencies": {
    "eslint": "^9.0.0",
    "eslint-config-next": "^15.1.0",
    "tailwindcss": "^3.4.0",
    "postcss": "^8.4.0",
    "autoprefixer": "^10.4.0",
    "tailwindcss-animate": "^1.0.7"
  }
}
"""

# next.config.js template (unified: dev + production)
# - Dev: basePath empty so / works; rewrites proxy API to Frappe
# - Prod: basePath for Frappe; rewrites disabled (output: export incompatible)
NEXTJS_CONFIG = """/** @type {import('next').NextConfig} */
const isDev = process.env.NODE_ENV === 'development';
const frappeUrl = process.env.FRAPPE_URL || 'http://{{ site_name }}:{{ webserver_port }}';
const nextConfig = {
  reactStrictMode: true,
  output: 'export',
  trailingSlash: true,
  images: { unoptimized: true },
  basePath: isDev ? '' : '/{{ spa_name }}',
  assetPrefix: isDev ? undefined : '/{{ spa_name }}/',
  ...(isDev && {
    async rewrites() {
      return [
        { source: '/api/:path*', destination: `${frappeUrl}/api/:path*` },
        { source: '/assets/:path*', destination: `${frappeUrl}/assets/:path*` },
      ];
    },
  }),
  turbopack: { root: __dirname },
};

module.exports = nextConfig;
"""

# next.config.js for development (with rewrites) - alias for backward compat
NEXTJS_CONFIG_DEV = NEXTJS_CONFIG

# tsconfig.json template
NEXTJS_TSCONFIG = """{
  "compilerOptions": {
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "paths": { "@/*": ["./src/*"] }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
"""

# API module for guest-accessible methods (SPA auth/connection check)
NEXTJS_API_PY = '''"""API methods for Next.js frontend - allow guest for auth and connection check."""

import frappe


@frappe.whitelist(allow_guest=True)
def get_logged_user():
    """Return current user (Guest when not logged in). Required for SPA auth state."""
    return frappe.session.user


@frappe.whitelist(allow_guest=True)
def check_backend():
    """Return System Settings setup_complete. Safe for guest - used for connection status."""
    try:
        return frappe.db.get_value("System Settings", None, "setup_complete")
    except Exception:
        return None
'''

# .env.local template
NEXTJS_ENV_LOCAL = """# Frappe Backend URL
NEXT_PUBLIC_FRAPPE_URL=http://{{ site_name }}:{{ webserver_port }}
FRAPPE_URL=http://{{ site_name }}:{{ webserver_port }}
NEXT_PUBLIC_SITE_NAME={{ site_name }}
"""

# Main layout.tsx (App Router)
NEXTJS_LAYOUT_TSX = """import React from 'react';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import { FrappeProvider } from '@/lib/frappe';
import { Toaster } from '@/components/ui/toaster';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: '{{ app_title }}',
  description: 'Next.js Frontend for {{ app_name }}',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <FrappeProvider>
          {children}
          <Toaster />
        </FrappeProvider>
      </body>
    </html>
  );
}
"""

# Main layout.js (App Router - JavaScript)
NEXTJS_LAYOUT_JS = """import { Inter } from 'next/font/google';
import './globals.css';
import { FrappeProvider } from '@/lib/frappe';
import { Toaster } from '@/components/ui/toaster';

const inter = Inter({ subsets: ['latin'] });

export const metadata = {
  title: '{{ app_title }}',
  description: 'Next.js Frontend for {{ app_name }}',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <FrappeProvider>
          {children}
          <Toaster />
        </FrappeProvider>
      </body>
    </html>
  );
}
"""

# Main page.tsx (App Router) - Using createResource pattern
NEXTJS_PAGE_TSX = """'use client';

import Link from 'next/link';
import { useResource, useFrappe } from '@/lib/frappe';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { useToast } from '@/hooks/use-toast';

function AppNotInstalled() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8">
      <Card className="w-full max-w-2xl">
        <CardHeader className="text-center">
          <CardTitle className="text-4xl font-bold">{{ app_title }}</CardTitle>
          <CardDescription className="text-lg text-amber-600">App is not installed on this site</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="bg-amber-50 border border-amber-200 rounded-lg p-4">
            <p className="text-amber-800 font-medium mb-2">The app &quot;{{ app_name }}&quot; has been added to bench but is not yet installed on this site.</p>
            <p className="text-amber-700 text-sm">Run the following command to install it:</p>
          </div>
          <div className="bg-muted rounded-lg p-4 font-mono text-sm">
            <p>bench --site <span className="text-primary">your-site-name</span> install-app {{ app_name }}</p>
          </div>
          <div className="bg-muted rounded-lg p-4 text-sm text-muted-foreground space-y-1">
            <p>After installing, restart bench:</p>
            <p className="font-mono">bench restart</p>
          </div>
        </CardContent>
      </Card>
    </main>
  );
}

export default function Home() {
  const { user, isLoggedIn, logout } = useFrappe();
  const { toast } = useToast();

  const systemSettings = useResource({
    method: '{{ app_package }}.api.check_backend',
    params: {},
    auto: true,
  });

  const isNotInstalled = systemSettings.error?.message?.includes('not installed');

  const handleLogout = async () => {
    try {
      await logout();
      toast({ title: 'Logged out', description: 'You have been logged out successfully' });
    } catch (error) {
      toast({ title: 'Error', description: 'Logout failed', variant: 'destructive' });
    }
  };

  if (isNotInstalled) return <AppNotInstalled />;

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8">
      <Card className="w-full max-w-2xl">
        <CardHeader className="text-center">
          <CardTitle className="text-4xl font-bold">Welcome to {{ app_title }}</CardTitle>
          <CardDescription className="text-lg">Your Next.js frontend for Frappe is ready!</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="bg-muted rounded-lg p-4 text-center">
            {isLoggedIn ? (
              <p className="text-green-600 font-medium">Logged in as: {user}</p>
            ) : (
              <p className="text-muted-foreground">Not logged in (Guest)</p>
            )}
          </div>
          <div className="bg-muted rounded-lg p-4 text-center">
            {systemSettings.loading ? (
              <p className="text-muted-foreground">Connecting to Frappe backend...</p>
            ) : systemSettings.error ? (
              <p className="text-destructive">Unable to connect to Frappe backend</p>
            ) : (
              <p className="text-green-600 font-medium">Connected to Frappe!</p>
            )}
          </div>
          <div className="flex justify-center gap-4">
            {isLoggedIn ? (
              <Button variant="destructive" onClick={handleLogout}>Logout</Button>
            ) : (
              <Link href="/login"><Button>Login</Button></Link>
            )}
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <a href="https://nextjs.org/docs" target="_blank" rel="noopener noreferrer">
              <Button variant="outline" className="w-full h-auto p-4 flex flex-col items-start">
                <span className="font-semibold">Next.js Docs</span>
                <span className="text-muted-foreground text-sm">Learn about Next.js features</span>
              </Button>
            </a>
            <a href="https://frappeframework.com/docs" target="_blank" rel="noopener noreferrer">
              <Button variant="outline" className="w-full h-auto p-4 flex flex-col items-start">
                <span className="font-semibold">Frappe Docs</span>
                <span className="text-muted-foreground text-sm">Learn about Frappe Framework</span>
              </Button>
            </a>
          </div>
        </CardContent>
      </Card>
    </main>
  );
}
"""

# Main page.js (App Router - JavaScript)
NEXTJS_PAGE_JS = """'use client';

import Link from 'next/link';
import { useResource, useFrappe } from '@/lib/frappe';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { useToast } from '@/hooks/use-toast';

function AppNotInstalled() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8">
      <Card className="w-full max-w-2xl">
        <CardHeader className="text-center">
          <CardTitle className="text-4xl font-bold">{{ app_title }}</CardTitle>
          <CardDescription className="text-lg text-amber-600">App is not installed on this site</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="bg-amber-50 border border-amber-200 rounded-lg p-4">
            <p className="text-amber-800 font-medium mb-2">The app &quot;{{ app_name }}&quot; has been added to bench but is not yet installed on this site.</p>
            <p className="text-amber-700 text-sm">Run the following command to install it:</p>
          </div>
          <div className="bg-muted rounded-lg p-4 font-mono text-sm">
            <p>bench --site <span className="text-primary">your-site-name</span> install-app {{ app_name }}</p>
          </div>
          <div className="bg-muted rounded-lg p-4 text-sm text-muted-foreground space-y-1">
            <p>After installing, restart bench:</p>
            <p className="font-mono">bench restart</p>
          </div>
        </CardContent>
      </Card>
    </main>
  );
}

export default function Home() {
  const { user, isLoggedIn, logout } = useFrappe();
  const { toast } = useToast();

  const systemSettings = useResource({
    method: '{{ app_package }}.api.check_backend',
    params: {},
    auto: true,
  });

  const isNotInstalled = systemSettings.error?.message?.includes('not installed');

  const handleLogout = async () => {
    try {
      await logout();
      toast({ title: 'Logged out', description: 'You have been logged out successfully' });
    } catch (error) {
      toast({ title: 'Error', description: 'Logout failed', variant: 'destructive' });
    }
  };

  if (isNotInstalled) return <AppNotInstalled />;

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8">
      <Card className="w-full max-w-2xl">
        <CardHeader className="text-center">
          <CardTitle className="text-4xl font-bold">Welcome to {{ app_title }}</CardTitle>
          <CardDescription className="text-lg">Your Next.js frontend for Frappe is ready!</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="bg-muted rounded-lg p-4 text-center">
            {isLoggedIn ? (
              <p className="text-green-600 font-medium">Logged in as: {user}</p>
            ) : (
              <p className="text-muted-foreground">Not logged in (Guest)</p>
            )}
          </div>
          <div className="bg-muted rounded-lg p-4 text-center">
            {systemSettings.loading ? (
              <p className="text-muted-foreground">Connecting to Frappe backend...</p>
            ) : systemSettings.error ? (
              <p className="text-destructive">Unable to connect to Frappe backend</p>
            ) : (
              <p className="text-green-600 font-medium">Connected to Frappe!</p>
            )}
          </div>
          <div className="flex justify-center gap-4">
            {isLoggedIn ? (
              <Button variant="destructive" onClick={handleLogout}>Logout</Button>
            ) : (
              <Link href="/login"><Button>Login</Button></Link>
            )}
          </div>
        </CardContent>
      </Card>
    </main>
  );
}
"""

# globals.css with Tailwind and shadcn variables
NEXTJS_GLOBALS_CSS = """@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 222.2 84% 4.9%;
    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 222.2 84% 4.9%;
    --radius: 0.5rem;
  }
  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --card: 222.2 84% 4.9%;
    --card-foreground: 210 40% 98%;
    --popover: 222.2 84% 4.9%;
    --popover-foreground: 210 40% 98%;
    --primary: 210 40% 98%;
    --primary-foreground: 222.2 47.4% 11.2%;
    --secondary: 217.2 32.6% 17.5%;
    --secondary-foreground: 210 40% 98%;
    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%;
    --accent: 217.2 32.6% 17.5%;
    --accent-foreground: 210 40% 98%;
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 210 40% 98%;
    --border: 217.2 32.6% 17.5%;
    --input: 217.2 32.6% 17.5%;
    --ring: 212.7 26.8% 83.9%;
  }
}

@layer base {
  * { @apply border-border; }
  body { @apply bg-background text-foreground; }
}
"""

# createResource and Frappe utilities (TypeScript)
NEXTJS_FRAPPE_LIB_TSX = """'use client';

import { createContext, useContext, useState, useEffect, useCallback, ReactNode } from 'react';

// Types
interface ResourceOptions {
  method: string;
  params?: Record<string, any>;
  auto?: boolean;
  transform?: (data: any) => any;
  onSuccess?: (data: any) => void;
  onError?: (error: Error) => void;
}

interface Resource<T = any> {
  data: T | null;
  loading: boolean;
  error: Error | null;
  fetch: (params?: Record<string, any>) => Promise<T>;
  reload: () => Promise<T>;
  submit: (params?: Record<string, any>) => Promise<T>;
  reset: () => void;
}

interface ListResourceOptions {
  doctype: string;
  fields?: string[];
  filters?: Record<string, any>;
  orderBy?: string;
  limit?: number;
  start?: number;
  auto?: boolean;
}

interface DocResourceOptions {
  doctype: string;
  name?: string;
  auto?: boolean;
}

// Frappe API call function
// Use empty string in dev to go through Next.js rewrites proxy (avoids CORS)
const FRAPPE_URL = '';

export async function call<T = any>(method: string, params?: Record<string, any>): Promise<T> {
  const response = await fetch(`${FRAPPE_URL}/api/method/${method}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
    credentials: 'include',
    body: JSON.stringify(params || {}),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ message: 'Request failed' }));
    throw new Error(error.message || error.exc || 'Request failed');
  }

  const result = await response.json();
  return result.message;
}

// useResource hook - Similar to frappe-ui's createResource
export function useResource<T = any>(options: ResourceOptions): Resource<T> {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const fetchData = useCallback(async (overrideParams?: Record<string, any>): Promise<T> => {
    setLoading(true);
    setError(null);
    try {
      const result = await call<T>(options.method, { ...options.params, ...overrideParams });
      const transformed = options.transform ? options.transform(result) : result;
      setData(transformed);
      options.onSuccess?.(transformed);
      return transformed;
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Unknown error');
      setError(error);
      options.onError?.(error);
      throw error;
    } finally {
      setLoading(false);
    }
  }, [options.method, JSON.stringify(options.params)]);

  useEffect(() => {
    if (options.auto) fetchData();
  }, [options.auto, fetchData]);

  return {
    data, loading, error,
    fetch: fetchData,
    reload: () => fetchData(),
    submit: fetchData,
    reset: () => { setData(null); setError(null); setLoading(false); },
  };
}

// useListResource - For fetching lists of documents  
export function useListResource<T = any>(options: ListResourceOptions) {
  const [data, setData] = useState<T[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const [start, setStart] = useState(options.start || 0);
  const [hasNextPage, setHasNextPage] = useState(true);
  const limit = options.limit || 20;

  const fetchList = useCallback(async (reset = true): Promise<T[]> => {
    setLoading(true);
    setError(null);
    try {
      const result = await call<T[]>('frappe.client.get_list', {
        doctype: options.doctype,
        fields: options.fields || ['*'],
        filters: options.filters,
        order_by: options.orderBy,
        limit_page_length: limit,
        limit_start: reset ? 0 : start,
      });
      if (reset) { setData(result); setStart(limit); }
      else { setData(prev => [...prev, ...result]); setStart(prev => prev + limit); }
      setHasNextPage(result.length === limit);
      return result;
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Unknown error');
      setError(error);
      throw error;
    } finally { setLoading(false); }
  }, [options.doctype, JSON.stringify(options.filters), options.orderBy, limit, start]);

  useEffect(() => { if (options.auto) fetchList(); }, [options.auto]);

  const insert = async (doc: Partial<T>): Promise<T> => {
    const result = await call<T>('frappe.client.insert', { doc: { doctype: options.doctype, ...doc } });
    await fetchList();
    return result;
  };

  const deleteDoc = async (name: string): Promise<void> => {
    await call('frappe.client.delete', { doctype: options.doctype, name });
    await fetchList();
  };

  return {
    data, list: data, loading, error, hasNextPage,
    fetch: () => fetchList(true),
    reload: () => fetchList(true),
    loadMore: () => fetchList(false),
    insert,
    delete: deleteDoc,
  };
}

// useDocResource - For single document operations
export function useDocResource<T = any>(options: DocResourceOptions) {
  const [doc, setDoc] = useState<T | null>(null);
  const [localChanges, setLocalChanges] = useState<Record<string, any>>({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const [docName, setDocName] = useState(options.name);

  const fetchDoc = useCallback(async (name?: string): Promise<T> => {
    const targetName = name || docName;
    if (!targetName) throw new Error('Document name is required');
    setLoading(true);
    setError(null);
    try {
      const result = await call<T>('frappe.client.get', { doctype: options.doctype, name: targetName });
      setDoc(result);
      setDocName(targetName);
      setLocalChanges({});
      return result;
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Unknown error');
      setError(error);
      throw error;
    } finally { setLoading(false); }
  }, [options.doctype, docName]);

  useEffect(() => { if (options.auto && options.name) fetchDoc(options.name); }, [options.auto, options.name]);

  const setValue = (field: string, value: any) => {
    setLocalChanges(prev => ({ ...prev, [field]: value }));
    setDoc(prev => prev ? { ...prev, [field]: value } as T : null);
  };

  const save = async (): Promise<T> => {
    if (!doc || !docName) throw new Error('No document to save');
    setLoading(true);
    try {
      const result = await call<T>('frappe.client.save', { doc: { ...doc, ...localChanges } });
      setDoc(result);
      setLocalChanges({});
      return result;
    } finally { setLoading(false); }
  };

  const deleteDoc = async (): Promise<void> => {
    if (!docName) throw new Error('No document to delete');
    await call('frappe.client.delete', { doctype: options.doctype, name: docName });
    setDoc(null);
    setDocName(undefined);
  };

  return { doc, loading, error, fetch: fetchDoc, reload: () => fetchDoc(), setValue, save, delete: deleteDoc };
}

// Frappe Context
interface FrappeContextType {
  call: typeof call;
  user: string | null;
  isLoggedIn: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
}

const FrappeContext = createContext<FrappeContextType | null>(null);

export function FrappeProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<string | null>(null);

  const refreshUser = async () => {
    try {
      const result = await call<string>('frappe.auth.get_logged_user');
      setUser(result);
    } catch { setUser(null); }
  };

  const login = async (email: string, password: string) => {
    const response = await fetch(`${FRAPPE_URL}/api/method/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ usr: email, pwd: password }),
    });
    if (!response.ok) {
      const error = await response.json().catch(() => ({ message: 'Login failed' }));
      throw new Error(error.message || 'Login failed');
    }
    await refreshUser();
  };

  const logout = async () => {
    await fetch(`${FRAPPE_URL}/api/method/logout`, { method: 'POST', credentials: 'include' });
    setUser(null);
  };

  useEffect(() => { refreshUser(); }, []);

  return (
    <FrappeContext.Provider value={{ call, user, isLoggedIn: !!user && user !== 'Guest', login, logout, refreshUser }}>
      {children}
    </FrappeContext.Provider>
  );
}

export function useFrappe() {
  const context = useContext(FrappeContext);
  if (!context) throw new Error('useFrappe must be used within a FrappeProvider');
  return context;
}

// Aliases for frappe-ui compatibility
export const createResource = useResource;
export const createListResource = useListResource;
export const createDocumentResource = useDocResource;
"""

# createResource and Frappe utilities (JavaScript)
NEXTJS_FRAPPE_LIB_JS = """'use client';

import { createContext, useContext, useState, useEffect, useCallback } from 'react';

// Use empty string in dev to go through Next.js rewrites proxy (avoids CORS)
const FRAPPE_URL = '';

export async function call(method, params) {
  const response = await fetch(`${FRAPPE_URL}/api/method/${method}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
    credentials: 'include',
    body: JSON.stringify(params || {}),
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({ message: 'Request failed' }));
    throw new Error(error.message || error.exc || 'Request failed');
  }
  const result = await response.json();
  return result.message;
}

export function useResource(options) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchData = useCallback(async (overrideParams) => {
    setLoading(true);
    setError(null);
    try {
      const result = await call(options.method, { ...options.params, ...overrideParams });
      const transformed = options.transform ? options.transform(result) : result;
      setData(transformed);
      options.onSuccess?.(transformed);
      return transformed;
    } catch (err) {
      setError(err);
      options.onError?.(err);
      throw err;
    } finally { setLoading(false); }
  }, [options.method, JSON.stringify(options.params)]);

  useEffect(() => { if (options.auto) fetchData(); }, [options.auto, fetchData]);

  return {
    data, loading, error,
    fetch: fetchData, reload: () => fetchData(), submit: fetchData,
    reset: () => { setData(null); setError(null); setLoading(false); },
  };
}

export function useListResource(options) {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [start, setStart] = useState(options.start || 0);
  const [hasNextPage, setHasNextPage] = useState(true);
  const limit = options.limit || 20;

  const fetchList = useCallback(async (reset = true) => {
    setLoading(true);
    setError(null);
    try {
      const result = await call('frappe.client.get_list', {
        doctype: options.doctype, fields: options.fields || ['*'], filters: options.filters,
        order_by: options.orderBy, limit_page_length: limit, limit_start: reset ? 0 : start,
      });
      if (reset) { setData(result); setStart(limit); }
      else { setData(prev => [...prev, ...result]); setStart(prev => prev + limit); }
      setHasNextPage(result.length === limit);
      return result;
    } catch (err) { setError(err); throw err; }
    finally { setLoading(false); }
  }, [options.doctype, JSON.stringify(options.filters), options.orderBy, limit, start]);

  useEffect(() => { if (options.auto) fetchList(); }, [options.auto]);

  return {
    data, list: data, loading, error, hasNextPage,
    fetch: () => fetchList(true), reload: () => fetchList(true), loadMore: () => fetchList(false),
    insert: async (doc) => { const r = await call('frappe.client.insert', { doc: { doctype: options.doctype, ...doc } }); await fetchList(); return r; },
    delete: async (name) => { await call('frappe.client.delete', { doctype: options.doctype, name }); await fetchList(); },
  };
}

export function useDocResource(options) {
  const [doc, setDoc] = useState(null);
  const [localChanges, setLocalChanges] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [docName, setDocName] = useState(options.name);

  const fetchDoc = useCallback(async (name) => {
    const targetName = name || docName;
    if (!targetName) throw new Error('Document name is required');
    setLoading(true);
    setError(null);
    try {
      const result = await call('frappe.client.get', { doctype: options.doctype, name: targetName });
      setDoc(result); setDocName(targetName); setLocalChanges({});
      return result;
    } catch (err) { setError(err); throw err; }
    finally { setLoading(false); }
  }, [options.doctype, docName]);

  useEffect(() => { if (options.auto && options.name) fetchDoc(options.name); }, [options.auto, options.name]);

  return {
    doc, loading, error, fetch: fetchDoc, reload: () => fetchDoc(),
    setValue: (field, value) => { setLocalChanges(prev => ({ ...prev, [field]: value })); setDoc(prev => prev ? { ...prev, [field]: value } : null); },
    save: async () => { if (!doc || !docName) throw new Error('No document to save'); setLoading(true); try { const r = await call('frappe.client.save', { doc: { ...doc, ...localChanges } }); setDoc(r); setLocalChanges({}); return r; } finally { setLoading(false); } },
    delete: async () => { if (!docName) throw new Error('No document to delete'); await call('frappe.client.delete', { doctype: options.doctype, name: docName }); setDoc(null); setDocName(undefined); },
  };
}

const FrappeContext = createContext(null);

export function FrappeProvider({ children }) {
  const [user, setUser] = useState(null);

  const refreshUser = async () => {
    try { const result = await call('frappe.auth.get_logged_user'); setUser(result); }
    catch { setUser(null); }
  };

  const login = async (email, password) => {
    const response = await fetch(`${FRAPPE_URL}/api/method/login`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, credentials: 'include',
      body: JSON.stringify({ usr: email, pwd: password }),
    });
    if (!response.ok) { const error = await response.json().catch(() => ({ message: 'Login failed' })); throw new Error(error.message || 'Login failed'); }
    await refreshUser();
  };

  const logout = async () => {
    await fetch(`${FRAPPE_URL}/api/method/logout`, { method: 'POST', credentials: 'include' });
    setUser(null);
  };

  useEffect(() => { refreshUser(); }, []);

  return <FrappeContext.Provider value={{ call, user, isLoggedIn: !!user && user !== 'Guest', login, logout, refreshUser }}>{children}</FrappeContext.Provider>;
}

export function useFrappe() {
  const context = useContext(FrappeContext);
  if (!context) throw new Error('useFrappe must be used within a FrappeProvider');
  return context;
}

export const createResource = useResource;
export const createListResource = useListResource;
export const createDocumentResource = useDocResource;
"""

# shadcn cn utility
SHADCN_UTILS = """import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
"""

# shadcn Button component
SHADCN_BUTTON = """import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        outline: "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
        secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-8",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: { variant: "default", size: "default" },
  }
)

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement>, VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button"
    return <Comp className={cn(buttonVariants({ variant, size, className }))} ref={ref} {...props} />
  }
)
Button.displayName = "Button"

export { Button, buttonVariants }
"""

# shadcn Card component
SHADCN_CARD = """import * as React from "react"
import { cn } from "@/lib/utils"

const Card = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => <div ref={ref} className={cn("rounded-lg border bg-card text-card-foreground shadow-sm", className)} {...props} />
)
Card.displayName = "Card"

const CardHeader = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => <div ref={ref} className={cn("flex flex-col space-y-1.5 p-6", className)} {...props} />
)
CardHeader.displayName = "CardHeader"

const CardTitle = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLHeadingElement>>(
  ({ className, ...props }, ref) => <h3 ref={ref} className={cn("text-2xl font-semibold leading-none tracking-tight", className)} {...props} />
)
CardTitle.displayName = "CardTitle"

const CardDescription = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLParagraphElement>>(
  ({ className, ...props }, ref) => <p ref={ref} className={cn("text-sm text-muted-foreground", className)} {...props} />
)
CardDescription.displayName = "CardDescription"

const CardContent = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => <div ref={ref} className={cn("p-6 pt-0", className)} {...props} />
)
CardContent.displayName = "CardContent"

const CardFooter = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => <div ref={ref} className={cn("flex items-center p-6 pt-0", className)} {...props} />
)
CardFooter.displayName = "CardFooter"

export { Card, CardHeader, CardFooter, CardTitle, CardDescription, CardContent }
"""

# shadcn Input component
SHADCN_INPUT = """import * as React from "react"
import { cn } from "@/lib/utils"

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type, ...props }, ref) => (
    <input type={type} className={cn("flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50", className)} ref={ref} {...props} />
  )
)
Input.displayName = "Input"

export { Input }
"""

# shadcn Toaster component
SHADCN_TOASTER = """'use client';

import { Toast, ToastClose, ToastDescription, ToastProvider, ToastTitle, ToastViewport } from "@/components/ui/toast"
import { useToast } from "@/hooks/use-toast"

export function Toaster() {
  const { toasts } = useToast()
  return (
    <ToastProvider>
      {toasts.map(({ id, title, description, action, ...props }) => (
        <Toast key={id} {...props}>
          <div className="grid gap-1">
            {title && <ToastTitle>{title}</ToastTitle>}
            {description && <ToastDescription>{description}</ToastDescription>}
          </div>
          {action}
          <ToastClose />
        </Toast>
      ))}
      <ToastViewport />
    </ToastProvider>
  )
}
"""

# shadcn Toast component
SHADCN_TOAST = """'use client';

import * as React from "react"
import * as ToastPrimitives from "@radix-ui/react-toast"
import { cva, type VariantProps } from "class-variance-authority"
import { X } from "lucide-react"
import { cn } from "@/lib/utils"

const ToastProvider = ToastPrimitives.Provider

const ToastViewport = React.forwardRef<React.ElementRef<typeof ToastPrimitives.Viewport>, React.ComponentPropsWithoutRef<typeof ToastPrimitives.Viewport>>(
  ({ className, ...props }, ref) => (
    <ToastPrimitives.Viewport ref={ref} className={cn("fixed top-0 z-[100] flex max-h-screen w-full flex-col-reverse p-4 sm:bottom-0 sm:right-0 sm:top-auto sm:flex-col md:max-w-[420px]", className)} {...props} />
  )
)
ToastViewport.displayName = ToastPrimitives.Viewport.displayName

const toastVariants = cva(
  "group pointer-events-auto relative flex w-full items-center justify-between space-x-4 overflow-hidden rounded-md border p-6 pr-8 shadow-lg transition-all data-[swipe=cancel]:translate-x-0 data-[swipe=end]:translate-x-[var(--radix-toast-swipe-end-x)] data-[swipe=move]:translate-x-[var(--radix-toast-swipe-move-x)] data-[swipe=move]:transition-none data-[state=open]:animate-in data-[state=closed]:animate-out data-[swipe=end]:animate-out data-[state=closed]:fade-out-80 data-[state=closed]:slide-out-to-right-full data-[state=open]:slide-in-from-top-full data-[state=open]:sm:slide-in-from-bottom-full",
  { variants: { variant: { default: "border bg-background text-foreground", destructive: "destructive group border-destructive bg-destructive text-destructive-foreground" } }, defaultVariants: { variant: "default" } }
)

const Toast = React.forwardRef<React.ElementRef<typeof ToastPrimitives.Root>, React.ComponentPropsWithoutRef<typeof ToastPrimitives.Root> & VariantProps<typeof toastVariants>>(
  ({ className, variant, ...props }, ref) => <ToastPrimitives.Root ref={ref} className={cn(toastVariants({ variant }), className)} {...props} />
)
Toast.displayName = ToastPrimitives.Root.displayName

const ToastAction = React.forwardRef<React.ElementRef<typeof ToastPrimitives.Action>, React.ComponentPropsWithoutRef<typeof ToastPrimitives.Action>>(
  ({ className, ...props }, ref) => <ToastPrimitives.Action ref={ref} className={cn("inline-flex h-8 shrink-0 items-center justify-center rounded-md border bg-transparent px-3 text-sm font-medium ring-offset-background transition-colors hover:bg-secondary focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:pointer-events-none disabled:opacity-50", className)} {...props} />
)
ToastAction.displayName = ToastPrimitives.Action.displayName

const ToastClose = React.forwardRef<React.ElementRef<typeof ToastPrimitives.Close>, React.ComponentPropsWithoutRef<typeof ToastPrimitives.Close>>(
  ({ className, ...props }, ref) => <ToastPrimitives.Close ref={ref} className={cn("absolute right-2 top-2 rounded-md p-1 text-foreground/50 opacity-0 transition-opacity hover:text-foreground focus:opacity-100 focus:outline-none focus:ring-2 group-hover:opacity-100", className)} toast-close="" {...props}><X className="h-4 w-4" /></ToastPrimitives.Close>
)
ToastClose.displayName = ToastPrimitives.Close.displayName

const ToastTitle = React.forwardRef<React.ElementRef<typeof ToastPrimitives.Title>, React.ComponentPropsWithoutRef<typeof ToastPrimitives.Title>>(
  ({ className, ...props }, ref) => <ToastPrimitives.Title ref={ref} className={cn("text-sm font-semibold", className)} {...props} />
)
ToastTitle.displayName = ToastPrimitives.Title.displayName

const ToastDescription = React.forwardRef<React.ElementRef<typeof ToastPrimitives.Description>, React.ComponentPropsWithoutRef<typeof ToastPrimitives.Description>>(
  ({ className, ...props }, ref) => <ToastPrimitives.Description ref={ref} className={cn("text-sm opacity-90", className)} {...props} />
)
ToastDescription.displayName = ToastPrimitives.Description.displayName

type ToastProps = React.ComponentPropsWithoutRef<typeof Toast>
type ToastActionElement = React.ReactElement<typeof ToastAction>

export { type ToastProps, type ToastActionElement, ToastProvider, ToastViewport, Toast, ToastTitle, ToastDescription, ToastClose, ToastAction }
"""

# useToast hook
SHADCN_USE_TOAST = """'use client';

import * as React from "react"
import type { ToastActionElement, ToastProps } from "@/components/ui/toast"

const TOAST_LIMIT = 1
const TOAST_REMOVE_DELAY = 1000000

type ToasterToast = ToastProps & { id: string; title?: React.ReactNode; description?: React.ReactNode; action?: ToastActionElement }

const actionTypes = { ADD_TOAST: "ADD_TOAST", UPDATE_TOAST: "UPDATE_TOAST", DISMISS_TOAST: "DISMISS_TOAST", REMOVE_TOAST: "REMOVE_TOAST" } as const

let count = 0
function genId() { count = (count + 1) % Number.MAX_SAFE_INTEGER; return count.toString(); }

type Action = { type: "ADD_TOAST"; toast: ToasterToast } | { type: "UPDATE_TOAST"; toast: Partial<ToasterToast> } | { type: "DISMISS_TOAST"; toastId?: string } | { type: "REMOVE_TOAST"; toastId?: string }
interface State { toasts: ToasterToast[] }

const toastTimeouts = new Map<string, ReturnType<typeof setTimeout>>()

const addToRemoveQueue = (toastId: string) => {
  if (toastTimeouts.has(toastId)) return
  const timeout = setTimeout(() => { toastTimeouts.delete(toastId); dispatch({ type: "REMOVE_TOAST", toastId }) }, TOAST_REMOVE_DELAY)
  toastTimeouts.set(toastId, timeout)
}

export const reducer = (state: State, action: Action): State => {
  switch (action.type) {
    case "ADD_TOAST": return { ...state, toasts: [action.toast, ...state.toasts].slice(0, TOAST_LIMIT) }
    case "UPDATE_TOAST": return { ...state, toasts: state.toasts.map(t => t.id === action.toast.id ? { ...t, ...action.toast } : t) }
    case "DISMISS_TOAST": {
      const { toastId } = action
      if (toastId) addToRemoveQueue(toastId)
      else state.toasts.forEach(toast => addToRemoveQueue(toast.id))
      return { ...state, toasts: state.toasts.map(t => t.id === toastId || toastId === undefined ? { ...t, open: false } : t) }
    }
    case "REMOVE_TOAST": return action.toastId === undefined ? { ...state, toasts: [] } : { ...state, toasts: state.toasts.filter(t => t.id !== action.toastId) }
  }
}

const listeners: Array<(state: State) => void> = []
let memoryState: State = { toasts: [] }

function dispatch(action: Action) { memoryState = reducer(memoryState, action); listeners.forEach(listener => listener(memoryState)) }

type Toast = Omit<ToasterToast, "id">

function toast({ ...props }: Toast) {
  const id = genId()
  const update = (props: ToasterToast) => dispatch({ type: "UPDATE_TOAST", toast: { ...props, id } })
  const dismiss = () => dispatch({ type: "DISMISS_TOAST", toastId: id })
  dispatch({ type: "ADD_TOAST", toast: { ...props, id, open: true, onOpenChange: open => { if (!open) dismiss() } } })
  return { id, dismiss, update }
}

function useToast() {
  const [state, setState] = React.useState<State>(memoryState)
  React.useEffect(() => { listeners.push(setState); return () => { const index = listeners.indexOf(setState); if (index > -1) listeners.splice(index, 1) } }, [state])
  return { ...state, toast, dismiss: (toastId?: string) => dispatch({ type: "DISMISS_TOAST", toastId }) }
}

export { useToast, toast }
"""

# tailwind.config.js with shadcn
NEXTJS_TAILWIND_CONFIG = """/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ["class"],
  content: ['./src/pages/**/*.{js,ts,jsx,tsx,mdx}', './src/components/**/*.{js,ts,jsx,tsx,mdx}', './src/app/**/*.{js,ts,jsx,tsx,mdx}'],
  theme: {
    container: { center: true, padding: "2rem", screens: { "2xl": "1400px" } },
    extend: {
      colors: {
        border: "hsl(var(--border))", input: "hsl(var(--input))", ring: "hsl(var(--ring))",
        background: "hsl(var(--background))", foreground: "hsl(var(--foreground))",
        primary: { DEFAULT: "hsl(var(--primary))", foreground: "hsl(var(--primary-foreground))" },
        secondary: { DEFAULT: "hsl(var(--secondary))", foreground: "hsl(var(--secondary-foreground))" },
        destructive: { DEFAULT: "hsl(var(--destructive))", foreground: "hsl(var(--destructive-foreground))" },
        muted: { DEFAULT: "hsl(var(--muted))", foreground: "hsl(var(--muted-foreground))" },
        accent: { DEFAULT: "hsl(var(--accent))", foreground: "hsl(var(--accent-foreground))" },
        popover: { DEFAULT: "hsl(var(--popover))", foreground: "hsl(var(--popover-foreground))" },
        card: { DEFAULT: "hsl(var(--card))", foreground: "hsl(var(--card-foreground))" },
      },
      borderRadius: { lg: "var(--radius)", md: "calc(var(--radius) - 2px)", sm: "calc(var(--radius) - 4px)" },
      keyframes: { "accordion-down": { from: { height: "0" }, to: { height: "var(--radix-accordion-content-height)" } }, "accordion-up": { from: { height: "var(--radix-accordion-content-height)" }, to: { height: "0" } } },
      animation: { "accordion-down": "accordion-down 0.2s ease-out", "accordion-up": "accordion-up 0.2s ease-out" },
    },
  },
  plugins: [require("tailwindcss-animate")],
};
"""

# postcss.config.js
NEXTJS_POSTCSS_CONFIG = """module.exports = { plugins: { tailwindcss: {}, autoprefixer: {} } };
"""

# .gitignore for Next.js
NEXTJS_GITIGNORE = """/node_modules
/.next/
/out/
/build
.DS_Store
*.pem
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.env*.local
.vercel
*.tsbuildinfo
next-env.d.ts
"""

# ESLint config
NEXTJS_ESLINTRC = """{ "extends": "next/core-web-vitals" }
"""

# next-env.d.ts
NEXTJS_ENV_DTS = """/// <reference types="next" />
/// <reference types="next/image-types/global" />
"""

# jsconfig.json (for JavaScript projects)
NEXTJS_JSCONFIG = """{ "compilerOptions": { "paths": { "@/*": ["./src/*"] } } }
"""

# components.json for shadcn
SHADCN_COMPONENTS_JSON = """{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "default",
  "rsc": true,
  "tsx": true,
  "tailwind": { "config": "tailwind.config.js", "css": "src/app/globals.css", "baseColor": "slate", "cssVariables": true, "prefix": "" },
  "aliases": { "components": "@/components", "utils": "@/lib/utils", "ui": "@/components/ui", "lib": "@/lib", "hooks": "@/hooks" }
}
"""

# App root package.json (delegates to spa directory)
NEXTJS_APP_PACKAGE_JSON = """{
  "name": "{{ app_name }}",
  "version": "1.0.0",
  "description": "{{ app_title }} using Next.js",
  "main": "index.js",
  "scripts": {
    "test": "echo \\"Error: no test specified\\" && exit 1",
    "postinstall": "cd {{ spa_name }} && npm install",
    "dev": "cd {{ spa_name }} && npm run dev",
    "build": "cd {{ spa_name }} && npm install && npm run build:frappe"
  },
  "keywords": [],
  "author": "",
  "license": "ISC",
  "dependencies": {}
}
"""

# Backward compatibility aliases
NEXTJS_FRAPPE_PROVIDER_TSX = NEXTJS_FRAPPE_LIB_TSX
NEXTJS_FRAPPE_PROVIDER_JS = NEXTJS_FRAPPE_LIB_JS

# Login page (TypeScript)
NEXTJS_LOGIN_PAGE_TSX = """'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useFrappe } from '@/lib/frappe';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { useToast } from '@/hooks/use-toast';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useFrappe();
  const router = useRouter();
  const { toast } = useToast();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await login(email, password);
      toast({ title: 'Success', description: 'Logged in successfully' });
      router.push('/');
    } catch (error) {
      toast({ title: 'Error', description: error instanceof Error ? error.message : 'Login failed', variant: 'destructive' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <CardTitle className="text-2xl font-bold">Login</CardTitle>
          <CardDescription>Sign in to your account</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <label htmlFor="email" className="text-sm font-medium">Email</label>
              <Input id="email" placeholder="user@example.com" value={email} onChange={(e) => setEmail(e.target.value)} required />
            </div>
            <div className="space-y-2">
              <label htmlFor="password" className="text-sm font-medium">Password</label>
              <Input id="password" type="password" placeholder="••••••••" value={password} onChange={(e) => setPassword(e.target.value)} required />
            </div>
            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? 'Signing in...' : 'Sign In'}
            </Button>
          </form>
        </CardContent>
      </Card>
    </main>
  );
}
"""

# Login page (JavaScript)
NEXTJS_LOGIN_PAGE_JS = """'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useFrappe } from '@/lib/frappe';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { useToast } from '@/hooks/use-toast';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useFrappe();
  const router = useRouter();
  const { toast } = useToast();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await login(email, password);
      toast({ title: 'Success', description: 'Logged in successfully' });
      router.push('/');
    } catch (error) {
      toast({ title: 'Error', description: error?.message || 'Login failed', variant: 'destructive' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <CardTitle className="text-2xl font-bold">Login</CardTitle>
          <CardDescription>Sign in to your account</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <label htmlFor="email" className="text-sm font-medium">Email</label>
              <Input id="email" type="email" placeholder="user@example.com" value={email} onChange={(e) => setEmail(e.target.value)} required />
            </div>
            <div className="space-y-2">
              <label htmlFor="password" className="text-sm font-medium">Password</label>
              <Input id="password" type="password" placeholder="••••••••" value={password} onChange={(e) => setPassword(e.target.value)} required />
            </div>
            <Button type="submit" className="w-full" disabled={loading}>{loading ? 'Signing in...' : 'Sign In'}</Button>
          </form>
        </CardContent>
      </Card>
    </main>
  );
}
"""
