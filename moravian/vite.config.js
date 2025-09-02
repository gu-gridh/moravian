import { defineConfig } from 'vite';
import { viteStaticCopy } from 'vite-plugin-static-copy';
import { resolve } from 'path';

export default defineConfig({
  publicDir: 'public/',
  root: resolve(__dirname, 'moravian/assets/'),
  base: 'static/',
  build: {
    outDir: resolve(__dirname, 'moravian/static/'),
    emptyOutDir: true,
    manifest: 'manifest.json',
    rollupOptions: {
      input: resolve(__dirname, 'moravian/assets/js/index.js'),
    }
  },
  plugins: [
    viteStaticCopy({
      targets: [
        {
          src: resolve(__dirname, 'moravian/assets/images/openseadragon/'),
          dest: 'assets/images/'
        }
      ]
    })
  ]
});
