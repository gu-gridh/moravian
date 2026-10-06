import { defineConfig } from 'vite';
import { viteStaticCopy } from 'vite-plugin-static-copy';
import { resolve } from 'path';

export default defineConfig({
  publicDir: 'public/',
  root: resolve(import.meta.dirname, 'moravian/assets/'),
  base: '/static/',
  build: {
    outDir: resolve(import.meta.dirname, 'moravian/static/'),
    emptyOutDir: true,
    manifest: 'manifest.json',
    rollupOptions: {
      input: resolve(import.meta.dirname, 'moravian/assets/js/index.js'),
    }
  },
  plugins: [
    viteStaticCopy({
      targets: [
        {
          src: resolve(import.meta.dirname, 'moravian/assets/images/'),
          dest: 'assets/'
        }
      ]
    })
  ]
});
