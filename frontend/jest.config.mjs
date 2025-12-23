import nextJest from 'next/jest.js';

const createJestConfig = nextJest({
  dir: './',
});

const config = {
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'lcov', 'html'],
  collectCoverageFrom: [
    '<rootDir>/components/**/*.{ts,tsx}',
    '<rootDir>/lib/**/*.{ts,tsx}',
    '!<rootDir>/**/*.d.ts',
  ],
  coverageThreshold: {
    global: {
      lines: 90,
      statements: 90,
    },
  },
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/jest.setup.ts'],
  testPathIgnorePatterns: ['<rootDir>/tests/e2e/'],
};

export default createJestConfig(config);
