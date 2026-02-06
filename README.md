# Arcadian Outfitters Sales Dashboard (Vite + React)

This is a complete runnable Vite React project for the monthly sales dashboard by sales rep.

## Prerequisites

- Node.js 18+ (recommended: 20+)
- npm 9+

## Run locally

```bash
npm install
npm run dev
```

Open the URL printed by Vite (usually `http://localhost:5173`).

## Production build

```bash
npm run build
npm run preview
```

## Deploy options

### 1) Vercel

```bash
npm install -g vercel
vercel
```

Build command: `npm run build`  
Output directory: `dist`

### 2) Netlify

```bash
npm install -g netlify-cli
netlify deploy
netlify deploy --prod
```

Build command: `npm run build`  
Publish directory: `dist`

### 3) GitHub Pages (via static upload)

```bash
npm run build
```

Then upload `dist/` contents to your static host or GitHub Pages publishing target.
