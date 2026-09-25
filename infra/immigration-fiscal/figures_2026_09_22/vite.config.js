import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

export default defineConfig({
  plugins: [svelte()],
  server: { port: 5199, strictPort: true },
  // Two pages: the figures (index.html) and the prototypes, which the figures page does not link.
  build: { rollupOptions: { input: { main: 'index.html', prototypes: 'prototypes.html' } } },
})
