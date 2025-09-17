import path from 'path';
import { defineConfig } from 'vitest/config';

export default defineConfig({
  resolve: {
    alias: {
      '@antv/infographic': path.resolve(__dirname, './src/index.ts'),
      '@': path.resolve(__dirname, './src'),
      '@@': path.resolve(__dirname, './__tests__'),
    },
  },
  test: {
    environment: 'jsdom',
    coverage: {
      reporter: ['lcov', 'html'],
      reportsDirectory: './coverage',
    },
  },
});
